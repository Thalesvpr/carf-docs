---
type: leaf
status: review
updated: 2026-02-08
---

# CommunityCreatedEvent

Domain event emitido por Community aggregate root apos criacao bem-sucedida de nova comunidade ou assentamento, representando que area geografica de regularizacao foi estabelecida no sistema. Permite inicializacao de recursos e configuracoes especificas.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| CommunityId | Guid | Identificador unico da comunidade criada. |
| Name | string | Nome descritivo da comunidade. |
| Code | string | Codigo identificador legivel. |
| CommunityType | CommunityType | URBANA, RURAL, QUILOMBOLA ou RIBEIRINHA. |
| Municipality | string | Municipio ao qual pertence. |
| State | string | UF (2 letras). |
| CreatedBy | Guid | AccountId do criador. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC da criacao. |

## Handlers

| Handler | Acao |
| --- | --- |
| CommunityStorageHandler | Cria estrutura de pastas em S3 para documentos da comunidade. |
| CommunityAuthorizationHandler | Cria CommunityAuthorization inicial para o Account criador. |
| CommunityMetricsHandler | Incrementa contador de comunidades ativas no dashboard. |

## Contexto de Emissao

Emitido pelo agregado Community no construtor ou metodo Create(). A CommunityAuthorization inicial garante que a comunidade nao fica orfao sem ninguem autorizado a acessa-la.
