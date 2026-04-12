---
type: leaf
status: review
updated: 2026-02-08
---

# AccessRevokedEvent

Domain event emitido por Community aggregate root quando CommunityAuthorization e revogada, removendo permissao de acesso de Team ou Account. Exige limpeza de dados locais no app mobile e invalidacao de caches.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| CommunityId | Guid | Comunidade da qual acesso foi revogado. |
| AuthorizationId | Guid | CommunityAuthorization removida. |
| TeamId | Guid | Team que perdeu acesso (se coletiva). |
| AccountId | Guid | Account que perdeu acesso (se individual). |
| RevokedBy | Guid | AccountId que revogou acesso. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC. |

## Handlers

| Handler | Acao |
| --- | --- |
| RevokeNotificationHandler | Notifica Account ou membros de Team sobre remocao de acesso. |
| RevokeCacheHandler | Invalida cache de comunidades acessiveis. |
| RevokeSyncHandler | Dispara limpeza de dados locais no app mobile. |

## Contexto de Emissao

Emitido pelo agregado Community no metodo RevokeAccess(). Valida que nao e ultima autorizacao ativa, prevenindo comunidade inacessivel.
