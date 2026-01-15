# Error Codes

Códigos erro OAuth2/OIDC retornados em responses seguindo RFC 6749. invalid_request indica request malformado faltando parâmetros obrigatórios como client_id redirect_uri ou formato inválido, ação validar payload. invalid_client falha autenticação client por client_id inexistente ou client_secret incorreto, ação verificar credenciais. invalid_grant indica authorization code ou refresh token inválido expirado ou já usado, ação re-autenticar usuário. unauthorized_client client não autorizado para grant_type solicitado como client credentials em client público, ação verificar configuração client. unsupported_grant_type grant type não suportado ou não habilitado no client, ação habilitar grant type desejado. invalid_scope scope solicitado não existe ou não permitido para client, ação verificar scopes configurados. access_denied usuário negou consentimento ou cancelou fluxo autorização, ação informar usuário. HTTP status codes 200 success, 400 bad request validar input, 401 unauthorized token inválido expirado fazer refresh, 403 forbidden sem permissão verificar roles, 404 not found recurso inexistente, 409 conflict username email duplicado, 429 too many requests rate limit implementar backoff exponencial, 500 internal error verificar logs server, 503 unavailable server down ou overloaded retry com backoff.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
