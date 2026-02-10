---
type: leaf
status: review
updated: 2026-02-08
---

# UnitCreatedEvent

Domain event emitido quando nova Unit e criada no sistema, indicando que uma unidade habitacional foi registrada. Permite side effects como notificar equipe de campo, criar entrada em timeline da comunidade e disparar integracoes externas.

O evento e adicionado a colecao DomainEvents no construtor de Unit ou metodo estatico Unit.Create(), sendo despachado apos SaveChanges bem-sucedido.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| UnitId | Guid | Identificador da unidade criada. |
| CommunityId | Guid | Comunidade a qual pertence. |
| Code | string | Codigo da unidade no formato UNI-AAAA-NNNNN. |
| Status | UnitStatus | Status inicial, tipicamente DRAFT. |
| CreatedBy | Guid | AccountId do usuario que criou. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC do evento. |

## Handlers

| Handler | Acao |
| --- | --- |
| UnitCreatedCacheHandler | Invalida cache de listagem de unidades da comunidade. |
| UnitCreatedTimelineHandler | Cria entrada de audit trail visivel no frontend. |
| UnitCreatedNotificationHandler | Cria notificacao in-app para manager da equipe. |

## Contexto de Emissao

Emitido pelo agregado Unit no construtor ou metodo Create(). O evento e registrado via AddDomainEvent sem disparo imediato, aguardando SaveChanges do IUnitOfWork.
