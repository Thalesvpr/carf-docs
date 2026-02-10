---
type: leaf
status: review
updated: 2026-02-08
---

# RequestApprovedEvent

Domain event emitido quando processo de legitimacao e aprovado apos analise. Permite emissao de certidao e conclusao do processo.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo aprovado. |
| UnitId | Guid | Unidade regularizada. |
| ApprovedBy | Guid | Account aprovador. |
| TenantId | Guid | Tenant. |
| ApprovedAt | DateTime | Data de aprovacao. |

## Handlers

| Handler | Acao |
| --- | --- |
| ApprovedNotificationHandler | Notifica requerente. |
| ApprovedCertificateHandler | Inicia emissao de certidao. |
| ApprovedMetricsHandler | Incrementa contador de aprovados. |

## Contexto de Emissao

Emitido no metodo Approve(). Status transita para APPROVED.
