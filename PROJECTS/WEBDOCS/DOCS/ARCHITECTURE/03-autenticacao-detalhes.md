---
type: leaf
status: review
updated: 2026-02-07
---

# Autenticacao - Detalhes Tecnicos

Detalhes tecnicos da autenticacao WEBDOCS incluindo especificacao de cookies, validacao JWT, e fluxo de refresh token. Documento complementar a 03-autenticacao.md.

## Especificacao de Cookies

| Cookie | Conteudo | httpOnly | secure | sameSite | path | maxAge |
|--------|----------|----------|--------|----------|------|--------|
| carf_access_token | JWT access token do Keycloak | Sim | Sim | Lax | / | 300s (5 min) |
| carf_refresh_token | Refresh token do Keycloak | Sim | Sim | Lax | /auth | 28800s (8 horas) |
| carf_auth_state | JSON com code_verifier, state, redirect_to | Sim | Sim | Lax | /auth | 600s (10 min) |

### Flags de Seguranca

| Flag | Valor | Razao |
|------|-------|-------|
| httpOnly | true | Previne acesso via JavaScript, protecao contra XSS. Obrigatorio para tokens |
| secure | true | Cookie so enviado via HTTPS. Pode ser false em localhost durante desenvolvimento |
| sameSite | Lax | Enviado em navegacao top-level, nao em requests cross-site |
| path (access) | / | Access token enviado em todas requisicoes |
| path (refresh) | /auth | Refresh token so enviado para rotas /auth/ |

### Gerenciamento de Cookies

Modulo src/lib/auth/cookies.ts exporta funcoes para manipulacao dos cookies de autenticacao. Funcao setAuthCookies recebe AstroCookies, TokenResponse, e flag isProduction. Funcao clearAuthCookies deleta ambos cookies. Funcao setAuthStateCookie serializa code_verifier, state e redirect_to como JSON. Funcao getAuthState le e desserializa o cookie retornando null se invalido.

## Validacao JWT

Validacao utiliza biblioteca jose com metodo jwtVerify combinado com JWKS remoto obtido do endpoint Keycloak /realms/carf/protocol/openid-connect/certs.

| Claim extraido | Uso |
|----------------|-----|
| sub | ID do usuario |
| email | Email do usuario |
| name / preferred_username | Nome de exibicao |
| realm_access.roles | Array de roles para autorizacao |
| tenant_id | Identificador do tenant |

Cache JWKS mantido em variavel de modulo inicializado via createRemoteJWKSet. Funcao invalidateJWKSCache reseta cache apos rotacao de chaves.

## Fluxo de Refresh Token

Trigger ocorre quando access token expira (5 minutos). Middleware detecta expiracao via claim exp ou falha em jwtVerify. Sequencia: ler refresh_token do cookie, POST para Keycloak token endpoint, receber novos tokens, atualizar cookies, retry da request original.

| Cenario de falha | Tratamento |
|-------------------|------------|
| Refresh token expirado | Redirect para login |
| Refresh token revogado | Redirect para login |
| Keycloak indisponivel | Retry com backoff ou erro 503 |
