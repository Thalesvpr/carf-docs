# AUTHENTICATION

Schemas JSON para autenticação do CARF via Keycloak OIDC. LoginRequest (username/email, password, tenant_id opcional para seleção de município), LoginResponse (access_token JWT, refresh_token, expires_in, token_type bearer, user profile com id/name/email/roles), RefreshTokenRequest (refresh_token), RefreshTokenResponse (novo access_token), LogoutRequest (refresh_token para invalidar), ValidateTokenRequest (token JWT para verificação server-side), ValidateTokenResponse (valid boolean, claims decodificados, expiration). Tokens JWT contém claims: sub (user id), email, name, roles array, tenant_id, iat (issued at), exp (expiration). Headers obrigatórios: Authorization Bearer {token}, X-Tenant-ID para multi-tenancy. Códigos HTTP: 200 OK sucesso, 401 Unauthorized credenciais inválidas, 403 Forbidden sem permissão no tenant, 422 Unprocessable Entity validação falhou.

## Implementação e Uso

Autenticação implementada via Keycloak conforme [ADR-003: Keycloak Autenticação](../../ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md) usando OAuth2 + PKCE flow documentado em [CENTRAL/INTEGRATION/KEYCLOAK/07-token-management.md](../../INTEGRATION/KEYCLOAK/07-token-management.md) onde client-side inicia authorization code flow com code_challenge PKCE redirecionando para Keycloak login obtendo authorization code e trocando por access_token + refresh_token, integração client-side via reutilizado pelos frontends GEOWEB portal web, REURBCAD mobile app e ADMIN console administrativo, backend GEOAPI valida tokens JWT recebidos via Authorization header com middleware ASP.NET Core verificando assinatura RSA usando public key do Keycloak realm e extraindo claims user_id tenant_id roles para authorização.

---

**Última atualização:** 2025-12-29
