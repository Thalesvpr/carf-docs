# Get Unit

Schema e comportamento do endpoint de consulta de unidade habitacional.

## Endpoint

```
GET /api/units/{id}
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
```

## Path Parameters

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| id | UUID | Identificador único da unidade |

## Query Parameters

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| include | string[] | [] | Relações a incluir: holders, community, documents, history |

## Response Schema (200 OK)

```json
{
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "code": { "type": "string" },
    "status": { "enum": ["Rascunho", "Pendente", "Aprovado", "Rejeitado"] },
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "number": { "type": "string" },
        "complement": { "type": "string" },
        "neighborhood": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" },
        "zip_code": { "type": "string" },
        "full_address": { "type": "string" }
      }
    },
    "geometry": {
      "type": "object",
      "description": "GeoJSON Polygon"
    },
    "area_m2": { "type": "number" },
    "centroid": {
      "type": "object",
      "properties": {
        "latitude": { "type": "number" },
        "longitude": { "type": "number" }
      }
    },
    "photos": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "format": "uuid" },
          "url": { "type": "string" },
          "thumbnail_url": { "type": "string" },
          "description": { "type": "string" }
        }
      }
    },
    "holders": {
      "type": "array",
      "description": "Incluído se ?include=holders",
      "items": { "$ref": "#/definitions/HolderSummary" }
    },
    "community": {
      "type": "object",
      "description": "Incluído se ?include=community",
      "$ref": "#/definitions/CommunitySummary"
    },
    "documents": {
      "type": "array",
      "description": "Incluído se ?include=documents"
    },
    "history": {
      "type": "array",
      "description": "Incluído se ?include=history"
    },
    "metadata": { "type": "object" },
    "tenant_id": { "type": "string", "format": "uuid" },
    "created_by": { "type": "string", "format": "uuid" },
    "created_at": { "type": "string", "format": "date-time" },
    "updated_at": { "type": "string", "format": "date-time" }
  }
}
```

## Códigos de Erro

| Código | Erro | Descrição |
|--------|------|-----------|
| 401 | unauthorized | Token inválido ou ausente |
| 403 | forbidden | Sem permissão para visualizar unidades do tenant |
| 404 | not_found | Unidade não encontrada |

## Exemplos

```bash
# Consulta simples
curl -X GET "https://api.carf.com.br/api/units/550e8400-e29b-41d4-a716-446655440000" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "X-Tenant-ID: 550e8400-e29b-41d4-a716-446655440001"

# Com includes
curl -X GET "https://api.carf.com.br/api/units/550e8400...?include=holders,community" \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "X-Tenant-ID: 550e8400..."
```

## Notas

- RLS (Row-Level Security) garante que apenas unidades do tenant são retornadas
- Includes são carregados via LEFT JOIN para evitar N+1 queries
- Geometria é retornada em GeoJSON para compatibilidade com bibliotecas de mapa

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
