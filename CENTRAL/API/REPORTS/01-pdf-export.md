# PDF Export

Schema e comportamento do endpoint de exportação de relatórios em PDF.

## Endpoint

```
POST /api/reports/pdf
Authorization: Bearer {access_token}
X-Tenant-ID: {tenant_uuid}
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "required": ["report_type"],
  "properties": {
    "report_type": {
      "enum": [
        "unit_detail",
        "holder_detail",
        "community_summary",
        "legitimation_status",
        "cadastral_map",
        "progress_report"
      ]
    },
    "entity_id": {
      "type": "string",
      "format": "uuid",
      "description": "ID da entidade para relatórios individuais"
    },
    "filters": {
      "type": "object",
      "properties": {
        "community_id": { "type": "string", "format": "uuid" },
        "status": { "type": "array", "items": { "type": "string" } },
        "date_from": { "type": "string", "format": "date" },
        "date_to": { "type": "string", "format": "date" }
      }
    },
    "options": {
      "type": "object",
      "properties": {
        "include_map": { "type": "boolean", "default": true },
        "include_photos": { "type": "boolean", "default": true },
        "include_signatures": { "type": "boolean", "default": false },
        "paper_size": { "enum": ["A4", "Letter"], "default": "A4" },
        "orientation": { "enum": ["portrait", "landscape"], "default": "portrait" }
      }
    }
  }
}
```

## Response (202 Accepted)

```json
{
  "type": "object",
  "properties": {
    "job_id": { "type": "string", "format": "uuid" },
    "status": { "enum": ["queued", "processing", "completed", "failed"] },
    "estimated_time_seconds": { "type": "integer" },
    "status_url": { "type": "string", "format": "uri" }
  }
}
```

## Consultar Status

```
GET /api/reports/status/{job_id}
```

### Response (Completed)

```json
{
  "job_id": "uuid",
  "status": "completed",
  "download_url": "https://storage.carf.com.br/reports/uuid.pdf",
  "expires_at": "2026-01-16T12:00:00Z",
  "file_size_bytes": 1048576,
  "pages": 15
}
```

## Tipos de Relatório

### unit_detail
Ficha completa da unidade com mapa, fotos, titulares e histórico.

### holder_detail
Cadastro completo do titular com unidades vinculadas.

### community_summary
Resumo da comunidade com estatísticas, mapa de situação e lista de unidades.

### legitimation_status
Status do processo de legitimação com timeline de workflow.

### cadastral_map
Mapa cadastral da comunidade ou conjunto de unidades.

### progress_report
Relatório de progresso do projeto REURB com gráficos e indicadores.

## Exemplo

```bash
# Gerar relatório de unidade
curl -X POST https://api.carf.com.br/api/reports/pdf \
  -H "Authorization: Bearer ..." \
  -H "X-Tenant-ID: ..." \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "unit_detail",
    "entity_id": "550e8400-e29b-41d4-a716-446655440000",
    "options": { "include_map": true, "include_photos": true }
  }'

# Consultar status
curl https://api.carf.com.br/api/reports/status/job-uuid-here \
  -H "Authorization: Bearer ..."
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
