---
type: leaf
status: review
updated: 2026-02-08
---

# Shapefile Import - Importacao de Shapefiles

Feature de importacao de shapefiles mobile, permitindo field collectors carregarem dados geoespaciais externos no formato ESRI Shapefile contendo poligonos de unidades e ocupacoes para integracao bulk no cadastro, facilitando levantamentos tecnicos com dados pre-existentes cartograficos.

## Visao Geral

A importacao e realizada pela tela `ShapefileImportScreen` com botao **Select Shapefile** que abre `Expo Document Picker`, filtrando extensoes `.zip` e `.shp`, permitindo o usuario selecionar arquivo do device storage/downloads.

## Fluxo de Importacao

### 1. Selecao de Arquivo

Componente `FilePickerButton` usando `DocumentPicker.getDocumentAsync` com:
- `type`: `application/zip`, `application/octet-stream`
- `copyToCacheDirectory`: `true`
- Obtem local URI do cache

### 2. Validacao do Shapefile

Service `ShapefileValidator` verifica file integrity e completeness:

1. Verifica presence dos companion files (`shp`, `shx`, `dbf`, `prj`) dentro do ZIP
2. Extrai via `expo-file-system` unzip
3. Le contents e valida structure

### 3. Mapeamento de Atributos

Componente `AttributeMappingTable` exibe shapefile DBF attributes (columns) com dropdown selectors permitindo mapear source fields para target CENTRAL Unit fields:

| Source Field (DBF) | Target Field (Unit) | Descricao |
|--------------------|---------------------|-----------|
| (dropdown) | `name` | Nome da unidade |
| (dropdown) | `address` | Endereco (composed: street, number, neighborhood, city) |
| (dropdown) | `area` | Area em metros quadrados |
| (dropdown) | `holder_name` | Nome do titular |
| (dropdown) | `holder_cpf` | CPF do titular |
| (dropdown) | `community_id` | Identificador da comunidade |

### 4. Preview no Mapa

Componente `PreviewMap` (React Native Maps) renderiza shapefile polygons como geometries overlay no base map:

- Styling diferenciado: **verde** (valid), **vermelho** (invalid)
- Permite inspecao visual antes do import

### 5. Execucao do Import

Componente `ImportProgressModal` mostra:
- Upload progress (percentage)
- Records processed
- Successes e failures em real-time updates

### 6. Rollback

Se import falha midway:
- **Backend**: transaction rollback garantindo consistency
- **Client**: deleta partially imported local records via batch delete operation

## Validacoes

| Validacao | Descricao | Acao se Invalido |
|-----------|-----------|-----------------|
| **File Format** | Extension e mime type checking: aceita `.zip` ou `.shp`, rejeita CSV, GeoJSON, KML | Rejeita arquivo com mensagem de formato incompativel |
| **Shapefile Completeness** | Presence required components: `.shp`, `.shx`, `.dbf`, `.prj` dentro do ZIP | Rejeita como corrupto/incomplete |
| **Geometry Type** | Parsing `.shp` file via `shp.js` ou similar, aceita `Polygon` e `MultiPolygon`, rejeita `Point` e `LineString` | Rejeita geometrias incompativeis com Unit entity |
| **CRS Validation** | Reading `.prj` file, parsing WKT coordinate system definition, checking EPSG codes compativeis: `4326`, `31983` (SIRGAS2000), WGS84 | Oferece reproject via `proj4` library transformation se divergente |
| **Topology Validation** | Basic checks: self-intersections via `turf.js` `kinks` function, invalid rings via `isValid` para cada feature geometry | Alerta errors, permite user corrigir em external GIS tool (QGIS, ArcGIS) antes re-import |
| **Attribute Validation** | Required fields mapped (`name`, `area`, `community_id`) nao null, valid formats: area number positive, CPF format 11 digits se `holder_cpf` mapped | Rejeita records invalidos com detalhes |
| **Duplicate Detection** | Compara geometries com existing local units via spatial query `turf.js` `intersect` ou `contains` | Alerta potential duplicates, oferece skip ou merge options |
| **File Size Limit** | Max 50MB | Previne memory overflow e device crash, requer split em multiplos smaller files via external tool |

## Formatos Aceitos

| Formato | Extensao | Obrigatorio | Descricao |
|---------|----------|-------------|-----------|
| Shapefile geometria | `.shp` | Sim | Contem as geometrias (poligonos) |
| Shapefile index | `.shx` | Sim | Indice de posicao das geometrias |
| Shapefile atributos | `.dbf` | Sim | Tabela de atributos (dBASE) |
| Shapefile projecao | `.prj` | Sim | Definicao do sistema de coordenadas (WKT) |
| Container ZIP | `.zip` | Recomendado | Empacota todos os componentes acima |

## Integracao API

### Upload Online

Quando online, envia shapefile via upload multipart:

```
POST /api/units/import
Content-Type: multipart/form-data
Authorization: Bearer {access_token}

Parameters:
  file: [shapefile ZIP]
  attribute_mapping: JSON config { field_mappings: [{ source, target }] }
  import_options: { skip_duplicates, overwrite_existing }
  tenant_id: UUID
```

Backend GEOAPI processa async job:
1. Extrai ZIP, le shapefile via `NetTopologySuite` / `SharpZipLib`
2. Converte geometrias para formato PostGIS
3. Valida e insere na `Units` table
4. Retorna `job_id`

Client faz polling do status:

```
GET /api/jobs/:jobId

Response: {
  status: "processing" | "completed" | "failed",
  progress: number (percentage),
  records_total: number,
  records_processed: number,
  errors: [{ feature_id, message }]
}
```

### Queue Offline

Se offline, queueing import operation na `sync_queue`:
- Armazena shapefile file URI do cache
- Armazena attribute mapping config
- Postpone ate conexao disponivel
- Sync manager detecta network e push queued import

### Resultado do Import

- Summary dialog mostrando: successes count, failures list com feature IDs e error messages detalhados
- Opcao de retry corrigindo source shapefile e re-importando apenas failed subset
- Imported units aparecem imediatamente na `UnitsList` screen (persistencia local WatermelonDB)
- Sync com server em background quando online

## Domain Model

Shapefile features mapeados para CENTRAL Unit entity:

| Fonte | Metodo de Extracao | Target |
|-------|-------------------|--------|
| DBF attributes | `dbf.js` library reading field values, converting types (string, number, Date) | `name`, `address` (composed: street, number, neighborhood, city) |
| Geometry | `turf.js` `area` function calculating square meters polygon bounds | `area` |
| Geometry centroid | `turf.js` `centroid` function ou user-specified lat/lon columns DBF | `geolocation` |
| DBF columns (se presentes) | `holder_name`, `holder_cpf` | Cria `Holder` records inline, linking via `unit_holders` junction |
| Attribute mapping dropdown | User selects `community_id` target field | `community_id` (source field contendo community identifier string ou foreign key) |

## Requisitos Funcionais Implementados

Implementacao dos requisitos de importacao shapefile:

- Selecionar shapefile do device storage via file picker com validation de formato e presence de components
- Validar geometrias, topology, CRS e attributes antes do import, mostrando validation report com warnings e errors
- Mapear atributos: source DBF fields para target Unit/Holder fields via interactive table com dropdown matching
- Preview features no map canvas com styling diferenciado (valid/invalid) para inspecao visual
- Executar import com progress tracking mostrando successes/failures e summary com retry options
- Tratar duplicates oferecendo estrategias: skip, overwrite, merge
- Offline queue: import postponed ate online, sync automatico

Rastreando requisitos: **RF-012**, **RF-013** (importacao bulk dados geoespaciais, shapefile polygon validation, attribute mapping mobile, facilitando levantamentos tecnicos pre-existentes e cadastro massivo de unidades).

## Referencias

- [Field Collection](./01-field-collection.md)
- [Offline Sync](./03-offline-sync.md)
- [GEOAPI Unit Aggregate](../../../GEOAPI/DOCS/DOMAIN/AGGREGATES/01-unit-aggregate.md)
- [GEOAPI GIS Spatial Patterns](../../../GEOAPI/DOCS/PATTERNS/02-gis-spatial-patterns.md)
- [GeoPolygon Value Object](../../../GEOAPI/DOCS/DOMAIN/VALUE-OBJECTS/02-geo-polygon.md)
