# List Units

Schema e comportamento do endpoint de listagem de unidades com filtros e paginação.

## Endpoint

```
GET /api/units
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
```

## Query Parameters

### Paginação

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| page | integer | 1 | Página atual (1-indexed) |
| limit | integer | 20 | Itens por página (max 100) |

### Filtros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| status | string | Filtrar por status: Rascunho, Pendente, Aprovado, Rejeitado |
| neighborhood | string | Filtrar por bairro (parcial, case-insensitive) |
| community_id | UUID | Filtrar por comunidade |
| area_min | number | Área mínima em m² |
| area_max | number | Área máxima em m² |
| created_after | date | Criadas após esta data |
| created_before | date | Criadas antes desta data |
| has_holders | boolean | Filtrar unidades com/sem titulares vinculados |
| search | string | Busca em código, endereço e nome de titular |

### Filtros Geoespaciais

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| bbox | string | Bounding box: minLng,minLat,maxLng,maxLat |
| near | string | Ponto central: lng,lat,radius_meters |
| within | string | GeoJSON Polygon encoded em base64 |

### Ordenação

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| sort | string | -created_at | Campo: code, area_m2, created_at, updated_at |

Prefixo `-` para ordem decrescente.

## Response Schema (200 OK)

```json
{
  "type": "object",
  "properties": {
    "data": {
      "type": "array",
      "items": { "$ref": "#/definitions/UnitSummary" }
    },
    "pagination": {
      "type": "object",
      "properties": {
        "page": { "type": "integer" },
        "limit": { "type": "integer" },
        "total": { "type": "integer" },
        "total_pages": { "type": "integer" },
        "has_next": { "type": "boolean" },
        "has_prev": { "type": "boolean" }
      }
    },
    "aggregations": {
      "type": "object",
      "properties": {
        "total_area_m2": { "type": "number" },
        "count_by_status": {
          "type": "object",
          "additionalProperties": { "type": "integer" }
        }
      }
    }
  }
}
```

### UnitSummary

```json
{
  "id": "uuid",
  "code": "UNI-2026-00001",
  "status": "Aprovado",
  "address": {
    "street": "Rua das Flores",
    "number": "123",
    "neighborhood": "Centro",
    "full_address": "Rua das Flores, 123 - Centro"
  },
  "area_m2": 150.5,
  "centroid": { "latitude": -23.5489, "longitude": -46.6388 },
  "holders_count": 2,
  "created_at": "2026-01-15T10:30:00Z"
}
```

## Exemplos

```bash
# Listagem básica
curl -X GET "https://api.carf.com.br/api/units?page=1&limit=20" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "X-Tenant-ID: 550e8400..."

# Com filtros
curl -X GET "https://api.carf.com.br/api/units?status=Aprovado&neighborhood=Centro&area_min=100" \
  -H "Authorization: Bearer ..." -H "X-Tenant-ID: ..."

# Busca geoespacial (bounding box)
curl -X GET "https://api.carf.com.br/api/units?bbox=-46.64,-23.55,-46.63,-23.54" \
  -H "Authorization: Bearer ..." -H "X-Tenant-ID: ..."
```

## Performance

- Índices GiST em geometry para queries espaciais
- Índices parciais por status para filtros frequentes
- Limite de 100 itens por página para evitar timeouts
- Aggregations são calculadas apenas se solicitadas via ?include_aggregations=true

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
