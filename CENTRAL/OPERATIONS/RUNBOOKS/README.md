---
status: review
updated: 2026-01-15
---

# RUNBOOKS

Runbooks de troubleshooting do CARF para resolução rápida de incidentes operacionais.

## Problemas Frequentes

- Connection pool exhausted
- JWT expired
- RLS policy block
- Slow queries

## Guia de Troubleshooting

1. Reproduzir o issue
2. Coletar logs com correlation ID
3. Verificar métricas no Grafana
4. Usar distributed tracing para rastrear
5. Testar componentes isoladamente
6. Aplicar fix
7. Validar correção

## Post-mortem

Após resolução, documentar:
- Root cause identificado
- Correção permanente implementada
- Ações para prevenir recorrência


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (8 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-connection-pool-exhausted](./01-connection-pool-exhausted.md) | Connection Pool Exhausted |
| [02-jwt-token-expired](./02-jwt-token-expired.md) | JWT Token Expired |
| [03-rls-policy-violation](./03-rls-policy-violation.md) | RLS Policy Violation |
| [04-slow-query-detection](./04-slow-query-detection.md) | Slow Query Detection |
| [05-service-health-check](./05-service-health-check.md) | Service Health Check |
| [06-database-backup-restore](./06-database-backup-restore.md) | Database Backup e Restore |
| [07-cache-invalidation](./07-cache-invalidation.md) | Cache Invalidation |
| [08-storage-quota-exceeded](./08-storage-quota-exceeded.md) | Storage Quota Exceeded |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/01-connection-pool-exhausted.md|Connection Pool Exhausted]]
- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/02-jwt-token-expired.md|JWT Token Expired]]
- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/03-rls-policy-violation.md|RLS Policy Violation]]
- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/04-slow-query-detection.md|Slow Query Detection]]
- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/05-service-health-check.md|Service Health Check]]
- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/06-database-backup-restore.md|Database Backup e Restore]]
- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/07-cache-invalidation.md|Cache Invalidation]]
- ○ [[CENTRAL/OPERATIONS/RUNBOOKS/08-storage-quota-exceeded.md|Storage Quota Exceeded]]

<!-- CARF-INDEX-END -->
