---
type: readme
status: review
updated: 2026-02-07
---

# RUNBOOKS

Procedimentos operacionais para administracao do Keycloak no ecossistema CARF. Cada runbook documenta passos detalhados para operacoes comuns que administradores executam no dia-a-dia.

O [criar usuario](./01-create-user.md) guia criacao de usuarios com roles e atribuicao de tenant (registration esta OFF, usuarios sao criados via ADMIN). O [criar tenant](./02-create-tenant.md) documenta provisionamento de novo municipio no sistema. A [rotacao de secrets](./03-rotate-secrets.md) explica procedimento seguro para trocar client secrets (apenas geogis e confidential). O [troubleshoot auth](./04-troubleshoot-auth.md) orienta diagnostico de falhas de autenticacao. O [backup restore](./05-backup-restore.md) cobre estrategia de backup e disaster recovery. O [monitoring](./06-monitoring.md) documenta health checks (/health/ready) e metricas Prometheus (/metrics).

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (6)

| Documento | Status |
|-----------|--------|
| [Criar Usuário no Keycloak](./01-create-user.md) | ⚠ |
| [Criar e Gerenciar Tenants](./02-create-tenant.md) | ⚠ |
| [Rotacionar Secrets](./03-rotate-secrets.md) | ⚠ |
| [Troubleshoot Autenticação](./04-troubleshoot-auth.md) | ⚠ |
| [Backup e Restore](./05-backup-restore.md) | ⚠ |
| [Monitoramento Keycloak](./06-monitoring.md) | ⚠ |

<!-- CARF-INDEX-END -->
