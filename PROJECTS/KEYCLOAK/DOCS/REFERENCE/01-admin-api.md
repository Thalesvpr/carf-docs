---
status: review
updated: 2026-01-21
---

# Admin REST API

Keycloak Admin REST API permite gerenciamento programático de realms, usuários, roles, clients e configurações. Base URL para realm CARF: `/admin/realms/carf`. Autenticação via Bearer token obtido através admin-cli client credentials flow ou token de usuário com role realm-admin.

## Autenticação

### Obter Token Admin

```bash
# Via admin-cli (service account)
curl -X POST "https://keycloak.carf.gov.br/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=<admin-password>" \
  -d "grant_type=password"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer"
}
```

### Headers Obrigatórios

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Endpoints de Realm

### GET /admin/realms/{realm}

Retorna configuração completa do realm.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
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
  "bruteForceProtected": true,
  "maxFailureWaitSeconds": 900,
  "failureFactor": 5,
  "accessTokenLifespan": 300,
  "ssoSessionIdleTimeout": 1800,
  "loginTheme": "carf",
  "accountTheme": "carf",
  "emailTheme": "carf",
  "internationalizationEnabled": true,
  "supportedLocales": ["pt-BR", "en"],
  "defaultLocale": "pt-BR"
}
```

### PUT /admin/realms/{realm}

Atualiza configurações do realm.

```bash
curl -X PUT "https://keycloak.carf.gov.br/admin/realms/carf" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "loginTheme": "carf-v2",
    "accessTokenLifespan": 600
  }'
```

## Endpoints de Usuários

### GET /admin/realms/{realm}/users

Lista usuários com paginação e filtros.

**Query Parameters:**

| Param | Tipo | Descrição |
|:------|:-----|:----------|
| `first` | int | Offset para paginação (default: 0) |
| `max` | int | Limite de resultados (default: 100, max: 1000) |
| `search` | string | Busca em username, firstName, lastName, email |
| `username` | string | Filtro exato por username |
| `email` | string | Filtro exato por email |
| `enabled` | boolean | Filtro por status |
| `briefRepresentation` | boolean | Retorna versão resumida (default: true) |

```bash
# Buscar usuários com CPF começando em 529
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/users?search=529&max=20" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "username": "52998224725",
    "email": "joao.silva@email.com",
    "firstName": "João",
    "lastName": "Silva",
    "enabled": true,
    "emailVerified": true,
    "createdTimestamp": 1705334400000,
    "attributes": {
      "tenants": ["tenant-001", "tenant-002"],
      "current_tenant": ["tenant-001"]
    }
  }
]
```

### GET /admin/realms/{realm}/users/count

Conta usuários com filtros opcionais.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/users/count?enabled=true" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:** `1523`

### POST /admin/realms/{realm}/users

Cria novo usuário.

```bash
curl -X POST "https://keycloak.carf.gov.br/admin/realms/carf/users" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "12345678900",
    "email": "maria.santos@email.com",
    "firstName": "Maria",
    "lastName": "Santos",
    "enabled": true,
    "emailVerified": false,
    "attributes": {
      "tenants": ["tenant-001"],
      "current_tenant": ["tenant-001"]
    },
    "credentials": [
      {
        "type": "password",
        "value": "senha-temporaria",
        "temporary": true
      }
    ]
  }'
```

**Response:** `201 Created` com header `Location: /admin/realms/carf/users/{id}`

### GET /admin/realms/{realm}/users/{id}

Obtém usuário por ID.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479" \
  -H "Authorization: Bearer $TOKEN"
```

### PUT /admin/realms/{realm}/users/{id}

Atualiza dados do usuário.

```bash
curl -X PUT "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "João Carlos",
    "attributes": {
      "tenants": ["tenant-001", "tenant-002", "tenant-003"],
      "current_tenant": ["tenant-002"]
    }
  }'
```

### DELETE /admin/realms/{realm}/users/{id}

Remove usuário.

```bash
curl -X DELETE "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:** `204 No Content`

## Endpoints de Roles

### GET /admin/realms/{realm}/roles

Lista todas roles do realm.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/roles" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "id": "role-001",
    "name": "admin",
    "description": "Administrador do sistema",
    "composite": false
  },
  {
    "id": "role-002",
    "name": "analyst",
    "description": "Analista de regularização",
    "composite": false
  },
  {
    "id": "role-003",
    "name": "field-agent",
    "description": "Agente de campo",
    "composite": false
  }
]
```

### POST /admin/realms/{realm}/roles

Cria nova role.

```bash
curl -X POST "https://keycloak.carf.gov.br/admin/realms/carf/roles" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "supervisor",
    "description": "Supervisor de equipe de campo"
  }'
```

### GET /admin/realms/{realm}/users/{id}/role-mappings/realm

Lista roles atribuídas ao usuário.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/role-mappings/realm" \
  -H "Authorization: Bearer $TOKEN"
```

### POST /admin/realms/{realm}/users/{id}/role-mappings/realm

Atribui roles ao usuário.

```bash
curl -X POST "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/role-mappings/realm" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {"id": "role-002", "name": "analyst"},
    {"id": "role-003", "name": "field-agent"}
  ]'
```

### DELETE /admin/realms/{realm}/users/{id}/role-mappings/realm

Remove roles do usuário.

```bash
curl -X DELETE "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/role-mappings/realm" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '[{"id": "role-003", "name": "field-agent"}]'
```

## Endpoints de Clients

### GET /admin/realms/{realm}/clients

Lista clients configurados.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/clients?clientId=geoweb" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "id": "client-uuid-001",
    "clientId": "geoweb",
    "name": "GEOWEB Application",
    "enabled": true,
    "publicClient": true,
    "directAccessGrantsEnabled": false,
    "standardFlowEnabled": true,
    "implicitFlowEnabled": false,
    "serviceAccountsEnabled": false,
    "redirectUris": [
      "https://geoweb.carf.gov.br/*",
      "http://localhost:3000/*"
    ],
    "webOrigins": [
      "https://geoweb.carf.gov.br",
      "http://localhost:3000"
    ]
  }
]
```

### GET /admin/realms/{realm}/clients/{id}/service-account-user

Obtém service account user de um client confidential.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/clients/client-uuid-002/service-account-user" \
  -H "Authorization: Bearer $TOKEN"
```

## Endpoints de Groups

### GET /admin/realms/{realm}/groups

Lista grupos do realm.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/groups" \
  -H "Authorization: Bearer $TOKEN"
```

### POST /admin/realms/{realm}/users/{id}/groups/{groupId}

Adiciona usuário a um grupo.

```bash
curl -X PUT "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/groups/group-uuid-001" \
  -H "Authorization: Bearer $TOKEN"
```

### DELETE /admin/realms/{realm}/users/{id}/groups/{groupId}

Remove usuário de um grupo.

```bash
curl -X DELETE "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/groups/group-uuid-001" \
  -H "Authorization: Bearer $TOKEN"
```

## Gerenciamento de Sessões

### GET /admin/realms/{realm}/users/{id}/sessions

Lista sessões ativas do usuário.

```bash
curl -X GET "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/sessions" \
  -H "Authorization: Bearer $TOKEN"
```

**Response:**
```json
[
  {
    "id": "session-uuid-001",
    "username": "52998224725",
    "ipAddress": "192.168.1.100",
    "start": 1705334400000,
    "lastAccess": 1705337800000,
    "clients": {
      "geoweb": "GEOWEB Application"
    }
  }
]
```

### DELETE /admin/realms/{realm}/users/{id}/sessions

Invalida todas sessões do usuário (logout forçado).

```bash
curl -X DELETE "https://keycloak.carf.gov.br/admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479/sessions" \
  -H "Authorization: Bearer $TOKEN"
```

## Boas Práticas

**Paginação obrigatória**: Para listagens grandes, sempre usar `first` e `max` para evitar timeout e sobrecarga.

**Rate limiting**: Implementar backoff exponencial para chamadas em lote. Keycloak não tem rate limiting nativo, mas servidores podem ter limites.

**Cache de tokens**: Admin tokens têm `expires_in` curto (300s). Cachear e fazer refresh antes da expiração.

**Audit log**: Todas operações admin são logadas. Verificar logs em `/admin/realms/{realm}/events`.

## Referências

- [Keycloak Admin REST API](https://keycloak.org/docs-api/latest/rest-api/index.html)
- [02-oidc-endpoints](./02-oidc-endpoints.md) - Endpoints de autenticação
- [INTEGRATION](../INTEGRATION/README.md) - Configuracao de integracao
