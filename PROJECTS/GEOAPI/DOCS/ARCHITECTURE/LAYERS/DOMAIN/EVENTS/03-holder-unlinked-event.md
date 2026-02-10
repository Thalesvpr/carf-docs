---
type: leaf
status: review
updated: 2026-02-08
---

# HolderUnlinkedEvent

Domain event emitido por Unit aggregate root quando vinculo entre titular e unidade habitacional e removido, representando que um relacionamento de propriedade ou ocupacao foi desfeito. Permite rastreamento de mudancas de titularidade e atualizacao de indices.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| UnitId | Guid | Unidade da qual holder foi desvinculado. |
| HolderId | Guid | Titular removido. |
| RelationshipType | string | Tipo de vinculo que foi desfeito. |
| OwnershipPercentage | decimal | Percentual que holder possuia antes do desvinculo. |
| UnlinkedBy | Guid | AccountId que executou a desvinculacao. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC do desvinculo. |

## Handlers

| Handler | Acao |
| --- | --- |
| HolderUnlinkedCacheHandler | Invalida caches de holders da unidade e unidades do holder. |
| HolderUnlinkedAuditHandler | Registra em audit trail para compliance legal. |
| HolderUnlinkedValidationHandler | Valida que unidade ainda possui ao menos um holder ativo. |

## Contexto de Emissao

Emitido pelo agregado Unit no metodo UnlinkHolder(holderId). Despachado apos SaveChanges garantindo que UnitHolder foi realmente removido do banco.
