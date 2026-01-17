# Workflow Actions

Schema e comportamento dos endpoints de ações no workflow de legitimação.

## Aprovar Processo

```
POST /api/legitimation/{id}/approve
Authorization: Bearer {access_token} (role: aprovador)
X-Tenant-ID: {tenant_uuid}
```

### Request

```json
{
  "type": "object",
  "properties": {
    "comments": { "type": "string", "maxLength": 2000 },
    "registry_info": {
      "type": "object",
      "properties": {
        "registry_number": { "type": "string" },
        "book": { "type": "string" },
        "page": { "type": "string" }
      }
    }
  }
}
```

### Response (200 OK)

```json
{
  "id": "uuid",
  "status": "Aprovado",
  "approved_at": "2026-01-16T10:30:00Z",
  "approved_by": { "id": "uuid", "name": "Maria Aprovadora" },
  "title_ready": true
}
```

## Rejeitar Processo

```
POST /api/legitimation/{id}/reject
Authorization: Bearer {access_token} (role: aprovador)
```

### Request

```json
{
  "type": "object",
  "required": ["reason"],
  "properties": {
    "reason": {
      "enum": [
        "Documentação Insuficiente",
        "Titular Possui Outro Imóvel",
        "Renda Acima do Limite",
        "Ocupação Posterior ao Marco",
        "Área Irregular",
        "Outro"
      ]
    },
    "details": { "type": "string", "maxLength": 2000 }
  }
}
```

## Solicitar Pendência

```
POST /api/legitimation/{id}/request-documents
Authorization: Bearer {access_token} (role: analista)
```

### Request

```json
{
  "type": "object",
  "required": ["documents"],
  "properties": {
    "documents": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "type": { "type": "string" },
          "description": { "type": "string" },
          "required": { "type": "boolean", "default": true }
        }
      }
    },
    "deadline": { "type": "string", "format": "date" },
    "message": { "type": "string" }
  }
}
```

## Responder Pendência

```
POST /api/legitimation/{id}/resolve-pending
Authorization: Bearer {access_token}
Content-Type: multipart/form-data
```

### Request

- `documents[]`: Arquivos enviados
- `comments`: Comentários do solicitante

## Consultar Histórico

```
GET /api/legitimation/{id}/history
Authorization: Bearer {access_token}
```

### Response

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "action": { "type": "string" },
      "from_status": { "type": "string" },
      "to_status": { "type": "string" },
      "user": { "$ref": "#/definitions/UserSummary" },
      "comments": { "type": "string" },
      "timestamp": { "type": "string", "format": "date-time" }
    }
  }
}
```

## Permissões por Role

| Ação | cadastrista | analista | aprovador | admin |
|------|-------------|----------|-----------|-------|
| Submeter | ✓ | ✓ | ✓ | ✓ |
| Analisar | | ✓ | ✓ | ✓ |
| Solicitar docs | | ✓ | ✓ | ✓ |
| Aprovar | | | ✓ | ✓ |
| Rejeitar | | | ✓ | ✓ |

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
