# Data Export

Schema e comportamento dos endpoints de exportação de dados em formatos tabulares e geoespaciais.

## Excel Export

```
POST /api/reports/excel
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
```

### Request

```json
{
  "type": "object",
  "required": ["entity_type"],
  "properties": {
    "entity_type": {
      "enum": ["units", "holders", "communities", "legitimations"]
    },
    "filters": {
      "type": "object",
      "description": "Mesmos filtros do endpoint de listagem"
    },
    "columns": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Colunas a incluir (todas se omitido)"
    },
    "include_relations": {
      "type": "boolean",
      "default": false,
      "description": "Incluir dados relacionados em abas separadas"
    }
  }
}
```

### Response (202 Accepted)

```json
{
  "job_id": "uuid",
  "status": "queued",
  "status_url": "/api/reports/status/{job_id}"
}
```

## GeoJSON Export

```
GET /api/export/geojson/{entity_type}
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
```

### Path Parameters

- `entity_type`: units, communities

### Query Parameters

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| Todos os filtros do list endpoint | | Aplicados ao export |
| properties | string[] | Propriedades a incluir no GeoJSON |
| simplify | number | Tolerância de simplificação (metros) |

### Response (200 OK)

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[...]]]
      },
      "properties": {
        "id": "uuid",
        "code": "UNI-2026-00001",
        "status": "Aprovado",
        "area_m2": 150.5
      }
    }
  ]
}
```

## Shapefile Export

```
POST /api/reports/shapefile
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
```

### Request

```json
{
  "entity_type": "units",
  "filters": {},
  "crs": "EPSG:31983",
  "encoding": "UTF-8"
}
```

### Response

ZIP contendo .shp, .shx, .dbf, .prj

## CSV Export

```
GET /api/export/csv/{entity_type}
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
Accept: text/csv
```

Streaming de CSV direto, sem necessidade de job assíncrono para datasets pequenos.

## Limites

| Formato | Limite de Registros | Timeout |
|---------|---------------------|---------|
| Excel | 50.000 | 5 min |
| GeoJSON | 10.000 | 2 min |
| Shapefile | 100.000 | 10 min |
| CSV | 100.000 | 5 min |

Para exports maiores, use filtros ou solicite export programado.

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
