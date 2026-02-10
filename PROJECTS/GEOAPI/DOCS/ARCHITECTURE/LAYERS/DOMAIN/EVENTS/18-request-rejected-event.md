---
type: leaf
status: review
updated: 2026-02-08
---

# RequestRejectedEvent

Domain event emitido quando processo de legitimacao e rejeitado apos analise. Encerra processo sem emissao de certidao.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo rejeitado. |
| UnitId | Guid | Unidade vinculada. |
| RejectedBy | Guid | Account responsavel. |
| DecisionReason | text | Justificativa obrigatoria. |
| TenantId | Guid | Tenant. |

## Handlers

| Handler | Acao |
| --- | --- |
| RejectedNotificationHandler | Notifica requerente com motivos. |
| RejectedMetricsHandler | Incrementa rejeitados. |
| RejectedAuditHandler | Registra em audit trail. |

## Contexto de Emissao

Emitido no metodo Reject(). Status transita para REJECTED com justificativa obrigatoria.
