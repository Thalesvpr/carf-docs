---
type: leaf
status: review
updated: 2026-02-08
---

# CommunityBoundaryChangedEvent

Domain event emitido por Community aggregate root quando geometria boundary delimitando perimetro espacial da comunidade e modificada. Exige recalculo de estatisticas espaciais e validacao de que unidades habitacionais ainda estao dentro do perimetro.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| CommunityId | Guid | Comunidade cujo boundary foi alterado. |
| OldArea | decimal | Area anterior em metros quadrados. |
| NewArea | decimal | Area apos modificacao. |
| ChangedBy | Guid | AccountId que executou alteracao. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC da alteracao. |

## Handlers

| Handler | Acao |
| --- | --- |
| BoundaryValidationHandler | Valida que todas Units existentes estao dentro do novo boundary. |
| BoundaryCacheHandler | Invalida cache de visualizacao de mapa. |
| BoundaryMetricsHandler | Recalcula estatisticas espaciais da comunidade. |

## Contexto de Emissao

Emitido pelo agregado Community no metodo UpdateBoundary(). Handlers de validacao espacial executam em background job.
