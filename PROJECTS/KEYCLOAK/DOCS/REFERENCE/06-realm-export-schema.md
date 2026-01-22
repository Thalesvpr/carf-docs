---
type: leaf
status: rejected
description: "REFERENCE usa tabelas extensivas e code blocks JSON - formato referencia incompativel com prosa densa"
updated: 2026-01-22
---

# Realm Export Schema

Estrutura JSON do arquivo `realm-export.json` para versionamento de configuração como código (Configuration as Code). Importável via `--import-realm` flag no startup do Keycloak.

## Estrutura Raiz

```json
{
  "id": "carf",
  "realm": "carf",
  "displayName": "Sistema CARF",
  "displayNameHtml": "<strong>CARF</strong>",
  "enabled": true,
  ...
}
```

| Campo | Tipo | Obrigatório | Descrição |
|:------|:-----|:------------|:----------|
| `id` | string | Sim | Identificador interno (geralmente igual a `realm`) |
| `realm` | string | Sim | Nome do realm (usado em URLs) |
| `displayName` | string | Não | Nome amigável para UI |
| `displayNameHtml` | string | Não | Nome com HTML para branding |
| `enabled` | boolean | Não | Se realm está ativo (default: true) |

## SSL e Segurança

```json
{
  "sslRequired": "external",
  "bruteForceProtected": true,
  "permanentLockout": false,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "waitIncrementSeconds": 60,
  "quickLoginCheckMilliSeconds": 1000,
  "maxDeltaTimeSeconds": 43200,
  "failureFactor": 5
}
```

| Campo | Tipo | Default | Descrição |
|:------|:-----|:--------|:----------|
| `sslRequired` | string | `external` | `all`, `external`, `none` |
| `bruteForceProtected` | boolean | `false` | Proteção contra brute force |
| `permanentLockout` | boolean | `false` | Lock permanente após falhas |
| `maxFailureWaitSeconds` | int | `900` | Wait máximo (15 min) |
| `failureFactor` | int | `30` | Tentativas antes de lock |

## Registro e Login

```json
{
  "registrationAllowed": true,
  "registrationEmailAsUsername": false,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "resetPasswordAllowed": true,
  "editUsernameAllowed": false,
  "verifyEmail": true,
  "rememberMe": true
}
```

| Campo | Tipo | Default | Descrição |
|:------|:-----|:--------|:----------|
| `registrationAllowed` | boolean | `false` | Auto-registro habilitado |
| `registrationEmailAsUsername` | boolean | `false` | Email como username |
| `loginWithEmailAllowed` | boolean | `true` | Permite login com email |
| `duplicateEmailsAllowed` | boolean | `false` | Permite emails duplicados |
| `resetPasswordAllowed` | boolean | `false` | Recuperação de senha |
| `editUsernameAllowed` | boolean | `false` | Usuário pode editar username |
| `verifyEmail` | boolean | `false` | Requer verificação de email |
| `rememberMe` | boolean | `false` | Opção "lembrar-me" |

## Token Lifespans

```json
{
  "accessTokenLifespan": 300,
  "accessTokenLifespanForImplicitFlow": 900,
  "ssoSessionIdleTimeout": 1800,
  "ssoSessionMaxLifespan": 36000,
  "ssoSessionIdleTimeoutRememberMe": 0,
  "ssoSessionMaxLifespanRememberMe": 0,
  "offlineSessionIdleTimeout": 2592000,
  "offlineSessionMaxLifespanEnabled": false,
  "offlineSessionMaxLifespan": 5184000,
  "accessCodeLifespan": 60,
  "accessCodeLifespanUserAction": 300,
  "accessCodeLifespanLogin": 1800,
  "actionTokenGeneratedByAdminLifespan": 43200,
  "actionTokenGeneratedByUserLifespan": 300
}
```

| Campo | Tipo | Default | Descrição |
|:------|:-----|:--------|:----------|
| `accessTokenLifespan` | int | `300` | Vida do access token (5 min) |
| `ssoSessionIdleTimeout` | int | `1800` | Idle timeout SSO (30 min) |
| `ssoSessionMaxLifespan` | int | `36000` | Max lifetime SSO (10h) |
| `offlineSessionIdleTimeout` | int | `2592000` | Idle offline (30 dias) |
| `accessCodeLifespan` | int | `60` | Vida do auth code (1 min) |

## Temas

```json
{
  "loginTheme": "carf",
  "accountTheme": "carf",
  "adminTheme": "keycloak.v2",
  "emailTheme": "carf"
}
```

## Internacionalização

```json
{
  "internationalizationEnabled": true,
  "supportedLocales": ["pt-BR", "en", "es"],
  "defaultLocale": "pt-BR"
}
```

## Clients

Array de clients OAuth2/OIDC configurados.

```json
{
  "clients": [
    {
      "clientId": "geoweb",
      "name": "GEOWEB Application",
      "description": "Sistema de Gestão de Regularização Fundiária",
      "enabled": true,
      "clientAuthenticatorType": "client-secret",
      "secret": "${GEOWEB_CLIENT_SECRET}",
      "publicClient": true,
      "protocol": "openid-connect",
      "standardFlowEnabled": true,
      "implicitFlowEnabled": false,
      "directAccessGrantsEnabled": false,
      "serviceAccountsEnabled": false,
      "authorizationServicesEnabled": false,
      "rootUrl": "https://geoweb.carf.gov.br",
      "baseUrl": "/",
      "redirectUris": [
        "https://geoweb.carf.gov.br/*",
        "http://localhost:3000/*"
      ],
      "webOrigins": [
        "https://geoweb.carf.gov.br",
        "http://localhost:3000"
      ],
      "defaultClientScopes": [
        "openid",
        "profile",
        "email",
        "tenants"
      ],
      "optionalClientScopes": [
        "offline_access"
      ],
      "attributes": {
        "pkce.code.challenge.method": "S256",
        "post.logout.redirect.uris": "https://geoweb.carf.gov.br/*"
      }
    },
    {
      "clientId": "geoapi",
      "name": "GeoAPI Service",
      "enabled": true,
      "publicClient": false,
      "secret": "${GEOAPI_CLIENT_SECRET}",
      "serviceAccountsEnabled": true,
      "standardFlowEnabled": false,
      "directAccessGrantsEnabled": false,
      "authorizationServicesEnabled": true
    }
  ]
}
```

**Campos importantes de client:**

| Campo | Tipo | Descrição |
|:------|:-----|:----------|
| `clientId` | string | Identificador único |
| `publicClient` | boolean | `true` para SPAs, `false` para confidential |
| `secret` | string | Secret para clients confidenciais |
| `standardFlowEnabled` | boolean | Authorization Code flow |
| `implicitFlowEnabled` | boolean | Implicit flow (deprecated) |
| `directAccessGrantsEnabled` | boolean | Resource Owner Password |
| `serviceAccountsEnabled` | boolean | Client Credentials flow |
| `redirectUris` | array | URIs de redirect permitidas |
| `webOrigins` | array | CORS origins permitidas |

## Client Scopes

Scopes compartilhados entre clients.

```json
{
  "clientScopes": [
    {
      "name": "tenants",
      "description": "Multi-tenancy claims",
      "protocol": "openid-connect",
      "attributes": {
        "include.in.token.scope": "true",
        "display.on.consent.screen": "true"
      },
      "protocolMappers": [
        {
          "name": "tenants",
          "protocol": "openid-connect",
          "protocolMapper": "oidc-usermodel-attribute-mapper",
          "consentRequired": false,
          "config": {
            "claim.name": "tenants",
            "user.attribute": "tenants",
            "jsonType.label": "JSON",
            "id.token.claim": "true",
            "access.token.claim": "true",
            "userinfo.token.claim": "true",
            "multivalued": "true"
          }
        },
        {
          "name": "current_tenant",
          "protocol": "openid-connect",
          "protocolMapper": "oidc-usermodel-attribute-mapper",
          "config": {
            "claim.name": "current_tenant",
            "user.attribute": "current_tenant",
            "id.token.claim": "true",
            "access.token.claim": "true",
            "userinfo.token.claim": "true"
          }
        }
      ]
    }
  ],
  "defaultDefaultClientScopes": [
    "openid",
    "profile",
    "email",
    "roles",
    "tenants"
  ],
  "defaultOptionalClientScopes": [
    "offline_access",
    "phone"
  ]
}
```

## Roles

Roles do realm e de clients.

```json
{
  "roles": {
    "realm": [
      {
        "name": "admin",
        "description": "Administrador do sistema",
        "composite": false
      },
      {
        "name": "analyst",
        "description": "Analista de regularização",
        "composite": false
      },
      {
        "name": "field-agent",
        "description": "Agente de campo",
        "composite": false
      },
      {
        "name": "viewer",
        "description": "Visualizador",
        "composite": false
      }
    ],
    "client": {
      "geoweb": [
        {
          "name": "editor",
          "description": "Pode editar unidades"
        },
        {
          "name": "approver",
          "description": "Pode aprovar regularizações"
        }
      ]
    }
  },
  "defaultRoles": ["viewer"]
}
```

## Users (Seed)

Usuários iniciais para seed do ambiente.

```json
{
  "users": [
    {
      "username": "admin-carf",
      "email": "admin@carf.gov.br",
      "firstName": "Admin",
      "lastName": "CARF",
      "enabled": true,
      "emailVerified": true,
      "credentials": [
        {
          "type": "password",
          "value": "${ADMIN_CARF_PASSWORD}",
          "temporary": true
        }
      ],
      "realmRoles": ["admin"],
      "clientRoles": {
        "geoweb": ["editor", "approver"]
      },
      "attributes": {
        "tenants": ["*"],
        "current_tenant": ["tenant-001"]
      }
    }
  ]
}
```

**Nota**: Não incluir senhas reais em arquivos versionados. Usar variáveis de ambiente ou criar usuários via API após deploy.

## Authentication Flows

Customização de fluxos de autenticação.

```json
{
  "authenticationFlows": [
    {
      "alias": "carf-browser",
      "description": "CARF browser-based authentication",
      "providerId": "basic-flow",
      "topLevel": true,
      "builtIn": false,
      "authenticationExecutions": [
        {
          "authenticator": "auth-cookie",
          "requirement": "ALTERNATIVE",
          "priority": 10
        },
        {
          "authenticator": "auth-username-password-form",
          "requirement": "REQUIRED",
          "priority": 20
        }
      ]
    }
  ],
  "browserFlow": "carf-browser"
}
```

## Identity Providers

Configuração de IdPs externos (Google, SAML, etc.).

```json
{
  "identityProviders": [
    {
      "alias": "google",
      "displayName": "Google",
      "providerId": "google",
      "enabled": true,
      "trustEmail": true,
      "config": {
        "clientId": "${GOOGLE_CLIENT_ID}",
        "clientSecret": "${GOOGLE_CLIENT_SECRET}",
        "defaultScope": "openid email profile"
      }
    }
  ]
}
```

## Exemplo Completo CARF

```json
{
  "id": "carf",
  "realm": "carf",
  "displayName": "Sistema CARF",
  "enabled": true,
  "sslRequired": "external",

  "registrationAllowed": true,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "resetPasswordAllowed": true,
  "rememberMe": true,
  "verifyEmail": true,

  "bruteForceProtected": true,
  "failureFactor": 5,
  "maxFailureWaitSeconds": 900,

  "accessTokenLifespan": 300,
  "ssoSessionIdleTimeout": 1800,
  "ssoSessionMaxLifespan": 36000,

  "loginTheme": "carf",
  "accountTheme": "carf",
  "emailTheme": "carf",

  "internationalizationEnabled": true,
  "supportedLocales": ["pt-BR", "en"],
  "defaultLocale": "pt-BR",

  "clients": [...],
  "clientScopes": [...],
  "roles": {...},
  "defaultRoles": ["viewer"]
}
```

## Import via CLI

```bash
# Import no startup (recomendado para IaC)
/opt/keycloak/bin/kc.sh start --import-realm

# Import manual
/opt/keycloak/bin/kc.sh import --file /path/to/realm-carf.json

# Export para backup
/opt/keycloak/bin/kc.sh export --file /backup/realm-carf.json --realm carf
```

## Variáveis de Ambiente no JSON

Use `${VAR_NAME}` para injetar valores de variáveis de ambiente.

```json
{
  "clients": [
    {
      "clientId": "geoweb",
      "secret": "${GEOWEB_CLIENT_SECRET}"
    }
  ]
}
```

## Referências

- [Keycloak Server Administration - Realm Export/Import](https://keycloak.org/docs/latest/server_admin/#_export_import)
- [Keycloak REST API - Realm Representation](https://keycloak.org/docs-api/latest/rest-api/index.html#_realmrepresentation)
