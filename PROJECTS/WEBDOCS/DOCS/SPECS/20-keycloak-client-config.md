---
type: leaf
status: review
updated: 2026-02-07
---

# Keycloak Client Configuration

Client carf-webdocs e public client com Authorization Code flow e PKCE.

## Client

| Propriedade | Valor |
|-------------|-------|
| clientId | carf-webdocs |
| publicClient | true |
| protocol | openid-connect |
| rootUrl | https://docs.carf.com.br |
| pkce.code.challenge.method | S256 |

Redirect URIs: localhost:4321 e docs.carf.com.br para /auth/callback e /admin. Web Origins: localhost:4321 e docs.carf.com.br.

## Tokens

| Propriedade | Valor | Descricao |
|-------------|-------|-----------|
| accessTokenLifespan | 300 | 5 minutos |
| refreshTokenLifespan | 28800 | 8 horas |
| ssoSessionIdleTimeout | 1800 | 30 minutos inatividade |
| ssoSessionMaxLifespan | 28800 | 8 horas maximo |

## Scopes e Mappers

Default scopes: openid (sub claim), profile (nome/username), email, roles (RBAC). Opcional: offline_access. Mapper realm roles inclui realm_access.roles nos tokens. Mapper tenant_id inclui atributo tenant_id.

## Endpoints

| Endpoint | Path |
|----------|------|
| authorization | /realms/carf/protocol/openid-connect/auth |
| token | /realms/carf/protocol/openid-connect/token |
| userinfo | /realms/carf/protocol/openid-connect/userinfo |
| logout | /realms/carf/protocol/openid-connect/logout |
| jwks | /realms/carf/protocol/openid-connect/certs |

Base URL: https://auth.carf.com.br

## Troubleshooting

| Erro | Solucao |
|------|---------|
| invalid_redirect_uri | Adicionar URI exata nas redirectUris |
| invalid_client | Verificar clientId e enabled |
| cors_error | Adicionar origin nas webOrigins |
| pkce_required | Implementar PKCE conforme SPECS/21a-pkce-overview.md |
