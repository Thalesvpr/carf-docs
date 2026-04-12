---
type: leaf
status: review
updated: 2026-02-07
---

# Troubleshooting - Autenticacao

Resolucao de problemas de autenticacao e CORS. Arquivos relacionados: 09-troubleshooting-build.md para problemas de build e 09-troubleshooting-runtime.md para problemas de runtime.

## Login Redirect Loop

Sintoma: usuario e redirecionado infinitamente entre WEBDOCS e Keycloak, browser mostra "too many redirects", cookies nao sao persistidos.

| Causa | Verificacao | Solucao |
|---|---|---|
| Cookie nao sendo salvo | DevTools, Application, Cookies | Verificar Secure=true apenas em HTTPS; em localhost usar Secure=false; usar SameSite=Lax e nao Strict |
| Redirect URI nao cadastrada | Keycloak Admin, Clients, carf-webdocs, Valid Redirect URIs | Adicionar http://localhost:4321/auth/callback com URL exata incluindo porta |
| State mismatch | Console do browser por erro state mismatch | Limpar todos cookies do dominio; verificar cookie carf_auth_state sendo salvo; aumentar Max-Age do cookie de state |

## Token Expired Errors

Sintoma: usuario autenticado recebe 401 Unauthorized em API calls apos alguns minutos, usuario e deslogado inesperadamente.

| Solucao | Detalhes |
|---|---|
| Implementar refresh automatico | Em src/middleware.ts, verificar expiracao e chamar /auth/refresh antes de expirar |
| Aumentar token lifetime | Keycloak, Realm Settings, Tokens: Access Token Lifespan 300 segundos ou mais, SSO Session Idle 1800 segundos |
| Forcar re-login | Redirect para /auth/login quando refresh falha |

## 403 Forbidden em Secao Permitida

Sintoma: usuario com role correta recebe 403. Passos de debug: verificar roles no JWT decodificando em jwt.io, confirmar que claim realm_access.roles existe e contem role esperada, verificar mapeamento de roles no middleware, e confirmar que heranca de roles esta implementada. O payload JWT deve conter realm_access.roles com array de roles do usuario e tenant_id com UUID do tenant.

## Problemas de CORS

Sintoma: erro Access-Control-Allow-Origin no console, fetch failed com CORS policy.

| Servico | Local de Configuracao | Acao |
|---|---|---|
| Keycloak | Clients, carf-webdocs, Web Origins | Adicionar http://localhost:4321 e https://docs.carf.com.br |
| GeoAPI | appsettings.json ou Program.cs | Adicionar https://docs.carf.com.br como origem |
| Proxy alternativo | src/pages/api/proxy/[...path].ts | Usar API route do Astro como proxy para GeoAPI |
