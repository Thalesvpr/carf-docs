# OPERATIONS

Procedimentos operacionais CARF organizados MAINTENANCE backup incremental diário PostgreSQL pg_dump duas horas madrugada retention trinta dias local S3 Glacier long-term restore procedures RTO RPO database maintenance VACUUM ANALYZE semanal REINDEX trimestral bloat maior trinta por cento monitoring slow queries scheduled cron Kubernetes CronJob checklist pré-manutenção notificar usuários read-only mode backup fresh pós-manutenção smoke tests verify integrity monitoring alerts MONITORING observabilidade Prometheus scrape configs GEOAPI PostgreSQL Keycloak alertas HighCPU maior oitenta por cento HighMemory maior noventa por cento HighErrorRate 5xx maior um por cento HighLatency p99 maior um segundo DatabaseConnectionsHigh AlertManager routing Slack email PagerDuty Grafana dashboards GEOAPI PostgreSQL Infrastructure provisioning datasources Prometheus Loki PostgreSQL auto-provisionados Logging agregação logs Loki Promtail structured JSON Serilog correlation IDs distributed tracing retention logs noventa dias audit um ano compress após sete dias archive S3 RUNBOOKS troubleshooting problemas frequentes connection pool exhausted JWT expired RLS policy block slow queries soluções específicas guia sistemático reproduzir issue coletar logs verificar metrics Grafana distributed tracing testar componentes isoladamente aplicar fix validar post-mortem root cause identificando causa raiz implementando correção permanente prevenindo recorrências futuras garantindo resolução rápida incidentes operacionais minimizando downtime impacto usuários define procedures incident response detecção triagem mitigação resolução post-mortem escalation matrix on-call rotation scripts automação limpar cache restart graceful verify data integrity.

## Estrutura

- **[MONITORING/](./MONITORING/README.md)** - Observabilidade Prometheus Grafana Logging Loki
- **[MAINTENANCE/](./MAINTENANCE/README.md)** - Backup restore database maintenance procedures
- **[RUNBOOKS/](./RUNBOOKS/README.md)** - Troubleshooting problemas comuns guias sistemáticos

---

**Última atualização:** 2026-01-11
