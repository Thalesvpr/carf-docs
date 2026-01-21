---
status: review
updated: 2026-01-21
---

# Keycloak Client Configuration

Configuração completa do client Keycloak para autenticação do WEBDOCS. Client carf-webdocs é public client que usa Authorization Code flow com PKCE para Single Page Applications.

## Client Configuration JSON

```json
{
  "clientId": "carf-webdocs",
  "name": "CARF WebDocs Portal",
  "description": "Portal de documentação do sistema CARF",
  "enabled": true,
  "publicClient": true,
  "protocol": "openid-connect",
  "rootUrl": "https://docs.carf.com.br",
  "baseUrl": "/",
  "redirectUris": [
    "http://localhost:4321/auth/callback",
    "http://localhost:4321/admin",
    "https://docs.carf.com.br/auth/callback",
    "https://docs.carf.com.br/admin"
  ],
  "webOrigins": [
    "http://localhost:4321",
    "https://docs.carf.com.br"
  ],
  "adminUrl": "https://docs.carf.com.br",
  "attributes": {
    "pkce.code.challenge.method": "S256",
    "post.logout.redirect.uris": "http://localhost:4321/+https://docs.carf.com.br/"
  }
}
```

## Token Configuration

```json
{
  "token_settings": {
    "accessTokenLifespan": 300,
    "accessTokenLifespanForImplicitFlow": 300,
    "refreshTokenLifespan": 28800,
    "ssoSessionIdleTimeout": 1800,
    "ssoSessionMaxLifespan": 28800,
    "offlineSessionIdleTimeout": 2592000,
    "offlineSessionMaxLifespan": 5184000
  },
  "description": {
    "accessTokenLifespan": "5 minutos - tempo curto para segurança",
    "refreshTokenLifespan": "8 horas - sessão de trabalho típica",
    "ssoSessionIdleTimeout": "30 minutos - inatividade antes de reautenticar",
    "ssoSessionMaxLifespan": "8 horas - máximo absoluto de sessão SSO"
  }
}
```

## Scopes Necessários

```json
{
  "defaultClientScopes": [
    "openid",
    "profile",
    "email",
    "roles"
  ],
  "optionalClientScopes": [
    "offline_access"
  ],
  "scope_details": {
    "openid": "Obrigatório para OIDC - retorna sub claim",
    "profile": "Nome, sobrenome, username - exibição no UserMenu",
    "email": "Email do usuário - exibição e notificações",
    "roles": "realm_access.roles - necessário para RBAC"
  }
}
```

## Mapper Configuration

Client precisa de mapper para incluir roles no token:

```json
{
  "mappers": [
    {
      "name": "realm roles",
      "protocol": "openid-connect",
      "protocolMapper": "oidc-usermodel-realm-role-mapper",
      "consentRequired": false,
      "config": {
        "multivalued": "true",
        "userinfo.token.claim": "true",
        "id.token.claim": "true",
        "access.token.claim": "true",
        "claim.name": "realm_access.roles",
        "jsonType.label": "String"
      }
    },
    {
      "name": "tenant_id",
      "protocol": "openid-connect",
      "protocolMapper": "oidc-usermodel-attribute-mapper",
      "consentRequired": false,
      "config": {
        "userinfo.token.claim": "true",
        "user.attribute": "tenant_id",
        "id.token.claim": "true",
        "access.token.claim": "true",
        "claim.name": "tenant_id",
        "jsonType.label": "String"
      }
    }
  ]
}
```

## Endpoints do Realm

```json
{
  "endpoints": {
    "issuer": "https://auth.carf.com.br/realms/carf",
    "authorization_endpoint": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/auth",
    "token_endpoint": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/token",
    "userinfo_endpoint": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/userinfo",
    "end_session_endpoint": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/logout",
    "jwks_uri": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/certs",
    "introspection_endpoint": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/token/introspect"
  }
}
```

## Configuração para Desenvolvimento Local

Para desenvolvimento local, criar client separado ou adicionar URIs:

```json
{
  "development": {
    "redirectUris_to_add": [
      "http://localhost:4321/*",
      "http://127.0.0.1:4321/*"
    ],
    "webOrigins_to_add": [
      "http://localhost:4321",
      "http://127.0.0.1:4321"
    ],
    "notes": [
      "Usar variável KEYCLOAK_URL=http://localhost:8080 para Keycloak local",
      "Realm de desenvolvimento pode ter tokens mais longos para debug"
    ]
  }
}
```

## Variáveis de Ambiente Relacionadas

```bash
# Keycloak Configuration
KEYCLOAK_URL=https://auth.carf.com.br
KEYCLOAK_REALM=carf
KEYCLOAK_CLIENT_ID=carf-webdocs

# Desenvolvimento Local
# KEYCLOAK_URL=http://localhost:8080
# KEYCLOAK_REALM=carf-dev
```

## Validação de Configuração

Teste de configuração correta:

1. **Verificar .well-known:**
```bash
curl https://auth.carf.com.br/realms/carf/.well-known/openid-configuration
```

2. **Verificar JWKS:**
```bash
curl https://auth.carf.com.br/realms/carf/protocol/openid-connect/certs
```

3. **Testar Authorization URL manualmente:**
```
https://auth.carf.com.br/realms/carf/protocol/openid-connect/auth?
  client_id=carf-webdocs&
  redirect_uri=http://localhost:4321/auth/callback&
  response_type=code&
  scope=openid profile email&
  code_challenge=<GENERATED>&
  code_challenge_method=S256&
  state=<RANDOM>
```

## Troubleshooting

```json
{
  "common_errors": {
    "invalid_redirect_uri": {
      "cause": "URI não cadastrada no client",
      "solution": "Adicionar URI exata (incluindo porta) nas redirectUris"
    },
    "invalid_client": {
      "cause": "client_id incorreto ou client desabilitado",
      "solution": "Verificar clientId e enabled=true"
    },
    "cors_error": {
      "cause": "Origin não permitida",
      "solution": "Adicionar origin nas webOrigins do client"
    },
    "pkce_required": {
      "cause": "Client requer PKCE mas code_challenge não enviado",
      "solution": "Implementar PKCE conforme SPECS/21-pkce-implementation.md"
    }
  }
}
```

Configuração detalhada de PKCE em SPECS/21-pkce-implementation.md.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
