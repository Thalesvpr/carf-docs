---
status: review
updated: 2026-01-19
---

# Permissões Detalhadas

Backend GEOAPI valida permissões usando atributo [Authorize(Roles = "analyst")] em controllers ou verificação programática com User.IsInRole("admin") para lógica condicional. Frontend esconde elementos de interface baseado em user.roles.includes('admin') obtido do token JWT decodificado.

## Permissões por Role

Permissões de user (base): acessar WEBDOCS seções públicas, visualizar próprio perfil (GET /profile), alterar senha própria (PUT /profile/password). Negado: qualquer operação em unidades, mapas ou dados do tenant.

Permissões de field-agent: tudo de user mais criar unidade (POST /units), editar unidade própria (PUT /units/{id} onde created_by = user_id), upload de documentos (POST /units/{id}/documents), visualizar mapa do tenant (GET /maps), listar unidades próprias (GET /units?created_by=me). Negado: deletar unidades, aprovar/rejeitar, ver unidades de outros coletores, exportar dados.

Permissões de analyst: tudo de field-agent mais aprovar unidade (POST /units/{id}/approve), rejeitar unidade (POST /units/{id}/reject), solicitar correção (POST /units/{id}/request-correction), editar qualquer unidade do tenant, listar todas unidades do tenant, gerar relatórios (GET /reports), exportar CSV/PDF (GET /exports).

Permissões de admin: tudo de analyst mais criar usuário (POST /users via Admin API), editar usuário (PUT /users/{id}), atribuir roles (POST /users/{id}/roles), desativar usuário (DELETE /users/{id}), configurar tenant (PUT /tenants/{id}), visualizar audit logs (GET /audit-logs), gerenciar equipes (CRUD /teams).

Permissões de super-admin: tudo de admin mais criar tenant (POST /tenants), deletar tenant (DELETE /tenants/{id}), transferir usuário entre tenants (POST /users/{id}/transfer), acessar qualquer tenant ignorando allowed_tenants, gerenciar realm Keycloak diretamente via Admin Console ou API.
