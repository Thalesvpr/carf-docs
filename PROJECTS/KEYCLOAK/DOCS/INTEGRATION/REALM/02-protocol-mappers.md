---
type: leaf
status: review
updated: 2026-01-19
---

# Protocol Mappers

Protocol mappers configuram extração de dados do usuário Keycloak para claims JWT permitindo backend e frontend acessarem informações customizadas sem consultas adicionais.

Mapper tenant_id utiliza tipo oidc-usermodel-attribute-mapper extraindo user attribute current_tenant para claim tenant_id tipo String incluído em id_token, access_token e userinfo endpoint. Este claim identifica o tenant atualmente selecionado pelo usuário e é usado pelo middleware backend para configurar Row Level Security no PostgreSQL.

Mapper allowed_tenants utiliza mesmo tipo extraindo user attribute tenants (multivalued) para claim allowed_tenants tipo JSON contendo array de UUIDs de todos tenants aos quais usuário tem permissão de acesso. Frontend usa este claim para renderizar dropdown de troca de tenant e validar operações antes de chamar backend.

Mapper roles inclui realm roles e client roles no token automaticamente através de configuração padrão do Keycloak. Claim roles contém array com roles do usuário como field-cadastrator, field-coordinator, analyst, manager, admin, super-admin, dev permitindo autorização granular no backend via [Authorize(Roles)] e no frontend via user.roles.includes().

Configuração no Admin Console: Client Scopes → carf-tenant → Mappers → Add mapper → User Attribute, preencher Token Claim Name, User Attribute, Claim JSON Type, e marcar checkboxes Add to ID token, Add to access token, Add to userinfo.
