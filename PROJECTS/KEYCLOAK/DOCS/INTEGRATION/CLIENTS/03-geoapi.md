---
type: leaf
status: review
updated: 2026-01-19
---

# Client GEOAPI

Backend .NET API REST configurado como bearer-only client que apenas valida tokens JWT sem gerar novos, apropriado para APIs que recebem tokens de frontends.

Não possui redirect URIs ou web origins pois não participa de fluxos interativos de login. Validação de tokens utiliza public key do Keycloak obtida via JWKS endpoint (/.well-known/openid-configuration → jwks_uri) com cache de 24 horas renovando automaticamente em caso de key rotation.

Configuração ASP.NET Core usa AddJwtBearer com TokenValidationParameters especificando ValidateIssuerSigningKey true, ValidIssuer como URL do realm, ValidAudience opcional, ValidateLifetime true com ClockSkew de 5 minutos tolerando pequena diferença de relógio entre servidores.

Middleware TenantMiddleware executa após autenticação extraindo claim tenant_id do token validado e configurando SET LOCAL app.tenant_id no PostgreSQL para Row Level Security. Controllers acessam claims via User.FindFirst("tenant_id") ou [Authorize(Roles = "analyst")] para autorização baseada em roles.
