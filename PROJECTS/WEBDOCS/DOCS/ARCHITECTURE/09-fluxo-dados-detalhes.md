---
type: leaf
status: review
updated: 2026-02-07
---

# Fluxo de Dados - Autenticacao e Status

Fluxos de autenticacao OAuth2 e status page. Documento complementar a 09-fluxo-dados.md.

## Fluxo de Autenticacao

Fluxo OAuth2 Authorization Code com PKCE segue sete etapas. Login click redireciona para /auth/login salvando URL atual. PKCE generation gera code_verifier e code_challenge, salva verifier em cookie auth_state, e redireciona para Keycloak authorize endpoint. Usuario autentica no Keycloak e retorna para /auth/callback com code e state.

Token exchange valida state contra cookie, executa POST para Keycloak token endpoint, e recebe access_token e refresh_token armazenados em cookies HttpOnly. Redirect back leva usuario a URL original e deleta cookie auth_state. Requisicoes subsequentes usam middleware para ler cookie, decodificar JWT, e popular Astro.locals.user.

Token refresh dispara quando access_token expira, executa POST para /api/refresh usando refresh_token, e atualiza cookie. Se refresh falhar, redireciona para login.

## Fluxo da Status Page

Combinacao de SSR inicial com polling client-side. SSR fetch le configuracao de servicos, executa Promise.allSettled para health checks paralelos com timeout de 5 segundos, e renderiza status inicial no HTML com grid de cards, timestamp, e checkbox para auto-refresh.

Client hydration ocorre quando pagina carrega: StatusGrid hidrata com client:idle e inicializa com status do SSR. Polling loop habilitado via checkbox executa fetch a cada 30 segundos para /api/status atualizando cards sem reload.

API endpoint GET /api/status executa mesma logica de health check do SSR, retorna JSON com status de todos servicos, e usa header no-cache para dados frescos.
