---
type: leaf
status: review
updated: 2026-02-08
---

# CorrectionRequestedEvent

Domain event emitido quando analista solicita correcoes ao requerente antes de prosseguir com analise. Processo pausado aguardando complementacao.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo. |
| AnalystId | Guid | Analista solicitante. |
| Corrections | list | Itens a serem sanados. |
| DeadlineDays | int | Prazo para correcao (tipicamente 30). |
| TenantId | Guid | Tenant. |

## Handlers

| Handler | Acao |
| --- | --- |
| CorrectionNotificationHandler | Notifica requerente com lista de pendencias. |
| CorrectionDeadlineHandler | Agenda alerta de prazo. |
| CorrectionMetricsHandler | Atualiza taxa first-time-right. |

## Contexto de Emissao

Emitido no metodo RequestCorrections(). Status transita para NEEDS_CORRECTION.
