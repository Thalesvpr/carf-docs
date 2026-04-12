---
type: leaf
status: review
updated: 2026-02-07
---

# Admin API - Roles, Clients, Groups e Sessoes

Endpoints para gestao de roles, clients, groups e sessoes no realm CARF. Todos exigem Bearer token com role realm-admin.

## Endpoints de Roles

| Metodo | Endpoint | Descricao |
|:-------|:---------|:----------|
| GET | /admin/realms/{realm}/roles | Lista todas roles do realm |
| POST | /admin/realms/{realm}/roles | Cria nova role |
| GET | /admin/realms/{realm}/users/{id}/role-mappings/realm | Lista roles do usuario |
| POST | /admin/realms/{realm}/users/{id}/role-mappings/realm | Atribui roles ao usuario |
| DELETE | /admin/realms/{realm}/users/{id}/role-mappings/realm | Remove roles do usuario |

A listagem retorna objetos com id, name, description e composite (booleano indicando role composta). As roles do realm CARF sao field-cadastrator, field-coordinator (composta), analyst, manager (composta), admin (composta) e super-admin (composta). Para atribuir ou remover roles, o body e um array de objetos com id e name da role.

## Endpoints de Clients

| Metodo | Endpoint | Descricao |
|:-------|:---------|:----------|
| GET | /admin/realms/{realm}/clients | Lista clients configurados |
| GET | /admin/realms/{realm}/clients/{id}/service-account-user | Obtem service account de client confidential |

A listagem suporta filtro por clientId via query parameter. A resposta inclui id, clientId, name, enabled, publicClient, directAccessGrantsEnabled, standardFlowEnabled, serviceAccountsEnabled, redirectUris e webOrigins.

## Endpoints de Groups

| Metodo | Endpoint | Descricao |
|:-------|:---------|:----------|
| GET | /admin/realms/{realm}/groups | Lista grupos do realm |
| PUT | /admin/realms/{realm}/users/{id}/groups/{groupId} | Adiciona usuario a grupo |
| DELETE | /admin/realms/{realm}/users/{id}/groups/{groupId} | Remove usuario de grupo |

## Gerenciamento de Sessoes

| Metodo | Endpoint | Descricao |
|:-------|:---------|:----------|
| GET | /admin/realms/{realm}/users/{id}/sessions | Lista sessoes ativas do usuario |
| DELETE | /admin/realms/{realm}/users/{id}/sessions | Invalida todas sessoes (logout forcado) |

A resposta de sessoes inclui id, username, ipAddress, start, lastAccess e mapa de clients conectados.

Ver [01-admin-api](./01-admin-api.md) para autenticacao e [01a-admin-api-users](./01a-admin-api-users.md) para endpoints de usuarios.
