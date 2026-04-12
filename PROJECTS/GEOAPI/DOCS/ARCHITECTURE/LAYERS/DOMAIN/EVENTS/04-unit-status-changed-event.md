---
type: leaf
status: review
updated: 2026-02-08
---

# UnitStatusChangedEvent

Domain event emitido por Unit aggregate root sempre que o status do workflow de unidade habitacional transita entre estados. Representa mudanca significativa no processo de regularizacao, permitindo rastreamento de progresso e disparo de acoes automatizadas especificas para cada transicao.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| UnitId | Guid | Identificador da unidade que mudou status. |
| PreviousStatus | UnitStatus | Status anterior antes da transicao. |
| NewStatus | UnitStatus | Status novo apos transicao. |
| ChangedBy | Guid | AccountId responsavel pela mudanca. |
| Reason | string | Justificativa, especialmente para rejeicoes. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC da transicao. |

## Handlers

| Handler | Acao |
| --- | --- |
| StatusChangedNotificationHandler | Envia email ao tecnico de campo quando REQUIRES_CHANGES. |
| StatusChangedCacheHandler | Invalida cache de listagens filtradas por status. |
| StatusChangedMetricsHandler | Recalcula contadores de unidades por status no dashboard. |
| StatusChangedAuditHandler | Registra transicao em audit trail para compliance. |

## Contexto de Emissao

Emitido pelo agregado Unit nos metodos Submit(), Approve(), Reject() e RequestChanges(). Transicoes validas sao verificadas antes de emitir o evento, lancando ConflictException se transicao for invalida.
