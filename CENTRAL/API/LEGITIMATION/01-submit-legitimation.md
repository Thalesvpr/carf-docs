# Submit Legitimation

Schema e comportamento do endpoint de submissão de processo de legitimação fundiária.

## Endpoint

```
POST /api/legitimation
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "required": ["unit_id", "holders"],
  "properties": {
    "unit_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unidade a ser legitimada"
    },
    "holders": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["holder_id", "ownership_type"],
        "properties": {
          "holder_id": { "type": "string", "format": "uuid" },
          "ownership_type": {
            "enum": ["Proprietário", "Coproprietário", "Usufrutuário", "Possuidor"]
          },
          "ownership_percentage": {
            "type": "number",
            "minimum": 0,
            "maximum": 100
          }
        }
      }
    },
    "modality": {
      "enum": ["REURB-S", "REURB-E"],
      "description": "Herdado da comunidade se não especificado"
    },
    "occupation_date": {
      "type": "string",
      "format": "date",
      "description": "Data de início da ocupação"
    },
    "documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": {
            "enum": ["Comprovante Residência", "RG", "CPF", "Contrato", "Declaração", "Outro"]
          },
          "file_id": { "type": "string", "format": "uuid" },
          "description": { "type": "string" }
        }
      }
    },
    "declaration": {
      "type": "object",
      "properties": {
        "no_other_property": { "type": "boolean" },
        "family_income_range": {
          "enum": ["Até 1 SM", "1-3 SM", "3-5 SM", "Acima 5 SM"]
        },
        "agreed_terms": { "type": "boolean" }
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
    "protocol": { "type": "string", "example": "LEG-2026-00001" },
    "status": {
      "enum": ["Submetido", "Em Análise", "Pendência", "Aprovado", "Rejeitado"]
    },
    "unit": { "$ref": "#/definitions/UnitSummary" },
    "holders": {
      "type": "array",
      "items": { "$ref": "#/definitions/HolderSummary" }
    },
    "modality": { "type": "string" },
    "workflow": {
      "type": "object",
      "properties": {
        "current_step": { "type": "string" },
        "next_steps": { "type": "array", "items": { "type": "string" } },
        "estimated_completion": { "type": "string", "format": "date" }
      }
    },
    "created_at": { "type": "string", "format": "date-time" }
  }
}
```

## Códigos de Erro

| Código | Erro | Descrição |
|--------|------|-----------|
| 400 | unit_not_approved | Unidade ainda não está aprovada |
| 400 | holder_has_property | Titular já possui imóvel (REURB-S) |
| 400 | incomplete_documents | Documentos obrigatórios ausentes |
| 409 | already_submitted | Processo já existe para esta unidade |
| 422 | ownership_exceeds_100 | Soma de participações excede 100% |

## Workflow de Legitimação

1. **Submetido** → Processo criado, aguardando análise
2. **Em Análise** → Técnico avaliando documentação
3. **Pendência** → Documentos faltantes ou correções necessárias
4. **Aprovado** → Apto para emissão de título
5. **Rejeitado** → Não atende requisitos legais

## Requisitos Lei 13.465/2017

- REURB-S: Renda familiar até 5 salários mínimos
- REURB-S: Não possuir outro imóvel urbano ou rural
- Ocupação deve ser anterior a 22/12/2016 (marco temporal)
- Unidade deve estar em área urbana consolidada

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
