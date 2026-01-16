# Create Unit

Schema e comportamento do endpoint de criação de unidades habitacionais.

## Endpoint

```
POST /api/units
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "required": ["address", "geometry"],
  "properties": {
    "address": {
      "type": "object",
      "required": ["street", "number", "neighborhood", "city", "state", "zip_code"],
      "properties": {
        "street": { "type": "string", "maxLength": 200 },
        "number": { "type": "string", "maxLength": 20 },
        "complement": { "type": "string", "maxLength": 100 },
        "neighborhood": { "type": "string", "maxLength": 100 },
        "city": { "type": "string", "maxLength": 100 },
        "state": { "type": "string", "pattern": "^[A-Z]{2}$" },
        "zip_code": { "type": "string", "pattern": "^\\d{5}-?\\d{3}$" }
      }
    },
    "geometry": {
      "type": "object",
      "description": "GeoJSON Polygon da unidade",
      "required": ["type", "coordinates"],
      "properties": {
        "type": { "enum": ["Polygon"] },
        "coordinates": {
          "type": "array",
          "items": {
            "type": "array",
            "items": {
              "type": "array",
              "items": { "type": "number" },
              "minItems": 2,
              "maxItems": 2
            }
          }
        }
      }
    },
    "area_m2": {
      "type": "number",
      "minimum": 0,
      "description": "Área em metros quadrados (calculada automaticamente se omitido)"
    },
    "photos": {
      "type": "array",
      "maxItems": 10,
      "items": {
        "type": "object",
        "properties": {
          "url": { "type": "string", "format": "uri" },
          "description": { "type": "string", "maxLength": 200 }
        }
      }
    },
    "community_id": {
      "type": "string",
      "format": "uuid",
      "description": "Comunidade a que pertence (opcional)"
    },
    "metadata": {
      "type": "object",
      "description": "Campos customizados do tenant",
      "additionalProperties": true
    }
  }
}
```

## Response Schema (201 Created)

```json
{
  "type": "object",
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "code": { "type": "string", "description": "Código legível (ex: UNI-2026-00001)" },
    "status": { "enum": ["Rascunho", "Pendente", "Aprovado", "Rejeitado"] },
    "address": { "$ref": "#/properties/address" },
    "geometry": { "$ref": "#/properties/geometry" },
    "area_m2": { "type": "number" },
    "centroid": {
      "type": "object",
      "properties": {
        "latitude": { "type": "number" },
        "longitude": { "type": "number" }
      }
    },
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
| 400 | invalid_geometry | Polígono GeoJSON inválido ou auto-intersectante |
| 401 | unauthorized | Token inválido ou ausente |
| 403 | forbidden | Sem permissão para criar unidades no tenant |
| 409 | geometry_overlap | Polígono sobrepõe unidade existente |
| 422 | validation_error | Campos obrigatórios ausentes ou formato inválido |

## Validações

- Polígono deve ser válido (fechado, não auto-intersectante)
- Área calculada deve estar entre 10m² e 100.000m²
- Coordenadas devem estar dentro dos limites do município
- CEP deve corresponder à cidade informada

## Exemplo

```bash
curl -X POST https://api.carf.com.br/api/units \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "X-Tenant-ID: 550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "address": {
      "street": "Rua das Flores",
      "number": "123",
      "neighborhood": "Centro",
      "city": "São Paulo",
      "state": "SP",
      "zip_code": "01310-100"
    },
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[-46.6388, -23.5489], [-46.6385, -23.5489], [-46.6385, -23.5492], [-46.6388, -23.5492], [-46.6388, -23.5489]]]
    }
  }'
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
