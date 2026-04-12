---
type: leaf
status: review
updated: 2026-02-08
---

# BlockAddedEvent

Domain event emitido por Community aggregate root quando novo Block (quadra urbana) e adicionado a estrutura espacial da comunidade. Permite organizacao hierarquica de unidades habitacionais em zonas urbanas.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| CommunityId | Guid | Comunidade a qual block foi adicionado. |
| BlockId | Guid | Identificador unico do block criado. |
| Code | string | Codigo unico dentro da comunidade. |
| Name | string | Nome descritivo opcional. |
| Area | decimal | Area em metros quadrados. |
| CreatedBy | Guid | AccountId criador. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC. |

## Handlers

| Handler | Acao |
| --- | --- |
| BlockValidationHandler | Valida que geometria do block esta dentro do boundary da community. |
| BlockCacheHandler | Invalida cache de listagem de blocks. |
| BlockSpatialHandler | Atualiza indice espacial de busca. |

## Contexto de Emissao

Emitido pelo agregado Community no metodo AddBlock(). Indice UNIQUE em (community_id, code) garante codigo unico dentro da comunidade.
