# List Communities

Schema e comportamento do endpoint de listagem de comunidades.

## Endpoint

```
GET /api/communities
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
```

## Query Parameters

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| page | integer | 1 | Página atual |
| limit | integer | 20 | Itens por página |
| search | string | | Busca em nome e descrição |
| reurb_modality | string | | REURB-S ou REURB-E |
| has_units | boolean | | Com/sem unidades cadastradas |
| bbox | string | | Bounding box para filtro espacial |
| sort | string | name | name, area_m2, units_count, created_at |

## Response Schema (200 OK)

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "format": "uuid" },
          "code": { "type": "string" },
          "name": { "type": "string" },
          "reurb_modality": { "type": "string" },
          "area_hectares": { "type": "number" },
          "centroid": {
            "type": "object",
            "properties": {
              "latitude": { "type": "number" },
              "longitude": { "type": "number" }
            }
          },
          "stats": {
            "type": "object",
            "properties": {
              "units_count": { "type": "integer" },
              "units_approved": { "type": "integer" },
              "holders_count": { "type": "integer" },
              "completion_percent": { "type": "number" }
            }
          }
        }
      }
    },
    "pagination": { "$ref": "#/definitions/Pagination" },
    "summary": {
      "type": "object",
      "properties": {
        "total_communities": { "type": "integer" },
        "total_area_hectares": { "type": "number" },
        "total_units": { "type": "integer" },
        "reurb_s_count": { "type": "integer" },
        "reurb_e_count": { "type": "integer" }
      }
    }
  }
}
```

## Exemplo

```bash
curl -X GET "https://api.carf.com.br/api/communities?reurb_modality=REURB-S&sort=-units_count" \
  -H "Authorization: Bearer ..." -H "X-Tenant-ID: ..."
```

## GeoJSON Export

Para obter comunidades em formato GeoJSON para uso em mapas:

```
GET /api/communities/geojson
```

Retorna FeatureCollection com todas comunidades do tenant.

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
