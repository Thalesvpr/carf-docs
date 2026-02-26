---
type: leaf
status: review
updated: 2026-02-21
---

# Permissões Detalhadas

Backend GEOAPI valida permissões usando atributo [Authorize(Roles = "analyst")] em controllers ou verificação programática com User.IsInRole("admin") para lógica condicional. Frontend esconde elementos de interface baseado em user.roles.includes('admin') obtido do token JWT decodificado.

## Permissões por Role

Permissões de field-cadastrator (base operacional): acessar REURBCAD com mapa e formularios apenas (sem menu completo), criar unidade (POST /units), editar unidade própria (PUT /units/{id} onde created_by = user_id), upload de documentos (POST /units/{id}/documents), visualizar próprio perfil (GET /profile), alterar senha própria (PUT /profile/password). Negado: deletar unidades, aprovar/rejeitar, ver unidades de outros coletores, exportar dados.

Permissões de field-coordinator: tudo de field-cadastrator (herança composite) mais menu mobile completo no REURBCAD, visualizar mapa do tenant (GET /maps), listar unidades da equipe (GET /units?team_id=me), coordenar trabalho de field-cadastrators, client role reurbcad:manage-team. Negado: deletar unidades, aprovar/rejeitar, exportar dados.

Permissões de analyst (ramo separado de field-* — NÃO herda permissões de campo): acessar REURBWEB, aprovar unidade (POST /units/{id}/approve), rejeitar unidade (POST /units/{id}/reject), solicitar correção (POST /units/{id}/request-correction), editar qualquer unidade do tenant, listar todas unidades do tenant, gerar relatórios (GET /reports), exportar CSV/PDF (GET /exports). Negado: gerenciar usuários, configurar tenant.

Permissões de manager: tudo de analyst E tudo de field-coordinator (herança composite de ambos os ramos), permitindo gerenciar equipes de campo enquanto também aprova e gera relatórios. É o perfil que junta capacidade de campo e escritório.

Permissões de admin: tudo de manager (herança composite) mais criar usuário (POST /users via Admin API), editar usuário (PUT /users/{id}), atribuir roles (POST /users/{id}/roles), desativar usuário (DELETE /users/{id}), configurar tenant (PUT /tenants/{id}), visualizar audit logs (GET /audit-logs), gerenciar equipes (CRUD /teams). Client roles admin:manage-users, admin:view-audit-logs.

Permissões de super-admin: tudo de admin (herança composite) mais criar tenant (POST /tenants), deletar tenant (DELETE /tenants/{id}), transferir usuário entre tenants (POST /users/{id}/transfer), acessar qualquer tenant ignorando allowed_tenants, gerenciar realm Keycloak diretamente via Admin Console ou API. Client role admin:manage-tenants.

Permissões de drone-operator (base isolada — NÃO herda de nenhuma role): upload de ortofoto (POST /api/orthofotos/upload), submeter link Pix4D (POST /api/orthofotos/from-link), consultar status de processamento (GET /api/orthofotos/jobs/{jobId}). Negado: tudo mais — nao acessa REURBCAD, REURBWEB, ADMIN, nao visualiza unidades, nao gera relatorios, nao gerencia usuarios ou tenants.
