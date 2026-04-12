---
type: leaf
status: review
updated: 2026-02-08
---

# ContestationReceivedEvent

Domain event emitido quando terceiro apresenta contestacao formal contra processo durante edital publico. Pausa workflow ate resolucao.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo contestado. |
| ContestationType | string | OWNERSHIP_CLAIM, BOUNDARY_DISPUTE, etc. |
| Content | text | Alegacoes detalhadas. |
| TenantId | Guid | Tenant. |

## Handlers

| Handler | Acao |
| --- | --- |
| ContestationPauseHandler | Pausa workflow automaticamente. |
| ContestationNotificationHandler | Notifica requerente e analista. |
| ContestationMetricsHandler | Incrementa processos contestados. |

## Contexto de Emissao

Emitido ao receber contestacao durante CONTESTATION_PERIOD. Status transita para CONTESTATION_RECEIVED.
