---
type: leaf
status: review
updated: 2026-02-07
---

# Endpoints de Autenticacao - Exemplos

Exemplos de request/response dos endpoints de autenticacao. Relacionado com 14a-auth-endpoints-overview.md.

## Login

GET /auth/login?redirect=/dev/middleware retorna 302 para Keycloak authorization endpoint com client_id, redirect_uri, response_type code, scope, code_challenge e state. Set-Cookie carf_auth_state com JSON contendo code_verifier, state, redirect_to e created_at (HttpOnly, Secure, SameSite Lax, Path /auth, Max-Age 600).

## Callback

Keycloak redireciona para /auth/callback?code=SplxlOBeZQQYbYS6WxSbIA&state=af0ifjsldkj com cookie carf_auth_state. Servidor faz POST server-to-server para token endpoint com grant_type, client_id, code, redirect_uri e code_verifier em x-www-form-urlencoded.

Keycloak responde com access_token JWT (expires_in 300), refresh_token (refresh_expires_in 28800), token_type Bearer, id_token e scope. Servidor retorna 302 para pagina original com Set-Cookie para access_token (Path /, Max-Age 300), refresh_token (Path /auth, Max-Age 28800) e deleta auth_state (Max-Age 0). State mismatch retorna 302 para /auth/login?error=state_mismatch.

## Refresh

POST /auth/refresh com cookie carf_refresh_token. Sucesso: 200 com success true e expiresIn, atualiza ambos cookies. Erros: 401 com no_refresh_token ou refresh_token_expired para login novamente.

## Logout

POST /auth/logout retorna 302 para Keycloak logout endpoint com client_id e post_logout_redirect_uri. Deleta ambos cookies com Max-Age 0.
