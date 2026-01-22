---
type: readme
status: rejected
description: "Conteudo operacional. Runbooks e procedimentos pertencem a repo de ops ou PROJECTS."
updated: 2026-01-15
---

# OPERATIONS

Procedimentos operacionais do CARF para monitoramento, manutenção e troubleshooting.

O [monitoramento](./MONITORING/README.md) usa Prometheus para métricas, Grafana para dashboards e Loki para agregação de logs. Alertas são configurados para CPU, memória, taxa de erros, latência e conexões de banco. SLOs definem 99.5% uptime e p99 latency menor que 500ms.

A [manutenção](./MAINTENANCE/README.md) inclui backup incremental diário do PostgreSQL às 2h com retenção de 30 dias local e S3 Glacier para long-term. Rotinas de VACUUM ANALYZE rodam semanalmente e REINDEX trimestralmente. Checklists garantem notificação de usuários, modo read-only e smoke tests após manutenção.

Os [runbooks](./RUNBOOKS/README.md) documentam troubleshooting de problemas frequentes como connection pool exhausted, JWT expired, RLS policy block e slow queries, com guia sistemático para reproduzir, coletar logs, verificar métricas e aplicar fix.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (24 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Maintenance](./MAINTENANCE/README.md) | 5 |
|  | [Monitoring](./MONITORING/README.md) | 11 |
|  | [Runbooks](./RUNBOOKS/README.md) | 8 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/OPERATIONS/MAINTENANCE/README|MAINTENANCE]]
- [[CENTRAL/OPERATIONS/MONITORING/README|MONITORING]]
- [[CENTRAL/OPERATIONS/RUNBOOKS/README|RUNBOOKS]]

<!-- CARF-INDEX-END -->
