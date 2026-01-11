# OPERATIONS

Procedimentos operacionais do CARF organizados em MAINTENANCE (backup-restore.md com estratégia de backup incremental diário e full semanal do PostgreSQL usando pg_dump, retention de 30 dias, restore procedures e RTO/RPO; database-maintenance.md com vacuum/analyze scheduling, reindex de tabelas fragmentadas, e monitoring de bloat) e RUNBOOKS (common-issues.md listando problemas frequentes como connection pool exhausted, JWT expired, RLS policy block com diagnóstico e solução; troubleshooting.md com guia sistemático de investigação usando logs, métricas, e tracing). Define procedimentos de incident response (detecção→triagem→mitigação→resolução→post-mortem), escalation matrix (quem acionar em cada tipo de incidente), e on-call rotation. Inclui scripts de automação para tarefas repetitivas (limpar cache, restart graceful, verify data integrity).

## Estrutura

- **[MONITORING/](./MONITORING/README.md)** - Observabilidade com Prometheus, Grafana e Logging (Loki/ELK)
- **[MAINTENANCE/](./MAINTENANCE/README.md)** - Procedimentos de backup, restore e database maintenance
- **[RUNBOOKS/](./RUNBOOKS/README.md)** - Guias de troubleshooting e problemas comuns

---

**Última atualização:** 2025-12-29
