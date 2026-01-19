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

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-login](./01-login.md) | Login |
| [02-refresh-token](./02-refresh-token.md) | Refresh Token |
| [03-logout](./03-logout.md) | Logout |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->
