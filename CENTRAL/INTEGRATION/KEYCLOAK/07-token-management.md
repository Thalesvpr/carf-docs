# Gerenciamento de Tokens

access_token dura 5min (300s), id_token dura 5min, refresh_token dura conforme sessão SSO (30min idle, 10h max, 24h com Remember Me). Frontend React usa `keycloak.updateToken(minValidity)` antes de cada API call: se token expira em menos de `minValidity` segundos faz refresh automático via POST /token com grant_type=refresh_token, se refresh falha redireciona pro login. Mobile armazena refresh_token em secure storage (react-native-keychain iOS, EncryptedSharedPreferences Android), checa conectividade antes de refresh, se offline usa token cacheado até expirar (max 24h), ao voltar online tenta refresh. Revogação: logout chama Keycloak `/logout` endpoint invalidando sessão SSO e refresh_token, backend pode invalidar token específico via Admin API `keycloak.Users.Logout(userId)`. Token introspection: endpoint `/token/introspect` verifica se token ativo, usado por geoapi pra validar tokens de external systems. Refresh token reuse: configurado como max reuse = 0 (uso único), cada refresh gera novo access_token + novo refresh_token invalidando o anterior, previne replay attacks. Token em URL: NUNCA passar token na query string, sempre no header Authorization: Bearer {token}, URLs podem ser logadas e expostas.

---

**Última atualização:** 2026-01-09
**Status do arquivo**: Pronto
