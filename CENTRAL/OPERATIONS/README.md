# OPERATIONS

Procedimentos operacionais do CARF para monitoramento, manutenção e troubleshooting.

O [monitoramento](./MONITORING/README.md) usa Prometheus para métricas, Grafana para dashboards e Loki para agregação de logs. Alertas são configurados para CPU, memória, taxa de erros, latência e conexões de banco. SLOs definem 99.5% uptime e p99 latency menor que 500ms.

A [manutenção](./MAINTENANCE/README.md) inclui backup incremental diário do PostgreSQL às 2h com retenção de 30 dias local e S3 Glacier para long-term. Rotinas de VACUUM ANALYZE rodam semanalmente e REINDEX trimestralmente. Checklists garantem notificação de usuários, modo read-only e smoke tests após manutenção.

Os [runbooks](./RUNBOOKS/README.md) documentam troubleshooting de problemas frequentes como connection pool exhausted, JWT expired, RLS policy block e slow queries, com guia sistemático para reproduzir, coletar logs, verificar métricas e aplicar fix.

## Estrutura

- **[MONITORING/](./MONITORING/README.md)** - Prometheus, Grafana e Loki
- **[MAINTENANCE/](./MAINTENANCE/README.md)** - Backup, restore e manutenção de banco
- **[RUNBOOKS/](./RUNBOOKS/README.md)** - Troubleshooting de problemas comuns

---

**Última atualização:** 2026-01-14
