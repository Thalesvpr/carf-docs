# List Holders

Schema e comportamento do endpoint de listagem de titulares.

## Endpoint

```
GET /api/holders
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
```

## Query Parameters

### Paginação

| Parâmetro | Tipo | Default | Descrição |
|-----------|------|---------|-----------|
| page | integer | 1 | Página atual |
| limit | integer | 20 | Itens por página (max 100) |

### Filtros

| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| search | string | Busca em nome e CPF (parcial) |
| cpf | string | CPF exato (com ou sem formatação) |
| name | string | Nome contém (case-insensitive) |
| has_unit | boolean | Com/sem unidade vinculada |
| unit_id | UUID | Titulares de unidade específica |
| community_id | UUID | Titulares de comunidade |
| income_max | number | Renda familiar máxima |
| age_min | integer | Idade mínima |
| age_max | integer | Idade máxima |

### Ordenação

| Parâmetro | Tipo | Default |
|-----------|------|---------|
| sort | string | name | Campos: name, cpf, birth_date, created_at |

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
          "cpf_masked": { "type": "string" },
          "age": { "type": "integer" },
          "contact": {
            "type": "object",
            "properties": {
              "phone": { "type": "string" },
              "email": { "type": "string" }
            }
          },
          "units_count": { "type": "integer" },
          "created_at": { "type": "string", "format": "date-time" }
        }
      }
    },
    "pagination": {
      "type": "object",
      "properties": {
        "page": { "type": "integer" },
        "limit": { "type": "integer" },
        "total": { "type": "integer" },
        "total_pages": { "type": "integer" }
      }
    }
  }
}
```

## Exemplos

```bash
# Listagem básica
curl -X GET "https://api.carf.com.br/api/holders?page=1&limit=20" \
  -H "Authorization: Bearer ..." -H "X-Tenant-ID: ..."

# Busca por nome
curl -X GET "https://api.carf.com.br/api/holders?search=maria%20silva" \
  -H "Authorization: Bearer ..." -H "X-Tenant-ID: ..."

# Titulares de uma comunidade
curl -X GET "https://api.carf.com.br/api/holders?community_id=550e8400..." \
  -H "Authorization: Bearer ..." -H "X-Tenant-ID: ..."
```

## LGPD

- CPF é retornado mascarado por padrão (***.***.***-00)
- CPF completo requer role `admin` ou `cadastrista`
- Listagem é auditada (quem consultou, quando)
- Dados sensíveis (renda, RG) omitidos na listagem, disponíveis apenas no GET individual

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
