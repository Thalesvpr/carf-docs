---
status: review
updated: 2026-01-21
---

# OpenID Connect Endpoints

OIDC endpoints do realm CARF seguindo especificação OpenID Connect Core 1.0. Base URL: `https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect`.

## Discovery Document

### GET /.well-known/openid-configuration

Retorna metadados do provedor OIDC com todos endpoints e capabilities suportadas.

```bash
curl -X GET "https://keycloak.carf.gov.br/realms/carf/.well-known/openid-configuration"
```

**Response:**
```json
{
  "issuer": "https://keycloak.carf.gov.br/realms/carf",
  "authorization_endpoint": "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/auth",
  "token_endpoint": "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/token",
  "userinfo_endpoint": "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/userinfo",
  "end_session_endpoint": "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/logout",
  "jwks_uri": "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/certs",
  "introspection_endpoint": "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/token/introspect",
  "revocation_endpoint": "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/revoke",
  "grant_types_supported": [
    "authorization_code",
    "refresh_token",
    "client_credentials"
  ],
  "response_types_supported": [
    "code",
    "token",
    "id_token",
    "code token",
    "code id_token"
  ],
  "scopes_supported": [
    "openid",
    "profile",
    "email",
    "roles",
    "tenants"
  ],
  "code_challenge_methods_supported": [
    "plain",
    "S256"
  ]
}
```

## Authorization Endpoint

### GET /protocol/openid-connect/auth

Inicia fluxo OAuth2 Authorization Code. Usuário é redirecionado para tela de login.

**Query Parameters:**

| Param | Obrigatório | Descrição |
|:------|:------------|:----------|
| `response_type` | Sim | `code` para Authorization Code flow |
| `client_id` | Sim | ID do client registrado |
| `redirect_uri` | Sim | URI de callback (deve estar em redirectUris do client) |
| `scope` | Sim | Scopes separados por espaço |
| `state` | Recomendado | Valor opaco para proteção CSRF |
| `code_challenge` | PKCE | Challenge gerado para PKCE |
| `code_challenge_method` | PKCE | `S256` (recomendado) ou `plain` |
| `nonce` | OpenID | Valor para prevenir replay attacks |
| `prompt` | Opcional | `login`, `consent`, `none` |
| `login_hint` | Opcional | Pre-fill do campo username |
| `ui_locales` | Opcional | Idioma preferido (pt-BR, en) |

**Exemplo - Authorization Code com PKCE:**

```
https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/auth?
  response_type=code&
  client_id=geoweb&
  redirect_uri=https://geoweb.carf.gov.br/callback&
  scope=openid%20profile%20email%20tenants&
  state=abc123xyz&
  code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&
  code_challenge_method=S256&
  nonce=n-0S6_WzA2Mj
```

**Redirect após autenticação bem-sucedida:**

```
https://geoweb.carf.gov.br/callback?
  code=eyJhbGciOiJkaXIiLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0...&
  state=abc123xyz
```

**Redirect após erro:**

```
https://geoweb.carf.gov.br/callback?
  error=access_denied&
  error_description=User%20denied%20consent&
  state=abc123xyz
```

## Token Endpoint

### POST /protocol/openid-connect/token

Troca authorization code por tokens ou obtém tokens via outros grants.

**Headers:**
```http
Content-Type: application/x-www-form-urlencoded
```

### Authorization Code Grant

```bash
curl -X POST "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code" \
  -d "code=eyJhbGciOiJkaXIi..." \
  -d "redirect_uri=https://geoweb.carf.gov.br/callback" \
  -d "client_id=geoweb" \
  -d "code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "not-before-policy": 0,
  "session_state": "session-uuid",
  "scope": "openid profile email tenants"
}
```

### Refresh Token Grant

```bash
curl -X POST "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=eyJhbGciOiJIUzI1NiIs..." \
  -d "client_id=geoweb"
```

### Client Credentials Grant

Para service-to-service authentication (clients confidenciais).

```bash
curl -X POST "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=geoapi" \
  -d "client_secret=client-secret-here"
```

## UserInfo Endpoint

### GET /protocol/openid-connect/userinfo

Retorna claims do usuário autenticado.

```bash
curl -X GET "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/userinfo" \
  -H "Authorization: Bearer <access_token>"
```

**Response:**
```json
{
  "sub": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "email_verified": true,
  "name": "João Silva",
  "preferred_username": "52998224725",
  "given_name": "João",
  "family_name": "Silva",
  "email": "joao.silva@email.com",
  "tenants": ["tenant-001", "tenant-002"],
  "current_tenant": "tenant-001",
  "realm_access": {
    "roles": ["analyst", "field-agent"]
  }
}
```

## JWKS Endpoint

### GET /protocol/openid-connect/certs

Retorna public keys RSA para validação de assinatura JWT.

```bash
curl -X GET "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/certs"
```

**Response:**
```json
{
  "keys": [
    {
      "kid": "key-id-001",
      "kty": "RSA",
      "alg": "RS256",
      "use": "sig",
      "n": "modulus-base64url",
      "e": "AQAB"
    }
  ]
}
```

**Uso em verificação JWT (Node.js):**

```typescript
import jwt from 'jsonwebtoken'
import jwksClient from 'jwks-rsa'

const client = jwksClient({
  jwksUri: 'https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/certs',
  cache: true,
  cacheMaxAge: 600000, // 10 minutos
})

function getKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    callback(err, key?.getPublicKey())
  })
}

jwt.verify(token, getKey, { algorithms: ['RS256'] }, (err, decoded) => {
  if (err) throw err
  console.log(decoded)
})
```

## Logout Endpoint

### GET /protocol/openid-connect/logout

Encerra sessão SSO. Redireciona para post_logout_redirect_uri se fornecido.

**Query Parameters:**

| Param | Descrição |
|:------|:----------|
| `id_token_hint` | ID token para identificar sessão |
| `post_logout_redirect_uri` | URI para redirect após logout |
| `state` | Valor opaco retornado no redirect |

```
https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/logout?
  id_token_hint=eyJhbGciOiJSUzI1NiIs...&
  post_logout_redirect_uri=https://geoweb.carf.gov.br&
  state=logout-state-123
```

**Back-channel logout (RP-Initiated):**

```bash
curl -X POST "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/logout" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=geoweb" \
  -d "refresh_token=eyJhbGciOiJIUzI1NiIs..."
```

## Introspection Endpoint

### POST /protocol/openid-connect/token/introspect

Valida token e retorna claims. Requer autenticação do client.

```bash
curl -X POST "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/token/introspect" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "token=eyJhbGciOiJSUzI1NiIs..." \
  -d "token_type_hint=access_token" \
  -d "client_id=geoapi" \
  -d "client_secret=client-secret-here"
```

**Response (token válido):**
```json
{
  "active": true,
  "sub": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "email_verified": true,
  "preferred_username": "52998224725",
  "given_name": "João",
  "family_name": "Silva",
  "realm_access": {
    "roles": ["analyst"]
  },
  "resource_access": {
    "geoweb": {
      "roles": ["viewer", "editor"]
    }
  },
  "scope": "openid profile email tenants",
  "client_id": "geoweb",
  "token_type": "Bearer",
  "exp": 1705338000,
  "iat": 1705337700
}
```

**Response (token inválido/expirado):**
```json
{
  "active": false
}
```

## Revocation Endpoint

### POST /protocol/openid-connect/revoke

Invalida refresh token específico.

```bash
curl -X POST "https://keycloak.carf.gov.br/realms/carf/protocol/openid-connect/revoke" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "token=eyJhbGciOiJIUzI1NiIs..." \
  -d "token_type_hint=refresh_token" \
  -d "client_id=geoweb"
```

**Response:** `200 OK` (sempre, mesmo se token não existir)

## Estrutura do Access Token JWT

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "key-id-001"
  },
  "payload": {
    "exp": 1705338000,
    "iat": 1705337700,
    "jti": "token-uuid",
    "iss": "https://keycloak.carf.gov.br/realms/carf",
    "aud": "account",
    "sub": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "typ": "Bearer",
    "azp": "geoweb",
    "session_state": "session-uuid",
    "acr": "1",
    "realm_access": {
      "roles": ["analyst", "field-agent"]
    },
    "resource_access": {
      "geoweb": {
        "roles": ["editor"]
      }
    },
    "scope": "openid profile email tenants",
    "email_verified": true,
    "name": "João Silva",
    "preferred_username": "52998224725",
    "given_name": "João",
    "family_name": "Silva",
    "email": "joao.silva@email.com",
    "tenants": ["tenant-001", "tenant-002"],
    "current_tenant": "tenant-001"
  }
}
```

## Referências

- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [OAuth 2.0 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [PKCE RFC 7636](https://tools.ietf.org/html/rfc7636)
- [07-error-codes](./07-error-codes.md) - Códigos de erro OAuth2/OIDC
