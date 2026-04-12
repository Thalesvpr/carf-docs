# PRD — Pipeline Ortofoto Ponta a Ponta

**Projeto:** Sistema Painel Comercial — Módulo Ortofoto  
**Autor:** Thales (Lead Intern, PRODERJ)  
**Data:** 2026-02-26  
**Versão:** 1.1  
**Status:** Em desenvolvimento  

---

## 1. Visão Geral

O módulo de Ortofoto permite que operadores de drone façam upload de GeoTIFFs georreferenciados via REURBWEB (portal admin), que esses rasters sejam processados, empacotados e distribuídos para o aplicativo mobile REURBCAD, onde técnicos de campo usam a ortofoto como base layer offline para demarcação de lotes em áreas de regularização fundiária urbana.

### 1.1 Problema Atual

O pipeline possui a camada de upload e armazenamento funcional, mas falta a extração de georreferenciamento (bounds/SRID), empacotamento para mobile, download real no app, renderização offline e gestão de ciclo de vida das ortofotos. Sem isso, o mobile opera apenas com Google Satellite — sem resolução adequada para demarcação cadastral.

### 1.2 Objetivo

Entregar o pipeline completo: upload → processamento geoespacial → empacotamento → distribuição → renderização offline no mobile, com versionamento e gestão de storage local.

---

## 2. Modelo de Domínio — Hierarquia

```
Tenant
 └── Região / Contrato          ← divisão administrativa (designação de equipe)
      └── Área                   ← unidade geográfica com ortofoto
           │                       (= Community OU Empreendimento, depende do tenant)
           └── Edificação        ← unidade individual (lote/imóvel)
```

### 2.1 Conceitos-Chave

| Conceito | Descrição | Relação com Ortofoto |
|---|---|---|
| **Região / Contrato** | Agrupamento organizacional. Serve para designação de equipe, não tem vínculo geográfico direto com ortofoto. | ❌ Sem ortofoto |
| **Área** | Unidade geográfica de trabalho. É o nível onde a ortofoto se vincula. Pode ser uma **Community** ou um **Empreendimento**, conforme o tipo de tenant. | ✅ 1:1 com ortofoto |
| **Community** | Entity específica para tenants de regularização fundiária (REURB). Representa uma comunidade/assentamento. | É um tipo de Área |
| **Empreendimento** | Entity específica para tenants de empreendimentos imobiliários. Representa um loteamento/condomínio. | É um tipo de Área |
| **Edificação** | Unidade individual dentro de uma Área (lote, imóvel, unidade habitacional). | ❌ Sem ortofoto direta |

### 2.2 Abordagem Polimórfica

Community e Empreendimento são entities **separadas** no banco, mas compartilham uma **interface comum** (`IArea`) para funcionalidades que operam sobre "a área de trabalho" — como ortofoto, pacotes de campo e seleção no mobile.

```csharp
public interface IArea
{
    Guid Id { get; }
    Guid TenantId { get; }
    string Name { get; }
    AreaType AreaType { get; } // Community | Empreendimento
}

public enum AreaType
{
    Community,
    Empreendimento
}
```

A ortofoto referencia a área via **par `(AreaId, AreaType)`** ao invés de `CommunityId` direto. Isso permite:
- Mesma lógica de pipeline pra ambos os tipos
- UI genérica no mobile (AreaPicker)
- Constraint 1:1 funciona por `(AreaId, AreaType)`

---

## 3. Arquitetura do Sistema

### 3.1 Componentes

| Componente | Stack | Responsabilidade |
|---|---|---|
| **REURBWEB** | React/Vite | Portal admin: upload, associação, preview |
| **GEOAPI** | C#/.NET, Hangfire | Backend: processamento, API REST, empacotamento |
| **REURBCAD** | React Native (Expo) | Mobile: download, storage local, mapa offline |
| **S3** | MinIO/AWS | Storage de objetos: originais, previews, tiles |

### 3.2 Fluxo End-to-End

```
[Operador Drone] 
    → Upload .tif via REURBWEB
    → S3 (original)
    → Hangfire ProcessOrtofotoJob
        → Extrai bounds/SRID (GDAL)
        → Gera JPEG preview (4096px)
        → Gera MBTiles (tiles raster)
        → Atualiza entity no DB
    → Admin associa ortofoto ↔ área (1:1, via AreaId + AreaType)
    → GEOAPI empacota bundle ZIP
    
[Técnico de Campo]
    → REURBCAD: AreaPicker seleciona community ou empreendimento
    → Checa versão via API
    → Baixa bundle ZIP
    → Descompacta no FileSystem local
    → MapView renderiza tiles locais offline
    → Troca de área → cleanup automático
```

---

## 4. Requisitos por Prioridade

### P1 — Extração de Bounds/SRID do GeoTIFF

**Onde:** GEOAPI — `ProcessOrtofotoJob`  
**Criticidade:** 🔴 Bloqueante — sem isso nada funciona no mapa  

**Requisitos Funcionais:**
- RF-1.1: Integrar GDAL no pipeline .NET (via `MaxRev.Gdal.Core` ou `MaxRev.Gdal.LinuxRuntime.Minimal`)
- RF-1.2: Após download do .tif do S3, extrair bounding box (minLon, minLat, maxLon, maxLat) usando `Gdal.Open()` + `GetGeoTransform()`
- RF-1.3: Extrair SRID/CRS do GeoTIFF via `GetProjection()` ou `GetSpatialRef()`
- RF-1.4: Se CRS ≠ EPSG:4326, reprojetar bounds automaticamente usando `CoordinateTransformation`
- RF-1.5: Se arquivo não possui georreferenciamento válido, setar status `InvalidGeoreference` e abortar processamento
- RF-1.6: Persistir `BoundsMinLon`, `BoundsMinLat`, `BoundsMaxLon`, `BoundsMaxLat` e `Srid` na entity `Orthophoto`

**Requisitos Não-Funcionais:**
- RNF-1.1: Extração deve levar < 5s para arquivos de até 2GB
- RNF-1.2: GDAL deve funcionar no container Linux (Docker)
- RNF-1.3: Logs estruturados para cada etapa (SRID detectado, bounds extraídos, reprojeção aplicada)

**Critérios de Aceite:**
- Upload de GeoTIFF EPSG:4326 → bounds corretos no DB
- Upload de GeoTIFF EPSG:31983 (SIRGAS 2000 / UTM 23S) → bounds reprojetados para 4326
- Upload de TIFF sem CRS → status `InvalidGeoreference`, bounds null
- Upload de JPEG/PNG → rejeição na validação

---

### P2 — Constraint 1:1 Ortofoto ↔ Área

**Onde:** GEOAPI — `AssociateAreaHandler`  
**Criticidade:** 🟡 Alta — evita inconsistência de dados

**Requisitos Funcionais:**
- RF-2.1: Substituir `CommunityId` por par `(AreaId: Guid, AreaType: AreaType)` na entity `Orthophoto`
- RF-2.2: Endpoint `PATCH /api/orthofotos/{id}/area` recebe `{ areaId, areaType }`
- RF-2.3: Validar que `areaId` existe na entity correspondente (Community se `AreaType.Community`, Empreendimento se `AreaType.Empreendimento`)
- RF-2.4: Ao associar, verificar se já existe ortofoto ativa para aquela `(AreaId, AreaType)` — se sim, soft-swap (anterior vira `Replaced`)
- RF-2.5: Manter histórico: ortofoto substituída não é deletada, apenas desassociada
- RF-2.6: Unique filtered index no DB: `UNIQUE (AreaId, AreaType) WHERE Status = 'Ready' AND DeletedAt IS NULL`
- RF-2.7: Response inclui `previousOrtofotoId` se houve swap

**Critérios de Aceite:**
- Associar ortofoto B à área X (que já tem A) → A fica `Replaced`, B fica ativa
- Query por área sempre retorna 0 ou 1 ortofoto ativa
- Funciona identicamente para Community e Empreendimento
- Validação rejeita `areaId` inexistente

---

### P3 — Package/Bundle Endpoint (ZIP)

**Onde:** GEOAPI — novo `PackagesController`  
**Criticidade:** 🔴 Bloqueante para mobile

**Requisitos Funcionais:**
- RF-3.1: `GET /api/packages/field?areaId={id}&areaType={type}` → metadados do pacote: `{ packageId, version, sizeBytes, ortofotoVersion, vectorsVersion, downloadUrl }`
- RF-3.2: `GET /api/packages/field/{areaId}/version?areaType={type}` → apenas versão para checagem rápida
- RF-3.3: `GET /api/packages/field/{areaId}/download?areaType={type}` → presigned URL para bundle ZIP contendo:
  - `ortofoto.mbtiles` — tiles raster (zoom levels 15-20)
  - `vectors.geojson` — lotes/geometrias da área
  - `meta.json` — metadados com bounds, versão, areaType
- RF-3.4: Bundle cacheado no S3 com invalidação por versão
- RF-3.5: Tenant isolation em todos os endpoints
- RF-3.6: Auth via Bearer token

**Requisitos Não-Funcionais:**
- RNF-3.1: Bundle típico ~50-100MB (MBTiles comprimido)
- RNF-3.2: Geração < 60s
- RNF-3.3: Download via presigned URL (não streama pelo backend)
- RNF-3.4: Cache S3: `{tenantId}/packages/field/{areaType}/{areaId}/v{version}.zip`

**meta.json:**
```json
{
  "version": 3,
  "areaId": "guid",
  "areaType": "Community",
  "areaName": "Nome da Comunidade",
  "bounds": { "minLon": -43.1, "minLat": -22.9, "maxLon": -43.0, "maxLat": -22.8 },
  "srid": 4326,
  "ortofotoVersion": 2,
  "vectorsVersion": 5,
  "generatedAt": "2026-02-26T00:00:00Z"
}
```

**Critérios de Aceite:**
- `GET /packages/field?areaId=X&areaType=Community` retorna 200 se área tem ortofoto ativa
- Retorna 404 se área não tem ortofoto
- ZIP válido com 3 arquivos
- MBTiles abre no QGIS
- Funciona para Community e Empreendimento

---

### P4 — Download Real no Mobile

**Onde:** REURBCAD — `AreaPicker` + `useFieldPackageStore` + FileSystem  
**Criticidade:** 🔴 Bloqueante — conecta stub ao backend

**Requisitos Funcionais:**
- RF-4.1: Renomear `RegionPicker` → `AreaPicker` — componente seleciona Community ou Empreendimento conforme o tenant do usuário
- RF-4.2: O tenant define o `areaType` automaticamente (config do tenant ou detecção)
- RF-4.3: Ao selecionar área, verificar pacote via `GET /packages/field/{areaId}/version?areaType={type}`
- RF-4.4: Se versão local desatualizada ou inexistente → dialog: "Baixar dados de {areaName}? ({sizeFormatted})"
- RF-4.5: Download real do ZIP + progress bar
- RF-4.6: Unzip para `FileSystem: /areas/{areaType}/{areaId}/`
  - `ortofoto.mbtiles`
  - `vectors.geojson`
  - `meta.json`
- RF-4.7: Salvar versão no AsyncStorage
- RF-4.8: Error handling: sem conexão, espaço insuficiente, download corrompido
- RF-4.9: Botão "Atualizar dados" para re-download manual

**Requisitos Não-Funcionais:**
- RNF-4.1: Download resumível ou retry automático
- RNF-4.2: Suportar até 200MB no FileSystem
- RNF-4.3: Descompactação < 30s para 100MB

**Critérios de Aceite:**
- AreaPicker exibe label correto por tenant ("Comunidade" vs "Empreendimento")
- Download funciona end-to-end
- Versão local impede re-download desnecessário

---

### P5 — Overlay de Ortofoto no Mapa (Offline)

**Onde:** REURBCAD — `MapView` component  
**Criticidade:** 🟡 Alta — objetivo principal do módulo

**Requisitos Funcionais:**
- RF-5.1: Ao carregar mapa de área com ortofoto baixada, renderizar MBTiles como tile layer
- RF-5.2: `UrlTile` com tiles extraídos localmente: `file:///areas/{areaType}/{areaId}/tiles/{z}/{x}/{y}.png`
- RF-5.3: Layer ordering: Google Satellite (base) → Ortofoto (z=1) → Vetores/Edificações (z=2)
- RF-5.4: Bounds de `meta.json` definem cobertura — fora dos bounds, Google Satellite transparece
- RF-5.5: Toggle "Mostrar/Ocultar Ortofoto" no menu de camadas
- RF-5.6: Sem ortofoto baixada → mapa funciona normalmente
- RF-5.7: Centralizar mapa nos bounds ao entrar na área

**Abordagem Técnica (Recomendada):**
- Extrair tiles do MBTiles para diretório durante a fase de unzip (P4)
- `UrlTile` aponta para filesystem local
- Conversão TMS → XYZ na extração: `y_xyz = (2^z - 1) - y_tms`

**Critérios de Aceite:**
- Ortofoto renderiza como base layer com resolução adequada
- Zoom in/out carrega tiles corretos
- 100% offline (modo avião)
- Edificações/vetores visíveis acima da ortofoto
- Toggle funciona

---

### P6 — Cleanup ao Trocar Área

**Onde:** REURBCAD — `useAreaStore` (antigo `useCommunityStore`)  
**Criticidade:** 🟢 Média — evita acúmulo de lixo no storage

**Requisitos Funcionais:**
- RF-6.1: Ao trocar de área, dialog: "Trocar de {areaTypeName}? Dados locais de {currentName} serão removidos."
- RF-6.2: Confirmar → deletar `/areas/{areaType}/{oldAreaId}/` inteiro
- RF-6.3: Trocar de tenant → deletar TODO `/areas/`
- RF-6.4: Apenas 1 área baixada por vez (constraint de storage)
- RF-6.5: Exibir: "Dados locais: {size} MB" na tela do AreaPicker
- RF-6.6: Botão "Limpar dados locais" para cleanup manual

**Critérios de Aceite:**
- Trocar área A → B: dados de A removidos após confirmação
- Trocar tenant: tudo removido
- Sem dados órfãos

---

## 5. Modelo de Dados

### 5.1 Entity Orthophoto (atualização)

```
Orthophoto {
    Id: Guid (PK)
    TenantId: Guid (FK)
    
    // Vínculo polimórfico com Área (MUDANÇA: era CommunityId)
    AreaId: Guid? (nullable)
    AreaType: AreaType? (Community | Empreendimento)
    
    // Arquivo
    OriginalFileName: string
    OriginalFileSize: long
    S3KeyOriginal: string
    S3KeyPreview: string?
    S3KeyMbtiles: string?
    
    // Georreferenciamento (P1)
    Srid: int?
    BoundsMinLon: double?
    BoundsMinLat: double?
    BoundsMaxLon: double?
    BoundsMaxLat: double?
    
    // Status
    Status: OrtofotoStatus (Uploaded, Processing, Ready, InvalidGeoreference, Replaced, Deleted)
    
    // Versionamento
    Version: int (auto-increment por área)
    ProcessedAt: DateTime?
    
    // Audit
    CreatedAt: DateTime
    UpdatedAt: DateTime
    CreatedBy: Guid
    DeletedAt: DateTime? (soft-delete)
}

// Constraint: UNIQUE (AreaId, AreaType) WHERE Status = 'Ready' AND DeletedAt IS NULL
```

### 5.2 FieldPackage (cache de bundles)

```
FieldPackage {
    Id: Guid (PK)
    TenantId: Guid (FK)
    
    AreaId: Guid
    AreaType: AreaType
    
    Version: int
    OrtofotoVersion: int
    VectorsVersion: int
    
    S3Key: string
    SizeBytes: long
    
    GeneratedAt: DateTime
    ExpiresAt: DateTime?
}
```

### 5.3 Interface IArea

```csharp
public interface IArea
{
    Guid Id { get; }
    Guid TenantId { get; }
    string Name { get; }
    AreaType AreaType { get; }
}

// Community : IArea { AreaType => AreaType.Community }
// Empreendimento : IArea { AreaType => AreaType.Empreendimento }
```

---

## 6. Endpoints API

| Método | Path | Descrição | Auth |
|---|---|---|---|
| `PATCH` | `/api/orthofotos/{id}/area` | Associar ortofoto a área `{ areaId, areaType }` (P2: com swap) | Admin |
| `GET` | `/api/packages/field?areaId={id}&areaType={type}` | Metadados do pacote | Field |
| `GET` | `/api/packages/field/{areaId}/version?areaType={type}` | Checagem de versão | Field |
| `GET` | `/api/packages/field/{areaId}/download?areaType={type}` | Download bundle ZIP | Field |

---

## 7. Decisões Técnicas

| # | Decisão | Justificativa | Alternativa Descartada |
|---|---|---|---|
| D1 | Polimorfismo via `(AreaId, AreaType)` | Community e Empreendimento são entities separadas com interface comum | FK direta para Community (não suporta Empreendimento) |
| D2 | MBTiles para tiles offline | Arquivo único SQLite, padrão da indústria | Diretório de tiles XYZ |
| D3 | 1 área baixada por vez | Budget de storage mobile ~200MB | Múltiplas áreas |
| D4 | Bundle ZIP sob demanda com cache S3 | Flexível, invalida por versão | Bundle pré-gerado |
| D5 | GDAL no .NET via NuGet | Integração nativa, sem processo externo | GDAL CLI via Process.Start |
| D6 | Tiles extraídos para filesystem | Compatível com UrlTile nativo | Plugin SQLite custom |
| D7 | Soft-swap na associação 1:1 | Preserva histórico | Hard delete |
| D8 | Label dinâmico por tenant | "Comunidade" vs "Empreendimento" no AreaPicker | Termos hardcoded |

---

## 8. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| GDAL não funcionar no container | Média | Alto | Testar Docker early; fallback GDAL CLI |
| MBTiles muito grande para mobile | Média | Alto | Limitar zoom 15-19; JPEG quality 75 |
| Download interrompido corrompe dados | Alta | Médio | Atomic write: .tmp → rename após validação |
| React Native Maps: tiles locais | Baixa | Alto | POC antes; fallback WebView + Leaflet |
| Storage insuficiente no device | Média | Médio | Check antes do download; dialog com tamanho |
| Polimorfismo AreaId/AreaType complexo | Baixa | Médio | IAreaResolver service encapsula lookup |

---

## 9. Métricas de Sucesso

- Upload de GeoTIFF → ortofoto visível no mapa web com bounds corretos em < 5 min
- Técnico baixa área em < 3 min (4G)
- Mapa offline carrega ortofoto em < 2s
- Zero ortofotos duplicadas ativas por área
- Storage local limpo corretamente após troca
- Pipeline funciona identicamente para Community e Empreendimento

---

## 10. Cronograma Estimado

| Sprint | Prioridade | Entrega |
|---|---|---|
| S1 (semana 1-2) | P1 + P2 | GDAL extraction + 1:1 constraint + migração CommunityId → AreaId/AreaType |
| S2 (semana 3-4) | P3 | Package endpoint + MBTiles generation |
| S3 (semana 5-6) | P4 + P5 | Mobile download + map overlay + AreaPicker |
| S4 (semana 7) | P6 | Cleanup + polish + QA |

---

*Documento vivo — atualizar conforme decisões técnicas evoluem.*
