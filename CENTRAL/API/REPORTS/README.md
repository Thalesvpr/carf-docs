# REPORTS

Schemas JSON para geração de relatórios do CARF. ReportGenerateRequest (type enum PDF/Excel/GeoJSON/Shapefile, scope enum Unit/Community/Municipality, filters objeto com date_range/status/city, template_id opcional para templates customizados), ReportGenerateResponse (job_id UUID para polling assíncrono, status enum Queued/Processing/Completed/Failed, estimated_time_seconds), ReportStatusRequest (job_id), ReportStatusResponse (job_id, status, progress_percentage, download_url quando completed, error_message se failed, created_at, completed_at), ReportDownloadRequest (job_id, format), ReportListResponse (items array de reports históricos, pagination). Relatórios suportados: lista de unidades (filtros customizados), resumo comunidade (demographics, mapas), relatório município completo (consolidado). Processamento assíncrono com Hangfire, armazenamento temporário S3/Azure Blob, expiração 7 dias.

---

**Última atualização:** 2025-12-29
