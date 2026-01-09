# MAINTENANCE

Procedimentos manutenção do CARF. backup-restore.md especifica backup incremental diário (pg_dump GEOAPI database 2am, retention 30 dias local + S3 Glacier long-term), restore (pg_restore from dump, testar staging antes prod). database-maintenance.md rotinas (VACUUM ANALYZE semanal domingo 3am, REINDEX trimestral se bloat > 30 porcento, monitoring slow queries). Scheduled via cron ou Kubernetes CronJob. Checklist pre-maintenance (notificar usuários, read-only mode, backup fresh), post-maintenance (smoke tests, verify integrity, monitoring alerts).

---

**Última atualização:** 2025-12-29
