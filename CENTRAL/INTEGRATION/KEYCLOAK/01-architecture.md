# Arquitetura de Autenticação Keycloak

Sistema CARF usa Keycloak como provedor OAuth2/OIDC centralizado para 6 aplicações (GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS, ADMIN) com SSO automático entre todas, fluxo Authorization Code + PKCE para SPAs/mobile garantindo segurança sem client secret, Client Credentials para backend-to-backend (plugin QGIS), e Bearer token validation no backend .NET com JWT contendo claims `tenant_id` e `allowed_tenants` que são extraídos e setados como `app.tenant_id` no PostgreSQL para RLS funcionar automaticamente filtrando dados por tenant.

## OAuth2/OIDC

OAuth2 = autorização (o que pode fazer), OpenID Connect = autenticação (quem é) estendendo OAuth2 com id_token. Fluxo: usuário acessa GEOWEB → redireciona pra Keycloak login → usuário loga → Keycloak retorna `code` → GEOWEB troca `code` por tokens (POST /token com `code_verifier` pra PKCE) → recebe `access_token` (API calls), `id_token` (info usuário), `refresh_token` (renovar) → usa `access_token` no header `Authorization: Bearer {token}` pra chamar GEOAPI → GEOAPI valida JWT (assinatura, exp, iss) e extrai claims → seta tenant no RLS → responde.

## SSO (Single Sign-On)

Login em GEOWEB cria sessão Keycloak via cookie → acessar REURBCAD detecta cookie → já logado automaticamente sem pedir credenciais de novo → logout em qualquer app desloga de todos (Single Logout) invalidando sessão Keycloak. Timeout: 30min idle, 10h max, 24h com Remember Me.

## Multi-Tenancy

1 realm "carf" + atributo `tenants: ["prefeitura-a", "prefeitura-b"]` no usuário + `current_tenant: "prefeitura-a"` → protocol mapper converte pra JWT claims `tenant_id` (atual) e `allowed_tenants` (autorizados) → frontend renderiza dropdown só se `allowed_tenants.length > 1` → troca chama `/api/auth/switch-tenant` → backend valida se novo tenant está em `allowed_tenants` → atualiza `current_tenant` via Keycloak Admin API → frontend faz `keycloak.updateToken(5)` pegando novo token com `tenant_id` atualizado → reload da página → middleware backend extrai `tenant_id` do JWT e seta `SET LOCAL app.tenant_id = '{tenant_id}'` no PostgreSQL → RLS policy `WHERE tenant_id = current_setting('app.tenant_id')::uuid` filtra tudo automaticamente.

## Integração PostgreSQL RLS

Middleware .NET extrai claim `tenant_id` do JWT e executa `db.Database.ExecuteSqlRawAsync("SET LOCAL app.tenant_id = {0}", tenantId)` no início de cada request. Todas as tabelas tem policy `CREATE POLICY tenant_isolation ON {table} USING (tenant_id = current_setting('app.tenant_id', true)::uuid)` garantindo que mesmo com SQL injection ou bug na aplicação é impossível acessar dados de outro tenant porque o PostgreSQL filtra na camada de banco.

## Fluxos

PKCE (SPAs/mobile): gera `code_verifier` random → calcula `code_challenge = SHA256(code_verifier)` → GET /auth com `code_challenge` → login → retorna `code` → POST /token com `code + code_verifier` → Keycloak valida que SHA256(code_verifier) == code_challenge salvo → retorna tokens. Client Credentials (QGIS): POST /token com `client_id + client_secret + grant_type=client_credentials` → retorna `access_token` sem user context. Bearer Validation (GEOAPI): extrai token do header `Authorization: Bearer {token}` → valida assinatura usando public key do Keycloak (JWKS endpoint) → valida `exp`, `iss`, `aud` → extrai claims → autoriza request baseado em `roles`.

---

**Última atualização:** 2026-01-09
