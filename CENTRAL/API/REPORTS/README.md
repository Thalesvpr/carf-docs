# REPORTS

Schemas JSON para geração de relatórios do CARF.

O ReportGenerateRequest contém type (PDF, Excel, GeoJSON, Shapefile), scope (Unit, Community, Municipality), filters e template_id opcional. A geração é assíncrona, retornando job_id para polling de status.

Relatórios suportados: lista de unidades com filtros customizados, resumo de comunidade com demographics e mapas, relatório consolidado do município.

Processamento assíncrono com armazenamento temporário e expiração em 7 dias.

## Endpoints

- POST /api/reports/generate - Iniciar geração
- GET /api/reports/{job_id}/status - Consultar status
- GET /api/reports/{job_id}/download - Download quando completo
- GET /api/reports - Listar histórico de relatórios

## Schemas

- ReportGenerateRequest / ReportGenerateResponse
- ReportStatusRequest / ReportStatusResponse
- ReportDownloadRequest
- ReportListResponse

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review
