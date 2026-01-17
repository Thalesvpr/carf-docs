# Create Holder

Schema e comportamento do endpoint de criação de titulares.

## Endpoint

```
POST /api/holders
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "required": ["name", "cpf", "birth_date"],
  "properties": {
    "name": {
      "type": "string",
      "minLength": 3,
      "maxLength": 200
    },
    "cpf": {
      "type": "string",
      "pattern": "^\\d{3}\\.?\\d{3}\\.?\\d{3}-?\\d{2}$",
      "description": "CPF com ou sem formatação"
    },
    "birth_date": {
      "type": "string",
      "format": "date"
    },
    "gender": {
      "enum": ["M", "F", "O"]
    },
    "marital_status": {
      "enum": ["Solteiro", "Casado", "Divorciado", "Viúvo", "União Estável"]
    },
    "contact": {
      "type": "object",
      "properties": {
        "email": { "type": "string", "format": "email" },
        "phone": { "type": "string", "pattern": "^\\+?\\d{10,13}$" },
        "whatsapp": { "type": "string" }
      }
    },
    "address": {
      "type": "object",
      "properties": {
        "street": { "type": "string" },
        "number": { "type": "string" },
        "complement": { "type": "string" },
        "neighborhood": { "type": "string" },
        "city": { "type": "string" },
        "state": { "type": "string" },
        "zip_code": { "type": "string" }
      }
    },
    "rg": {
      "type": "object",
      "properties": {
        "number": { "type": "string" },
        "issuer": { "type": "string" },
        "state": { "type": "string" }
      }
    },
    "income": {
      "type": "object",
      "properties": {
        "source": { "enum": ["Empregado", "Autônomo", "Aposentado", "Benefício", "Desempregado"] },
        "monthly_value": { "type": "number", "minimum": 0 },
        "family_composition": { "type": "integer", "minimum": 1 }
      }
    },
    "unit_id": {
      "type": "string",
      "format": "uuid",
      "description": "Vincular a unidade existente"
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
    "code": { "type": "string", "description": "Código legível (ex: TIT-2026-00001)" },
    "name": { "type": "string" },
    "cpf_masked": { "type": "string", "example": "***.***.***-00" },
    "birth_date": { "type": "string", "format": "date" },
    "age": { "type": "integer" },
    "contact": { "type": "object" },
    "units": {
      "type": "array",
      "items": { "$ref": "#/definitions/UnitSummary" }
    },
    "tenant_id": { "type": "string", "format": "uuid" },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

## Códigos de Erro

| Código | Erro | Descrição |
|--------|------|-----------|
| 400 | invalid_cpf | CPF inválido (dígitos verificadores) |
| 401 | unauthorized | Token inválido |
| 403 | forbidden | Sem permissão no tenant |
| 409 | cpf_exists | CPF já cadastrado no tenant |
| 422 | validation_error | Dados inválidos |

## Validações

- CPF validado com algoritmo oficial (dígitos verificadores)
- Data de nascimento deve resultar em idade >= 18 anos
- Email deve ser único por tenant (se informado)
- Nome deve conter pelo menos duas palavras

## Exemplo

```bash
curl -X POST https://api.carf.com.br/api/holders \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIs..." \
  -H "X-Tenant-ID: 550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria da Silva Santos",
    "cpf": "123.456.789-00",
    "birth_date": "1985-03-15",
    "contact": { "phone": "11999998888" },
    "unit_id": "550e8400-e29b-41d4-a716-446655440001"
  }'
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
