# Login

Schema e comportamento do endpoint de autenticação via Keycloak.

## Endpoint

```
POST /api/auth/login
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "required": ["username", "password"],
  "properties": {
    "username": {
      "type": "string",
      "description": "Email ou username do usuário",
      "example": "joao.silva@prefeitura.gov.br"
    },
    "password": {
      "type": "string",
      "format": "password",
      "minLength": 8
    },
    "tenant_id": {
      "type": "string",
      "format": "uuid",
      "description": "Município alvo (opcional se usuário tem apenas um)"
    },
    "remember_me": {
      "type": "boolean",
      "default": false,
      "description": "Estende validade do refresh token para 30 dias"
    }
  }
}
```

## Response Schema (200 OK)

```json
{
  "type": "object",
  "properties": {
    "access_token": {
      "type": "string",
      "description": "JWT para autenticação em requests"
    },
    "refresh_token": {
      "type": "string",
      "description": "Token para renovar access_token"
    },
    "token_type": {
      "type": "string",
      "enum": ["Bearer"]
    },
    "expires_in": {
      "type": "integer",
      "description": "Segundos até expiração do access_token",
      "example": 900
    },
    "refresh_expires_in": {
      "type": "integer",
      "description": "Segundos até expiração do refresh_token"
    },
    "user": {
      "type": "object",
      "properties": {
        "id": { "type": "string", "format": "uuid" },
        "email": { "type": "string", "format": "email" },
        "name": { "type": "string" },
        "roles": { "type": "array", "items": { "type": "string" } },
        "tenant_id": { "type": "string", "format": "uuid" },
        "tenant_name": { "type": "string" }
      }
    }
  }
}
```

## Códigos de Erro

| Código | Erro | Descrição |
|--------|------|-----------|
| 401 | invalid_credentials | Username ou senha incorretos |
| 403 | tenant_access_denied | Usuário não tem acesso ao tenant especificado |
| 422 | validation_error | Campos obrigatórios ausentes ou inválidos |
| 423 | account_locked | Conta bloqueada após múltiplas tentativas |
| 429 | rate_limited | Excedeu limite de tentativas de login |

## Exemplo de Uso

```bash
curl -X POST https://api.carf.com.br/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "joao.silva@prefeitura.gov.br",
    "password": "senha123",
    "tenant_id": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

## JWT Claims

O access_token contém:

```json
{
  "sub": "user-uuid",
  "email": "joao.silva@prefeitura.gov.br",
  "name": "João Silva",
  "roles": ["cadastrista", "visualizador"],
  "tenant_id": "tenant-uuid",
  "iat": 1705401600,
  "exp": 1705402500,
  "iss": "https://keycloak.carf.com.br/realms/carf"
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
