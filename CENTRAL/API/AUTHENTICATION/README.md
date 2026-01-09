# AUTHENTICATION

Schemas JSON para autenticação do CARF via Keycloak OIDC. LoginRequest (username/email, password, tenant_id opcional para seleção de município), LoginResponse (access_token JWT, refresh_token, expires_in, token_type bearer, user profile com id/name/email/roles), RefreshTokenRequest (refresh_token), RefreshTokenResponse (novo access_token), LogoutRequest (refresh_token para invalidar), ValidateTokenRequest (token JWT para verificação server-side), ValidateTokenResponse (valid boolean, claims decodificados, expiration). Tokens JWT contém claims: sub (user id), email, name, roles array, tenant_id, iat (issued at), exp (expiration). Headers obrigatórios: Authorization Bearer {token}, X-Tenant-ID para multi-tenancy. Códigos HTTP: 200 OK sucesso, 401 Unauthorized credenciais inválidas, 403 Forbidden sem permissão no tenant, 422 Unprocessable Entity validação falhou.

---

**Última atualização:** 2025-12-29
