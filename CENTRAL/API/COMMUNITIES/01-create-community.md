# Create Community

Schema e comportamento do endpoint de criação de comunidades/núcleos.

## Endpoint

```
POST /api/communities
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "required": ["name", "geometry"],
  "properties": {
    "name": {
      "type": "string",
      "minLength": 3,
      "maxLength": 200
    },
    "description": {
      "type": "string",
      "maxLength": 2000
    },
    "geometry": {
      "type": "object",
      "description": "GeoJSON Polygon delimitando a comunidade",
      "properties": {
        "type": { "enum": ["Polygon", "MultiPolygon"] },
        "coordinates": { "type": "array" }
      }
    },
    "reurb_modality": {
      "enum": ["REURB-S", "REURB-E"],
      "description": "S = Social, E = Específica (Lei 13.465/2017)"
    },
    "occupation_type": {
      "enum": ["Urbana", "Rural", "Mista"]
    },
    "land_ownership": {
      "enum": ["Público", "Privado", "Misto"]
    },
    "estimated_units": {
      "type": "integer",
      "minimum": 1
    },
    "contacts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "role": { "type": "string" },
          "phone": { "type": "string" },
          "email": { "type": "string" }
        }
      }
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
    "code": { "type": "string", "example": "COM-2026-00001" },
    "name": { "type": "string" },
    "description": { "type": "string" },
    "geometry": { "type": "object" },
    "area_m2": { "type": "number" },
    "area_hectares": { "type": "number" },
    "centroid": {
      "type": "object",
      "properties": {
        "latitude": { "type": "number" },
        "longitude": { "type": "number" }
      }
    },
    "reurb_modality": { "type": "string" },
    "stats": {
      "type": "object",
      "properties": {
        "units_count": { "type": "integer", "default": 0 },
        "holders_count": { "type": "integer", "default": 0 },
        "estimated_units": { "type": "integer" }
      }
    },
    "tenant_id": { "type": "string", "format": "uuid" },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

## Códigos de Erro

| Código | Erro | Descrição |
|--------|------|-----------|
| 400 | invalid_geometry | Polígono inválido |
| 401 | unauthorized | Token inválido |
| 403 | forbidden | Sem permissão no tenant |
| 409 | name_exists | Nome já existe no tenant |
| 409 | geometry_overlap | Sobrepõe comunidade existente |
| 422 | validation_error | Dados inválidos |

## Notas

- Área é calculada automaticamente a partir da geometria
- Comunidade delimita região geográfica que agrupa unidades
- Unidades dentro do polígono podem ser associadas automaticamente
- REURB-S isenta de custos; REURB-E tem custos de cartório

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
