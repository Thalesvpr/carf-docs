---
type: leaf
status: review
updated: 2026-02-08
---

# DeadlineApproachingEvent

Domain event emitido por job scheduler quando prazo legal de 120 dias para conclusao de processo esta se aproximando conforme Lei 13.465/2017.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo com deadline proximo. |
| Deadline | date | Data limite. |
| DaysRemaining | int | Dias restantes. |
| AnalystId | Guid | Analista responsavel. |
| TenantId | Guid | Tenant. |

## Handlers

| Handler | Acao |
| --- | --- |
| DeadlineAnalystHandler | Notifica analista com urgencia. |
| DeadlineManagerHandler | Notifica gestor sobre risco. |
| DeadlinePriorityHandler | Incrementa prioridade na fila. |

## Contexto de Emissao

Emitido por job diario. Alertas disparam aos 30, 15, 7 e 1 dias antes do deadline.
