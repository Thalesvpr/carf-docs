# AUTHENTICATION

Schemas JSON para autenticação do CARF via Keycloak OIDC.

O LoginRequest contém username ou email, password e tenant_id opcional para seleção de município. O LoginResponse retorna access_token JWT, refresh_token, expires_in e profile do usuário com id, name, email e roles.

Os tokens JWT contêm claims: sub (user id), email, name, roles array, tenant_id, iat (issued at) e exp (expiration).

Headers obrigatórios: Authorization Bearer {token} e X-Tenant-ID para multi-tenancy.

Códigos HTTP: 200 OK sucesso, 401 Unauthorized credenciais inválidas, 403 Forbidden sem permissão no tenant, 422 Unprocessable Entity validação falhou.

## Schemas

- LoginRequest / LoginResponse
- RefreshTokenRequest / RefreshTokenResponse
- LogoutRequest
- ValidateTokenRequest / ValidateTokenResponse

---

**Última atualização:** 2026-01-14
