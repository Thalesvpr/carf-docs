---
type: leaf
status: review
updated: 2026-02-07
---

# Autenticacao

WEBDOCS integra com Keycloak para autenticacao de usuarios que acessam secao protegida /dev/ e CMS administrativo. Client carf-webdocs configurado como public client usa Authorization Code flow com PKCE.

Fluxo de login inicia quando usuario nao autenticado acessa rota protegida. Middleware redireciona para Keycloak /authorize com parametros client_id, redirect_uri apontando para /auth/callback, response_type code, code_challenge gerado com S256, e state para protecao CSRF.

Callback em /auth/callback.astro processa response do Keycloak. Codigo de autorizacao e trocado por tokens via POST /token incluindo code_verifier do PKCE. Access token e refresh token sao armazenados em cookie HTTP-only com flags Secure e SameSite Strict.

Sessao e mantida via cookie carf-session contendo tokens criptografados. Cookie HTTP-only previne acesso via JavaScript protegendo contra XSS. Expiracao do cookie alinhada com refresh token (30 minutos idle, 8 horas max).

Refresh silencioso acontece quando access token expira (5 minutos). Middleware detecta token expirado, executa refresh via POST /token com grant_type refresh_token, e atualiza cookies com novos tokens. Processo transparente para usuario.

Logout em /auth/logout invalida sessao local deletando cookies e redireciona para Keycloak /logout com post_logout_redirect_uri. Logout completo do SSO invalida sessao em todas aplicacoes CARF.

Decap CMS usa mesmo fluxo OAuth com redirect para /admin/callback. Apos autenticacao, CMS recebe token para autenticar chamadas a GitHub API permitindo commits de edicoes.

Detalhes de cookies, validacao JWT e refresh flow estao documentados em 03-autenticacao-detalhes.md.
