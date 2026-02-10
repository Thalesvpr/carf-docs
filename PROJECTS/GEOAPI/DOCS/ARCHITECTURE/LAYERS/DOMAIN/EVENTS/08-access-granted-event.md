---
type: leaf
status: review
updated: 2026-02-08
---

# AccessGrantedEvent

Domain event emitido por Community aggregate root quando nova CommunityAuthorization e concedida a Team ou Account individual. Representa que permissao de acesso foi estabelecida, controlando escopo de sincronizacao offline no app mobile.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| CommunityId | Guid | Comunidade para qual acesso foi concedido. |
| AuthorizationId | Guid | CommunityAuthorization criada. |
| TeamId | Guid | Team que recebeu acesso (se coletiva). Mutuamente exclusivo com AccountId. |
| AccountId | Guid | Account que recebeu acesso (se individual). |
| PermissionLevel | string | READ, WRITE ou ADMIN. |
| GrantedBy | Guid | AccountId que concedeu acesso. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC. |

## Handlers

| Handler | Acao |
| --- | --- |
| AccessNotificationHandler | Notifica Account ou membros de Team sobre novo acesso. |
| AccessCacheHandler | Invalida cache de comunidades acessiveis. |
| AccessSyncHandler | Atualiza configuracao de sincronizacao offline no mobile. |

## Contexto de Emissao

Emitido pelo agregado Community no metodo GrantAccess(). Constraint XOR garante que exatamente um entre team_id e account_id esta preenchido.
