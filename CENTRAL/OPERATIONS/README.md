# OPERATIONS

Procedimentos operacionais do CARF para monitoramento, manutenção e troubleshooting.

O [monitoramento](./MONITORING/README.md) usa Prometheus para métricas, Grafana para dashboards e Loki para agregação de logs. Alertas são configurados para CPU, memória, taxa de erros, latência e conexões de banco. SLOs definem 99.5% uptime e p99 latency menor que 500ms.

A [manutenção](./MAINTENANCE/README.md) inclui backup incremental diário do PostgreSQL às 2h com retenção de 30 dias local e S3 Glacier para long-term. Rotinas de VACUUM ANALYZE rodam semanalmente e REINDEX trimestralmente. Checklists garantem notificação de usuários, modo read-only e smoke tests após manutenção.

Os [runbooks](./RUNBOOKS/README.md) documentam troubleshooting de problemas frequentes como connection pool exhausted, JWT expired, RLS policy block e slow queries, com guia sistemático para reproduzir, coletar logs, verificar métricas e aplicar fix.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Aguardando index gerado por script.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Maintenance](./MAINTENANCE/README.md) | 0 |
|  | [Monitoring](./MONITORING/README.md) | 0 |
|  | [Runbooks](./RUNBOOKS/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
