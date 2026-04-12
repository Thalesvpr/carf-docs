---
type: leaf
status: review
updated: 2026-02-07
---

# Integração com Keycloak

WEBDOCS integra com Keycloak para autenticação de usuários que acessam seção protegida /dev/. Client `webdocs` configurado como public client usa Authorization Code flow com PKCE para obter tokens JWT sem expor client secret.

Fluxo de autenticação inicia quando usuário acessa rota /dev/*. Middleware SSR verifica presença de cookie de sessão. Se ausente, redireciona para Keycloak /authorize endpoint com parâmetros client_id, redirect_uri, response_type=code, code_challenge (PKCE), scope=openid profile, e state para proteção CSRF.

Callback em /auth/callback recebe authorization code, troca por tokens via POST /token endpoint, valida id_token verificando assinatura e claims, extrai role dev do claim realm_access.roles, e cria cookie de sessão HTTP-only com access_token para requisições subsequentes.

Middleware de autorização em rotas /dev/* extrai token do cookie, valida expiração, e verifica presença de role dev no array de roles. Ausência de role resulta em página 403 explicando que acesso requer permissão de desenvolvedor. Token expirado dispara refresh silencioso usando refresh_token armazenado.

Logout em /auth/logout invalida sessão local deletando cookie e redireciona para Keycloak /logout endpoint com post_logout_redirect_uri para garantir logout completo do SSO.
