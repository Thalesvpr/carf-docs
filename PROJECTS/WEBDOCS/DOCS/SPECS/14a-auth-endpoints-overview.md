---
type: leaf
status: review
updated: 2026-02-07
---

# Endpoints de Autenticacao - Visao Geral

Especificacao dos endpoints de autenticacao do WEBDOCS que implementam fluxo OAuth2 Authorization Code com PKCE para integracao com Keycloak.

## Fluxo de Autenticacao

O fluxo segue padrao OAuth2 Authorization Code com PKCE para maxima seguranca. O usuario clica em login, GET /auth/login gera PKCE e redireciona para Keycloak. O usuario autentica no Keycloak. Keycloak redireciona para /auth/callback com code. POST para Keycloak token endpoint troca code por tokens. Tokens sao salvos em cookies HttpOnly. Usuario e redirecionado para pagina original.

## Tabela de Endpoints

| Metodo | Rota | Arquivo | Descricao |
|--------|------|---------|-----------|
| GET | /auth/login | src/pages/auth/login.astro | Inicia fluxo gerando PKCE e redirecionando para Keycloak |
| GET | /auth/callback | src/pages/auth/callback.astro | Recebe code do Keycloak e troca por tokens |
| POST | /auth/logout | src/pages/auth/logout.ts | Limpa tokens e redireciona para logout do Keycloak |
| POST | /auth/refresh | src/pages/api/refresh.ts | Renova access_token usando refresh_token |
| GET | /auth/cms | src/pages/auth/cms.astro | Proxy de autenticacao para Decap CMS acessar GitHub |

## Seguranca

Todas as comunicacoes usam HTTPS em producao. Tokens sao armazenados em cookies HttpOnly prevenindo acesso via JavaScript. Refresh token tem path restrito a /auth/ minimizando exposicao. PKCE previne ataques de interceptacao de codigo. State/nonce previne CSRF.

## Timing e Retry

| Operacao | Timeout | Retry | Backoff |
|----------|---------|-------|---------|
| Token exchange | 10000ms | sim em 5xx, max 2 | exponencial |
| Refresh | 5000ms | sim em 5xx, max 1 | - |

Erros de timeout no Keycloak mostram pagina de erro com botao retry. Erros 5xx fazem retry automatico com backoff. Erros 4xx redirecionam para login por credenciais invalidas.

Arquivos relacionados: 14b-auth-endpoints-login-callback.md, 14c-auth-endpoints-logout-refresh.md, 14d-auth-endpoints-examples.md.
