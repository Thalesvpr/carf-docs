---
type: leaf
status: review
updated: 2026-02-07
---

# Keycloak Integration

GEOAPI integra com Keycloak como client bearer-only, o que significa que nao autentica usuarios diretamente nem emite tokens. Recebe tokens JWT emitidos por outros clients (reurbweb, reurbcad, admin) e valida assinatura, lifetime e claims antes de processar cada requisicao. O client ID no Keycloak e `geoapi`, configurado sem secret (bearer-only nao precisa) com Authority apontando para `https://keycloak.carf.com.br/realms/carf` e Audience `geoapi`.

A configuracao .NET usa `AddAuthentication(JwtBearerDefaults.AuthenticationScheme).AddJwtBearer()` com `ValidateIssuer`, `ValidateAudience` e `ValidateLifetime` todos habilitados e `ClockSkew = TimeSpan.Zero` para validacao estrita de expiracao. O middleware automaticamente busca as chaves publicas do Keycloak via endpoint JWKS (`/protocol/openid-connect/certs`) e verifica assinatura RS256 do token. Se o token for invalido, expirado ou com audience errada, retorna 401 Unauthorized sem processar o request.

TenantContext extrai claims do JWT autenticado via `IHttpContextAccessor`. As tres claims customizadas do scope `carf-tenant` sao: `tenant_id` (Guid do municipio atual do usuario), `allowed_tenants` (array JSON de Guids dos municipios permitidos) e `community_ids` (array JSON de Guids das comunidades associadas). Alem dessas, extrai `sub` (UserId), `email`, `preferred_username` e `realm_access.roles` (array de roles como field-cadastrator, analyst, admin). O TenantMiddleware usa o `tenant_id` extraido para executar `SET LOCAL app.tenant_id = '{tenantId}'` no PostgreSQL, ativando Row Level Security que filtra automaticamente todos os dados pelo municipio correto.

Autorizacao por role usa `[Authorize(Roles = "admin,super-admin")]` nos controllers .NET, que valida contra o array `realm_access.roles` do token. Client roles especificas do client `admin` (manage-users, manage-tenants, view-audit-logs) sao verificadas via `resource_access.admin.roles` para endpoints de administracao.

GEOAPI tambem atua como proxy seguro para a Keycloak Admin REST API, permitindo que o sistema REURBMASTER (SPA publica, sem secrets) gerencie usuarios, roles e tenants via endpoints `/api/admin/*`. O GEOAPI valida que o usuario tem role admin ou superior, e entao faz chamadas a Admin API do Keycloak usando credenciais de servico configuradas no backend (separadas do client bearer-only).
