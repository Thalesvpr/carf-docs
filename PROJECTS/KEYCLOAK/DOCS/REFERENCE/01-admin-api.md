---
type: leaf
status: review
updated: 2026-02-07
---

# Admin REST API

Keycloak Admin REST API permite gerenciamento programatico de realms, usuarios, roles, clients e configuracoes. A base URL para o realm CARF e /admin/realms/carf. Autenticacao exige Bearer token obtido via admin-cli client credentials flow ou token de usuario com role realm-admin.

## Autenticacao

Para obter um token admin, envia-se requisicao POST ao endpoint /realms/master/protocol/openid-connect/token com content type application/x-www-form-urlencoded. O body contem client_id igual a admin-cli, username e password do administrador, e grant_type igual a password. A resposta retorna access_token, expires_in, refresh_expires_in, refresh_token e token_type Bearer. Todas requisicoes subsequentes devem incluir headers Authorization Bearer com o token e Content-Type application/json.

## Endpoints de Realm

| Metodo | Endpoint | Descricao |
|:-------|:---------|:----------|
| GET | /admin/realms/{realm} | Retorna configuracao completa do realm |
| PUT | /admin/realms/{realm} | Atualiza configuracoes do realm |

A resposta do GET retorna campos como id, realm, displayName, enabled, sslRequired, registrationAllowed, loginWithEmailAllowed, resetPasswordAllowed, bruteForceProtected, failureFactor, accessTokenLifespan, ssoSessionIdleTimeout, loginTheme, internationalizationEnabled, supportedLocales e defaultLocale. O PUT aceita body parcial com apenas os campos a alterar.

## Boas Praticas

Paginacao e obrigatoria para listagens grandes, usando parametros first e max para evitar timeout. Implementar backoff exponencial para chamadas em lote pois Keycloak nao possui rate limiting nativo. Admin tokens expiram rapidamente (300s padrao), exigindo cache e refresh antes da expiracao. Todas operacoes admin sao registradas em log de auditoria consultavel via /admin/realms/{realm}/events.

Ver [01a-admin-api-users](./01a-admin-api-users.md) para endpoints de usuarios e [01b-admin-api-roles-clients](./01b-admin-api-roles-clients.md) para roles, clients, groups e sessoes.
