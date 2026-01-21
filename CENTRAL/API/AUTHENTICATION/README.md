---
status: rejected
description: "Stub incompleto. Spec de API deve ter request/response schemas, exemplos, erros. Mover implementacao para PROJECTS/GEOAPI."
updated: 2026-01-15
---

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


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-login](./01-login.md) | Login |
| [02-refresh-token](./02-refresh-token.md) | Refresh Token |
| [03-logout](./03-logout.md) | Logout |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/API/AUTHENTICATION/01-login.md|Login]]
- ○ [[CENTRAL/API/AUTHENTICATION/02-refresh-token.md|Refresh Token]]
- ○ [[CENTRAL/API/AUTHENTICATION/03-logout.md|Logout]]

<!-- CARF-INDEX-END -->
