---
status: review
updated: 2026-01-17
---

# Autenticação

WEBDOCS integra com Keycloak para autenticação de usuários que acessam seção protegida /dev/ e CMS administrativo. Client carf-webdocs configurado como public client usa Authorization Code flow com PKCE.

Fluxo de login inicia quando usuário não autenticado acessa rota protegida. Middleware redireciona para Keycloak /authorize com parâmetros client_id, redirect_uri apontando para /auth/callback, response_type code, code_challenge gerado com S256, e state para proteção CSRF.

Callback em /auth/callback.astro processa response do Keycloak. Código de autorização é trocado por tokens via POST /token incluindo code_verifier do PKCE. Access token e refresh token são armazenados em cookie HTTP-only com flags Secure e SameSite Strict.

Sessão é mantida via cookie carf-session contendo tokens criptografados. Cookie HTTP-only previne acesso via JavaScript protegendo contra XSS. Expiração do cookie alinhada com refresh token (30 minutos idle, 8 horas max).

Refresh silencioso acontece quando access token expira (5 minutos). Middleware detecta token expirado, executa refresh via POST /token com grant_type refresh_token, e atualiza cookies com novos tokens. Processo transparente para usuário.

Logout em /auth/logout invalida sessão local deletando cookies e redireciona para Keycloak /logout com post_logout_redirect_uri. Logout completo do SSO invalida sessão em todas aplicações CARF.

Decap CMS usa mesmo fluxo OAuth com redirect para /admin/callback. Após autenticação, CMS recebe token para autenticar chamadas à GitHub API permitindo commits de edições.
