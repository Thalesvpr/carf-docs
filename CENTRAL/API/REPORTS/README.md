# REPORTS

Schemas JSON para geração de relatórios do CARF. ReportGenerateRequest (type enum PDF/Excel/GeoJSON/Shapefile, scope enum Unit/Community/Municipality, filters objeto com date_range/status/city, template_id opcional para templates customizados), ReportGenerateResponse (job_id UUID para polling assíncrono, status enum Queued/Processing/Completed/Failed, estimated_time_seconds), ReportStatusRequest (job_id), ReportStatusResponse (job_id, status, progress_percentage, download_url quando completed, error_message se failed, created_at, completed_at), ReportDownloadRequest (job_id, format), ReportListResponse (items array de reports históricos, pagination). Relatórios suportados: lista de unidades (filtros customizados), resumo comunidade (demographics, mapas), relatório município completo (consolidado). Processamento assíncrono com Hangfire, armazenamento temporário S3/Azure Blob, expiração 7 dias.

## Implementação e Uso

Endpoint de Relatórios implementado pelo backend GEOAPI gerando PDFs via library específica com templates customizáveis por tenant conforme [ADR-005: Multi-tenancy](../../ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md), consumido por GEOWEB para exportação de dados de comunidade via [UC-006: Gerar Relatório Comunidade](../../REQUIREMENTS/USE-CASES/UC-006-gerar-relatorio-comunidade.md) e [UC-007: Exportar Dados Geográficos](../../REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md) gerando Shapefiles para QGIS, acessado via @carf/geoapi-client com download direto de blobs.

---

**Última atualização:** 2025-12-29
