# Account

Entidade representando usuário sistema vinculado Tenant específico sincronizado Keycloak autenticação OAuth2/OIDC armazenando perfil preferências relacionamentos internos. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem TenantId Guid FK isolando via RLS, ExternalId UUID Keycloak sincronização bidirecional, Name nome completo, Email único por tenant para login, PhoneNumber opcional contato e Role definindo permissões SUPER_ADMIN/ADMIN/MANAGER/ANALYST/FIELD_AGENT.

Campos adicionais incluem ProfilePhoto URL S3 ou Gravatar, Preferences JSON configurações UI tema idioma timezone, IsActive bool desabilitando acesso sem deletar e LastLoginAt DateTime rastreando último acesso. Relacionamentos incluem TeamMember vinculando Account Teams, CommunityAuthorization acessos individuais comunidades, Session sessões ativas e ApiKey chaves API scripts.

Métodos negócio incluem Activate()/Deactivate() controlando IsActive, UpdatePreferences(json) validando estrutura JSON, UpdateProfile(name phone photo) validações e HasAccessToCommunity(communityId) verificando acesso direto ou via Team hierarquia permissões. Sincronizado Keycloak onde criação/atualização dispara webhook mantendo email nome roles consistentes sistemas.

---

**Última atualização:** 2026-01-12
