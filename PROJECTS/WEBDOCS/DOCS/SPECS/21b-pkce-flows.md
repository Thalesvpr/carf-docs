---
type: leaf
status: review
updated: 2026-02-07
---

# PKCE Implementation - Fluxos

Fluxos completos de login e callback com PKCE. Relacionado com 21a-pkce-overview.md e 21c-pkce-security.md.

## Fluxo Login

GET /auth/login com query param redirect (opcional, default /). Passos: gerar code_verifier 64 chars, gerar code_challenge SHA256 base64url, gerar state 32 bytes hex, salvar em cookie carf_auth_state, redirecionar para Keycloak.

| Parametro Keycloak | Valor |
|--------------------|-------|
| client_id | carf-webdocs |
| redirect_uri | https://docs.carf.com.br/auth/callback |
| response_type | code |
| scope | openid profile email |
| code_challenge_method | S256 |

## Fluxo Callback

GET /auth/callback com code e state. Passos: ler cookie verificando expiracao, validar state, trocar code por tokens via POST ao token endpoint com code e code_verifier, salvar tokens em cookies, deletar state cookie, redirecionar para URL original.

## Token Exchange

POST ao token endpoint com Content-Type x-www-form-urlencoded: grant_type authorization_code, client_id, code, redirect_uri, code_verifier.

Resposta: access_token JWT, expires_in 300, refresh_expires_in 28800, refresh_token, token_type Bearer, id_token, scope openid profile email.

## Timing

| Recurso | Duracao | Motivo |
|---------|---------|--------|
| auth_state_cookie | 600s | 10min para completar login |
| code_validity | 60s | 1min para trocar por tokens |
| access_token | 300s | 5min, curto para seguranca |
| refresh_token | 28800s | 8h, sessao de trabalho |
