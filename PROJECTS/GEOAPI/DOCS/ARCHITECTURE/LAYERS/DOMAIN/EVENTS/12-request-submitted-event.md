---
type: leaf
status: review
updated: 2026-02-08
---

# RequestSubmittedEvent

Domain event emitido por LegitimationRequest aggregate root quando processo de legitimacao e formalmente submetido para analise. Inicia contagem de prazos legais de 120 dias conforme Lei 13.465/2017.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo submetido. |
| UnitId | Guid | Unidade vinculada. |
| RequestedBy | Guid | Account que submeteu. |
| TenantId | Guid | Tenant. |
| RequestedAt | DateTime | Data de protocolo. |

## Handlers

| Handler | Acao |
| --- | --- |
| SubmittedAnalystHandler | Atribui analista por carga de trabalho. |
| SubmittedNotificationHandler | Envia confirmacao com protocolo. |
| SubmittedDeadlineHandler | Inicia contagem de 120 dias. |

## Contexto de Emissao

Emitido no metodo Submit(). Status transita de DRAFT para SUBMITTED.
