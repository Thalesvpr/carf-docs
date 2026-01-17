# Logout

Schema e comportamento do endpoint de logout.

## Endpoint

```
POST /api/auth/logout
Authorization: Bearer {access_token}
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "properties": {
    "refresh_token": {
      "type": "string",
      "description": "Refresh token a ser revogado (opcional)"
    },
    "all_sessions": {
      "type": "boolean",
      "default": false,
      "description": "Revogar todas as sessões do usuário"
    }
  }
}
```

## Response (204 No Content)

Logout bem-sucedido não retorna body.

## Códigos de Erro

| Código | Erro | Descrição |
|--------|------|-----------|
| 401 | unauthorized | Access token ausente ou inválido |

## Comportamento

- Revoga o refresh_token especificado no Keycloak
- Com `all_sessions: true`, revoga todos os tokens do usuário
- Access token continua válido até expirar (stateless)
- Para invalidação imediata de access token, verificar contra blacklist

## Exemplo de Uso

```bash
# Logout simples
curl -X POST https://api.carf.com.br/api/auth/logout \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI..." \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIi..."
  }'

# Logout de todas as sessões
curl -X POST https://api.carf.com.br/api/auth/logout \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI..." \
  -H "Content-Type: application/json" \
  -d '{ "all_sessions": true }'
```

## Integração Frontend

```typescript
async function logout(allSessions: boolean = false): Promise<void> {
  await fetch('/api/auth/logout', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${getAccessToken()}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      refresh_token: getStoredRefreshToken(),
      all_sessions: allSessions
    })
  });

  clearStoredTokens();
  redirectToLogin();
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
