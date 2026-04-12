---
type: leaf
status: review
updated: 2026-02-07
---

# Endpoints de Autenticacao - Login e Callback

Detalhamento de GET /auth/login e GET /auth/callback. Relacionado com 14a-auth-endpoints-overview.md.

## GET /auth/login

Arquivo src/pages/auth/login.astro. Query param redirect (opcional, default /) como path relativo do mesmo dominio.

Comportamento: gera PKCE com code_verifier (43-128 chars), code_challenge (SHA256 base64url) e metodo S256. Salva state no cookie carf_auth_state com code_verifier, redirect e state aleatorio (httpOnly, secure, sameSite lax, maxAge 600, path /auth). Redireciona para authorization endpoint do Keycloak com client_id, redirect_uri, response_type code, scope openid profile email, code_challenge e state.

Sucesso: 302 para Keycloak. Erro: 500 se falha no PKCE.

## GET /auth/callback

Arquivo src/pages/auth/callback.astro.

| Query Param | Obrigatorio | Descricao |
|-------------|-------------|-----------|
| code | sim | Authorization code |
| state | sim | Nonce CSRF |
| error | nao | Codigo de erro |
| error_description | nao | Descricao do erro |

Comportamento: valida state do cookie contra query param (erro redireciona para /auth/login). Verifica error param. Troca code por tokens via POST ao token endpoint como public client com PKCE, enviando grant_type, client_id, code, redirect_uri e code_verifier.

Tokens salvos: access_token em carf_access_token (path /, maxAge expires_in), refresh_token em carf_refresh_token (path /auth, maxAge refresh_expires_in). Ambos httpOnly, secure, sameSite lax.

Deleta carf_auth_state e redireciona para URL original. Sucesso: 302. Erro state: 302 para login. Erro exchange: pagina de erro com retry.
