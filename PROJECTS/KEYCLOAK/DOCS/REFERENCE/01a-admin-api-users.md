---
type: leaf
status: review
updated: 2026-02-07
---

# Admin API - Endpoints de Usuarios

Endpoints para gestao de usuarios no realm CARF. Todos exigem Bearer token com role realm-admin. Base path: /admin/realms/carf/users.

## Listagem e Contagem

| Metodo | Endpoint | Descricao |
|:-------|:---------|:----------|
| GET | /admin/realms/{realm}/users | Lista usuarios com paginacao e filtros |
| GET | /admin/realms/{realm}/users/count | Conta usuarios com filtros opcionais |

Parametros de query para listagem:

| Parametro | Tipo | Descricao |
|:----------|:-----|:----------|
| first | int | Offset para paginacao (default 0) |
| max | int | Limite de resultados (default 100, max 1000) |
| search | string | Busca em username, firstName, lastName, email |
| username | string | Filtro exato por username |
| email | string | Filtro exato por email |
| enabled | boolean | Filtro por status |
| briefRepresentation | boolean | Retorna versao resumida (default true) |

A resposta retorna array de objetos usuario contendo id, username (CPF no CARF), email, firstName, lastName, enabled, emailVerified, createdTimestamp e attributes com tenants, current_tenant e community_ids.

## CRUD de Usuario

| Metodo | Endpoint | Descricao |
|:-------|:---------|:----------|
| POST | /admin/realms/{realm}/users | Cria novo usuario |
| GET | /admin/realms/{realm}/users/{id} | Obtem usuario por ID |
| PUT | /admin/realms/{realm}/users/{id} | Atualiza dados do usuario |
| DELETE | /admin/realms/{realm}/users/{id} | Remove usuario |

Para criacao, o body contem username (CPF), email, firstName, lastName, enabled, emailVerified, attributes (tenants e current_tenant) e credentials com type password, value e temporary true. Resposta 201 Created com header Location contendo URL do novo recurso. Atualizacao aceita body parcial. Remocao retorna 204 No Content.

Ver [01-admin-api](./01-admin-api.md) para autenticacao e [01b-admin-api-roles-clients](./01b-admin-api-roles-clients.md) para roles e clients.
