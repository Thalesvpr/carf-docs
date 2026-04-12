---
type: leaf
status: review
updated: 2026-02-08
---

# HolderLinkedEvent

Domain event emitido por Unit aggregate root quando titular pessoa fisica e vinculado a unidade habitacional atraves de relacionamento UnitHolder. Representa o fato de que um vinculo de propriedade ou ocupacao foi estabelecido, permitindo rastreamento e notificacao de partes envolvidas.

O evento e adicionado durante execucao de Unit.LinkHolder() e despachado apos persistencia bem-sucedida do registro em unit_holders.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| UnitId | Guid | Identificador da unidade ao qual holder foi vinculado. |
| HolderId | Guid | Identificador do titular vinculado. |
| RelationshipType | string | Tipo de vinculo: PROPRIETARIO, CONJUGE, MORADOR, PROCURADOR, HERDEIRO. |
| OwnershipPercentage | decimal | Percentual de propriedade atribuido ao holder. |
| IsPrimary | bool | Se e titular principal responsavel pela unidade. |
| LinkedBy | Guid | AccountId que executou a vinculacao. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC quando vinculacao ocorreu. |

## Handlers

| Handler | Acao |
| --- | --- |
| HolderLinkedCacheHandler | Invalida cache de listagem de holders da unidade. |
| HolderLinkedAuditHandler | Registra em audit trail mudanca de titularidade. |
| HolderLinkedValidationHandler | Valida soma de percentuais nao excede 100%. |

## Contexto de Emissao

Emitido pelo agregado Unit no metodo LinkHolder(holderId, type, percentage). Permite que Unit e Holder mantenham-se desacoplados, referenciando apenas por ID.
