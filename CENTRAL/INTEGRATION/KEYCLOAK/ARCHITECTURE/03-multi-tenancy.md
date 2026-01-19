# Multi-Tenancy Dinâmico

Estratégia utiliza realm único "carf" com atributos de usuário para suportar múltiplos municípios sem necessidade de realms separados. User attribute tenants armazena array JSON de tenant IDs aos quais usuário tem acesso como ["prefeitura-a", "prefeitura-b"] e current_tenant indica tenant atualmente selecionado. Protocol mappers convertem atributos para JWT claims tenant_id e allowed_tenants incluídos em access_token e id_token.

Frontend React renderiza TenantSwitcher dropdown somente se allowed_tenants contém mais de um tenant. Usuário seleciona novo tenant acionando POST para /api/auth/switch-tenant no backend que valida se tenant solicitado está em allowed_tenants do token atual prevenindo privilege escalation, atualiza current_tenant via Keycloak Admin API, e retorna success. Frontend força refresh do token via keycloak.updateToken obtendo novo access_token com tenant_id atualizado e recarrega página.

Middleware TenantMiddleware no backend .NET extrai claim tenant_id do JWT validado e executa SET LOCAL app.tenant_id configurando variável de sessão PostgreSQL específica para conexão atual. Todas tabelas possuem Row Level Security policies definidas como USING (tenant_id = current_setting('app.tenant_id', true)::uuid) filtrando automaticamente queries SELECT UPDATE DELETE permitindo acesso apenas a rows do tenant correto.

Alternativas rejeitadas incluem realm por tenant que não escala e quebra SSO entre tenants, e grupos Keycloak que limitam usuário a um grupo impossibilitando consultores multi-tenant. Casos de uso suportados: analista single-tenant não vê dropdown, consultor multi-tenant troca livremente entre tenants autorizados, super-admin acessa qualquer tenant via endpoint especial sem validação allowed_tenants.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review
