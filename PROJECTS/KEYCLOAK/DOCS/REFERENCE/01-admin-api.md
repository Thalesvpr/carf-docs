# Admin REST API

Keycloak Admin REST API base URL /admin/realms/carf autenticada via Bearer token obtido através admin-cli client credentials flow ou token de usuário com role realm-admin. Endpoints principais incluem GET /admin/realms/carf retornando configuração realm, GET /users listando usuários com paginação first max query params e filtros username email search, POST /users criando usuário com payload JSON username email firstName lastName enabled attributes, GET /users/{id} obtendo usuário específico por UUID, PUT /users/{id} atualizando campos, DELETE /users/{id} removendo usuário. Gerenciamento roles via GET /roles listando realm roles, POST /users/{id}/role-mappings/realm atribuindo roles array, DELETE /users/{id}/role-mappings/realm removendo. Clients via GET /clients listando, GET /clients/{id}/service-account-user obtendo service account. Groups via GET /groups, POST /users/{id}/groups/{groupId} adicionando usuário. User attributes acessíveis via attributes map no payload user, atualizáveis via PUT incluindo tenants array e current_tenant para multi-tenancy. Rate limiting recomendado para chamadas bulk, paginação obrigatória para listagens grandes, caching de tokens admin-cli com refresh antes expiração.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
