# RBAC e Permissões

Hierarquia: super-admin (tudo) > admin (gestão tenant) > analyst (validação) > field-collector (coleta). field-collector: criar/editar unidades próprias, upload fotos/docs, visualizar mapas, sem deletar ou aprovar. analyst: tudo de field-collector + aprovar/rejeitar/solicitar-correções unidades, criar/editar qualquer unidade do tenant, gerar relatórios, exportar dados. admin: tudo de analyst + gerenciar usuários do tenant (criar, editar, atribuir roles), configurar tenant (nome, CNPJ, preferências), visualizar audit logs do tenant, gerenciar equipes. super-admin: tudo de admin + criar novos tenants, transferir usuários entre tenants, deletar tenants, acessar qualquer tenant via switcher sem validação allowed_tenants, gerenciar realm Keycloak via Admin API. Backend valida roles com `[Authorize(Roles = "analyst")]` ou `User.IsInRole("admin")` ou policies customizadas. Frontend esconde botões/rotas baseado em `user.roles.includes('admin')`. Client roles específicos do admin: manage-users (CRUD usuários), manage-tenants (CRUD tenants), view-audit-logs (visualizar logs). Composite roles: admin inclui analyst+field-collector automaticamente, super-admin inclui admin+analyst+field-collector.

---

**Última atualização:** 2026-01-09
