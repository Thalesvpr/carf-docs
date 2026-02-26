# PROMPT.md — Ortofoto Pipeline (All Priorities)

You are implementing the complete Orthophoto Pipeline for the REURBCAD/GEOAPI/REURBWEB system. This is a government land regularization platform (PRODERJ, Rio de Janeiro). Work through ALL phases sequentially. Do NOT skip phases. Do NOT move to the next phase until the current one compiles and passes tests.

## System Context

- **GEOAPI**: C#/.NET 8 backend with Hangfire background jobs, Entity Framework Core, S3 storage (MinIO), multi-tenant with tenant isolation
- **REURBWEB**: React/Vite admin portal with Leaflet maps
- **REURBCAD**: React Native (Expo) mobile app with react-native-maps
- **DB**: PostgreSQL with EF Core migrations
- **Storage**: S3-compatible (MinIO) — path pattern: `{tenantId}/ortofotos/{yyyy}/{MM}/original/{id}.tif`

## Critical Domain Model

The system has a **polymorphic area concept**:

```
Tenant
 └── Região / Contrato    ← organizational only (team assignment), NO ortofoto
      └── Área             ← geographic unit WITH ortofoto (1:1)
           │                  = Community OR Empreendimento (depends on tenant type)
           └── Edificação  ← individual unit (lot/building)
```

- **Community** and **Empreendimento** are SEPARATE entities in the DB
- They share an interface `IArea { Id, TenantId, Name, AreaType }`
- `AreaType` enum: `Community`, `Empreendimento`
- Orthophoto links to area via `(AreaId: Guid, AreaType: AreaType)` — NOT `CommunityId`
- The mobile label changes per tenant: "Comunidade" vs "Empreendimento"
- Região is purely organizational — it has NO ortofoto, NO package, NO download

## Existing Code to Understand First

Before writing ANY code, read and understand:
1. The existing `Orthophoto` entity and its current fields (likely has `CommunityId` — this needs migration to `AreaId` + `AreaType`)
2. The existing `Community` entity and `Empreendimento` entity (if exists)
3. The existing `ProcessOrtofotoJob` — it already generates JPEG preview (4096px max)
4. The existing `PATCH /api/orthofotos/{id}/community` endpoint (to be replaced with `/area`)
5. The existing S3 service/helper classes
6. The existing tenant isolation patterns (middleware, base repository)
7. The existing mobile `RegionPicker` component (to be renamed to `AreaPicker`)

Run `find . -name "*.cs" | head -50` and `find . -name "*.tsx" | head -50` to map the codebase.

---

## Phase 1: GDAL Bounds/SRID Extraction

### What to Do
1. Add GDAL NuGet packages: `MaxRev.Gdal.Core` and `MaxRev.Gdal.LinuxRuntime.Minimal`
2. Create `IGdalService` and `GdalService` with methods:
   - `ExtractGeoReference(string filePath)` → returns `GeoReference { Srid, MinLon, MinLat, MaxLon, MaxLat }`
   - Must handle: EPSG:4326 (passthrough), EPSG:31983/SIRGAS UTM (reproject to 4326), no CRS (return null)
3. Add fields to `Orthophoto` entity if not present: `Srid (int?)`, `BoundsMinLon`, `BoundsMinLat`, `BoundsMaxLon`, `BoundsMaxLat` (all `double?`)
4. Create EF migration for new fields
5. Modify `ProcessOrtofotoJob`:
   - After downloading .tif from S3, call `GdalService.ExtractGeoReference()`
   - If null → set `Status = OrtofotoStatus.InvalidGeoreference`, save, return
   - If valid → populate bounds + SRID fields, continue to JPEG generation
6. Add structured logging: SRID detected, bounds extracted, reprojection applied
7. Write unit tests for `GdalService`:
   - Test with EPSG:4326 GeoTIFF mock
   - Test with non-4326 CRS (verify reprojection)
   - Test with non-georeferenced TIFF (verify null return)

### Verification
- `dotnet build` succeeds
- `dotnet test` passes all new tests
- No existing tests broken

---

## Phase 2: Polymorphic Area Binding + 1:1 Constraint

### What to Do

**2A — Migration from CommunityId to AreaId/AreaType:**
1. Create `AreaType` enum: `Community = 0, Empreendimento = 1`
2. Create `IArea` interface: `{ Guid Id, Guid TenantId, string Name, AreaType AreaType }`
3. Make `Community` implement `IArea` (AreaType = Community)
4. If `Empreendimento` entity exists, make it implement `IArea`. If it doesn't exist yet, create a stub entity that implements `IArea`
5. Add `AreaId (Guid?)` and `AreaType (AreaType?)` to `Orthophoto` entity
6. Create EF migration:
   - Add `AreaId` and `AreaType` columns
   - Migrate existing data: `UPDATE Orthophotos SET AreaId = CommunityId, AreaType = 0 WHERE CommunityId IS NOT NULL`
   - Drop `CommunityId` column (or keep as deprecated — check if other code uses it)
7. Create `IAreaResolver` service:
   - `ResolveArea(Guid areaId, AreaType areaType)` → returns `IArea` by querying the correct DbSet
   - Used by handlers to validate that the area actually exists

**2B — 1:1 Constraint:**
1. Replace the existing `PATCH /api/orthofotos/{id}/community` with `PATCH /api/orthofotos/{id}/area`
   - Request body: `{ areaId: Guid, areaType: AreaType }`
   - Uses `IAreaResolver` to validate area exists
2. Add swap logic:
   - Query: `var existing = await repo.FirstOrDefaultAsync(o => o.AreaId == areaId && o.AreaType == areaType && o.Status == OrtofotoStatus.Ready && o.Id != ortofotoId)`
   - If exists: `existing.AreaId = null; existing.AreaType = null; existing.Status = OrtofotoStatus.Replaced;`
3. Add `Replaced` to `OrtofotoStatus` enum if not present
4. Add filtered unique index: `UNIQUE (AreaId, AreaType) WHERE Status = 'Ready' AND DeletedAt IS NULL`
   - Via EF Core: `.HasIndex(o => new { o.AreaId, o.AreaType }).HasFilter("\"Status\" = 'Ready' AND \"DeletedAt\" IS NULL").IsUnique()`
5. Response DTO includes `previousOrtofotoId` if swap occurred
6. Write tests:
   - Associate B to area that has A → A becomes Replaced
   - Associate to area with no existing → normal
   - Works for both Community and Empreendimento AreaTypes
   - Rejects invalid areaId

### Verification
- `dotnet build` succeeds
- `dotnet test` passes
- Migration applies cleanly
- Old `CommunityId` references are updated or removed

---

## Phase 3: Package/Bundle Endpoint

### What to Do
1. Create `PackagesController` with routes:
   - `GET /api/packages/field?areaId={id}&areaType={type}` → package metadata
   - `GET /api/packages/field/{areaId}/version?areaType={type}` → version check only
   - `GET /api/packages/field/{areaId}/download?areaType={type}` → presigned S3 URL to ZIP bundle
2. Create `FieldPackage` entity:
   ```
   Id (Guid), TenantId (Guid), AreaId (Guid), AreaType (AreaType),
   Version (int), OrtofotoVersion (int), VectorsVersion (int),
   S3Key (string), SizeBytes (long), GeneratedAt (DateTime)
   ```
3. Create `IFieldPackageService` with:
   - `GetOrGeneratePackage(Guid areaId, AreaType areaType)` — checks cache, generates if stale
   - Package generation: create ZIP with `ortofoto.mbtiles`, `vectors.geojson`, `meta.json`
4. MBTiles generation:
   - Use GDAL: `gdal2tiles.py` equivalent in C# OR shell out to `gdal2tiles.py` via `Process.Start`
   - Zoom levels 15-20
   - Pack tiles into MBTiles (SQLite) format
   - Store in S3: `{tenantId}/packages/field/{areaType}/{areaId}/v{version}.zip`
5. `meta.json` structure:
   ```json
   {
     "version": 3,
     "areaId": "guid",
     "areaType": "Community",
     "areaName": "Nome",
     "bounds": { "minLon": -43.1, "minLat": -22.9, "maxLon": -43.0, "maxLat": -22.8 },
     "srid": 4326,
     "ortofotoVersion": 2,
     "vectorsVersion": 5,
     "generatedAt": "2026-02-26T00:00:00Z"
   }
   ```
6. `vectors.geojson`: query edificações/lotes da área and serialize as GeoJSON FeatureCollection
7. Tenant isolation on all endpoints
8. Write tests for controller and service

### Verification
- `dotnet build` succeeds
- `dotnet test` passes
- Manual test: `curl` to endpoints returns expected JSON
- ZIP is valid and contains 3 files

---

## Phase 4: Mobile Download + AreaPicker

### What to Do

**4A — Rename RegionPicker → AreaPicker:**
1. Find the existing `RegionPicker` component in the React Native codebase
2. Rename to `AreaPicker`
3. Update all imports/references
4. Make the label dynamic based on tenant:
   - If tenant uses Communities → label "Comunidade", list communities
   - If tenant uses Empreendimentos → label "Empreendimento", list empreendimentos
   - The `areaType` should come from tenant config or be derived from which entities the tenant has
5. The picker should NOT show Regiões as selectable areas for ortofoto/download — Região is organizational only

**4B — Download Implementation:**
1. Create `useFieldPackageStore` (Zustand or context):
   - State: `{ downloadedAreaId, downloadedAreaType, localVersion, downloadProgress, isDownloading }`
   - Actions: `checkVersion()`, `downloadPackage()`, `clearLocal()`
2. Create `fieldPackageApi.ts`:
   - `getPackageVersion(areaId, areaType)` → GET /packages/field/{areaId}/version?areaType={type}
   - `getPackageDownloadUrl(areaId, areaType)` → GET /packages/field/{areaId}/download?areaType={type}
3. In `AreaPicker`:
   - After selecting area, call `checkVersion()`
   - If no local data OR version mismatch → dialog: "Baixar dados de {areaName}? ({sizeFormatted})"
   - On confirm → download ZIP → unzip to `/areas/{areaType}/{areaId}/`
     - `ortofoto.mbtiles`
     - `vectors.geojson`
     - `meta.json`
   - Save version to AsyncStorage
4. Progress bar, error handling (network, storage, corruption)
5. "Atualizar dados" button for manual re-download

### Dependencies to Install
```
expo-file-system
react-native-zip-archive (or jszip)
@react-native-async-storage/async-storage
```

### Verification
- App compiles: `npx expo start` succeeds
- TypeScript: `npx tsc --noEmit` passes
- AreaPicker shows correct label per tenant type
- RegionPicker no longer exists (fully renamed)

---

## Phase 5: Ortofoto Overlay on Map

### What to Do
1. After area is loaded with downloaded package:
   - Read `meta.json` for bounds and areaType
   - Extract tiles from MBTiles to: `/areas/{areaType}/{areaId}/tiles/{z}/{x}/{y}.png`
     - MBTiles uses TMS y-axis. Convert: `y_xyz = (2^z - 1) - y_tms`
   - OR: Extract during unzip phase (Phase 4) to avoid delay at map load
2. Add `UrlTile` to MapView:
   ```jsx
   {hasOrtofoto && showOrtofoto && (
     <UrlTile
       urlTemplate={`file://${tilesDir}/{z}/{x}/{y}.png`}
       maximumZ={20}
       minimumZ={15}
       zIndex={1}
     />
   )}
   ```
3. Layer ordering: Google Satellite (base) → Ortofoto (z=1) → Vectors/Edificações (z=2)
4. Toggle button: "Mostrar/Ocultar Ortofoto"
5. `fitToCoordinates` with bounds from meta.json on area load
6. Edge cases:
   - Missing tiles → transparent (Google Satellite shows through)
   - No ortofoto downloaded → normal Google Satellite only

### Verification
- Map renders ortofoto tiles
- Toggle works
- Works in airplane mode (fully offline)
- Edificações render above ortofoto

---

## Phase 6: Cleanup on Area Switch

### What to Do
1. In area store (rename `useCommunityStore` → `useAreaStore` if needed):
   - Before switching area: check if local data exists
   - Dialog: "Trocar de {areaTypeName}? Dados locais de {currentName} serão removidos."
   - On confirm: delete `/areas/{areaType}/{oldAreaId}/` recursively
   - Clear AsyncStorage version key
2. On tenant switch:
   - Delete entire `/areas/` directory
   - Clear all package-related AsyncStorage keys
3. Storage info in AreaPicker: "Dados locais: {sizeMB} MB"
4. "Limpar dados" manual cleanup button

### Verification
- Switch area A→B: folder A deleted, folder B downloaded
- Switch tenant: all area folders deleted
- Storage size displays correctly
- No orphan files

---

## Global Rules

1. Follow existing code patterns — naming conventions, folder structure, DI registration
2. All new code must have XML doc comments (C#) or JSDoc (TypeScript)
3. Maintain tenant isolation on every query and endpoint
4. Use structured logging (Serilog pattern) for all operations
5. EF migrations must be idempotent
6. Mobile code must handle offline scenarios gracefully
7. Do NOT modify existing working features — only add new functionality
8. Run `dotnet build` and `dotnet test` after every phase
9. Run `npx tsc --noEmit` for mobile TypeScript changes
10. NEVER use `CommunityId` for ortofoto — always `(AreaId, AreaType)`
11. Região/Contrato is ORGANIZATIONAL ONLY — no ortofoto, no package, no download associated with it

## Completion

After ALL 6 phases are implemented, verified, and passing:

Output <promise>PIPELINE_COMPLETE</promise>

If stuck on a phase for more than 5 iterations:
- Document what is blocking
- List what you've tried
- Skip to next phase if current is non-blocking
- Still output <promise>PIPELINE_COMPLETE</promise> when all possible phases are done, noting which phases are incomplete
