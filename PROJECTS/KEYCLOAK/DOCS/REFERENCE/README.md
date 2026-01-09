# REFERENCE - Referências Técnicas

Documentação de referência para APIs, configurações, e especificações técnicas.

## APIs

### Keycloak Admin REST API
- **Base URL**: `http://localhost:8080/admin/realms/carf`
- **Auth**: Bearer token (admin-cli client)
- **Docs**: https://www.keycloak.org/docs-api/24.0/rest-api/

#### Endpoints Principais
```
GET    /admin/realms/carf                  # Realm info
GET    /admin/realms/carf/users            # List users
POST   /admin/realms/carf/users            # Create user
GET    /admin/realms/carf/users/{id}       # Get user
PUT    /admin/realms/carf/users/{id}       # Update user
DELETE /admin/realms/carf/users/{id}       # Delete user
GET    /admin/realms/carf/clients          # List clients
GET    /admin/realms/carf/roles            # List roles
POST   /admin/realms/carf/users/{id}/role-mappings/realm # Assign role
```

### OpenID Connect Endpoints
- **Discovery**: `/.well-known/openid-configuration`
- **Authorize**: `/protocol/openid-connect/auth`
- **Token**: `/protocol/openid-connect/token`
- **UserInfo**: `/protocol/openid-connect/userinfo`
- **JWKS**: `/protocol/openid-connect/certs`
- **Logout**: `/protocol/openid-connect/logout`
- **Introspect**: `/protocol/openid-connect/token/introspect`
- **Revoke**: `/protocol/openid-connect/revoke`

## Configurações

### theme.properties Reference
```properties
# Parent theme (optional)
parent=keycloak.v2

# CSS files (relative to resources/)
styles=css/main.css css/custom.css

# JavaScript files (relative to resources/)
scripts=js/app.js js/validation.js

# Locales supported
locales=pt-BR,en,es

# Import resources from common
import=common/keycloak

# Cache themes (prod only)
cacheThemes=true

# Cache templates (prod only)
cacheTemplates=true
```

### FreeMarker Variables
```ftl
${realm.name}                       # Realm name
${realm.displayName}                # Realm display name
${realm.internationalizationEnabled} # i18n enabled

${url.loginAction}                  # Form action URL
${url.loginUrl}                     # Login URL
${url.registrationUrl}              # Registration URL
${url.loginResetCredentialsUrl}     # Password reset URL
${url.resourcesPath}                # Theme resources path

${msg("key")}                       # Localized message
${properties.kcFormClass}           # CSS class from parent

${login.username}                   # Username from form
${login.rememberMe}                 # Remember me checkbox

${user.username}                    # Current user username
${user.email}                       # Current user email
${user.firstName}                   # First name
${user.lastName}                    # Last name

${auth.attemptedUsername}           # Failed login attempt
${auth.showUsername}                # Show username in form

${client.clientId}                  # Client ID
${client.name}                      # Client name

${social.providers}                 # Social identity providers

${message.summary}                  # Message to display
${message.type}                     # success|error|warning|info
```

### Environment Variables
```bash
# Admin credentials
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=<strong-password>

# Database
KC_DB=postgres
KC_DB_URL=jdbc:postgresql://postgres:5432/keycloak
KC_DB_USERNAME=keycloak
KC_DB_PASSWORD=<db-password>

# Hostname
KC_HOSTNAME=keycloak.carf.gov.br
KC_HOSTNAME_STRICT=true
KC_HOSTNAME_STRICT_HTTPS=true

# HTTP/HTTPS
KC_HTTP_ENABLED=false
KC_HTTPS_PORT=8443
KC_HTTPS_CERTIFICATE_FILE=/path/to/cert.pem
KC_HTTPS_CERTIFICATE_KEY_FILE=/path/to/key.pem

# Proxy
KC_PROXY=edge                       # edge|reencrypt|passthrough

# Health & Metrics
KC_HEALTH_ENABLED=true
KC_METRICS_ENABLED=true

# Logging
KC_LOG_LEVEL=info                   # info|debug|warn|error
KC_LOG_FORMAT=json                  # json|default

# Performance
KC_DB_POOL_INITIAL_SIZE=5
KC_DB_POOL_MIN_SIZE=5
KC_DB_POOL_MAX_SIZE=20
KC_TRANSACTION_XA_ENABLED=false
```

### Realm Export Schema
```json
{
  "id": "carf",
  "realm": "carf",
  "displayName": "CARF - Regularização Fundiária",
  "enabled": true,
  "sslRequired": "external",
  "registrationAllowed": false,
  "loginWithEmailAllowed": true,
  "duplicateEmailsAllowed": false,
  "resetPasswordAllowed": true,
  "editUsernameAllowed": false,
  "bruteForceProtected": true,
  "permanentLockout": false,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "waitIncrementSeconds": 60,
  "quickLoginCheckMilliSeconds": 1000,
  "maxDeltaTimeSeconds": 43200,
  "failureFactor": 5,
  "accessTokenLifespan": 300,
  "accessTokenLifespanForImplicitFlow": 900,
  "ssoSessionIdleTimeout": 1800,
  "ssoSessionMaxLifespan": 36000,
  "offlineSessionIdleTimeout": 2592000,
  "accessCodeLifespan": 60,
  "accessCodeLifespanUserAction": 300,
  "accessCodeLifespanLogin": 1800,
  "loginTheme": "carf",
  "accountTheme": "carf",
  "emailTheme": "carf",
  "internationalizationEnabled": true,
  "supportedLocales": ["pt-BR", "en"],
  "defaultLocale": "pt-BR",
  "clients": [...],
  "roles": {...},
  "users": [...],
  "clientScopes": [...],
  "protocolMappers": [...]
}
```

## Códigos de Erro

### OAuth2/OIDC Errors
| Código | Descrição | Causa |
|--------|-----------|-------|
| `invalid_request` | Request malformed | Faltando parâmetros obrigatórios |
| `invalid_client` | Client authentication failed | client_id/client_secret inválidos |
| `invalid_grant` | Grant type inválido ou expirado | Code/refresh_token expirado |
| `unauthorized_client` | Client não autorizado para grant type | Client config incorreta |
| `unsupported_grant_type` | Grant type não suportado | Grant type não habilitado |
| `invalid_scope` | Scope inválido | Scope não existe ou não permitido |
| `access_denied` | Usuário negou consentimento | User cancelou autorização |

### HTTP Status Codes
| Status | Significado | Ação |
|--------|-------------|------|
| 200 | Success | Request processado com sucesso |
| 400 | Bad Request | Validar payload e parâmetros |
| 401 | Unauthorized | Token inválido/expirado, fazer refresh |
| 403 | Forbidden | User sem permissão, verificar roles |
| 404 | Not Found | Recurso não existe |
| 409 | Conflict | Username/email já existe |
| 429 | Too Many Requests | Rate limit, implementar backoff |
| 500 | Internal Server Error | Ver logs Keycloak |
| 503 | Service Unavailable | Keycloak down ou overloaded |

## Performance Tuning

### Database Connection Pool
```properties
KC_DB_POOL_INITIAL_SIZE=10
KC_DB_POOL_MIN_SIZE=10
KC_DB_POOL_MAX_SIZE=50
```

### JVM Heap
```bash
JAVA_OPTS="-Xms1024m -Xmx2048m -XX:MaxMetaspaceSize=512m"
```

### Cache Config
```bash
KC_CACHE=ispn
KC_CACHE_STACK=tcp
```

## Referências Externas

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [Admin REST API](https://www.keycloak.org/docs-api/24.0/rest-api/)
- [Server Administration Guide](https://www.keycloak.org/docs/latest/server_admin/)
- [OAuth 2.0 RFC 6749](https://datatracker.ietf.org/doc/html/rfc6749)
- [OpenID Connect Core 1.0](https://openid.net/specs/openid-connect-core-1_0.html)
- [PKCE RFC 7636](https://datatracker.ietf.org/doc/html/rfc7636)
