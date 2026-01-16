# Refresh Token

Schema e comportamento do endpoint de renovação de tokens.

## Endpoint

```
POST /api/auth/refresh
Content-Type: application/json
```

## Request Schema

```json
{
  "type": "object",
  "required": ["refresh_token"],
  "properties": {
    "refresh_token": {
      "type": "string",
      "description": "Refresh token obtido no login"
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
      "description": "Novo JWT para autenticação"
    },
    "refresh_token": {
      "type": "string",
      "description": "Novo refresh token (rotacionado)"
    },
    "token_type": {
      "type": "string",
      "enum": ["Bearer"]
    },
    "expires_in": {
      "type": "integer",
      "example": 900
    }
  }
}
```

## Códigos de Erro

| Código | Erro | Descrição |
|--------|------|-----------|
| 401 | invalid_token | Refresh token inválido ou malformado |
| 401 | token_expired | Refresh token expirou |
| 401 | token_revoked | Refresh token foi revogado (logout em outro dispositivo) |

## Comportamento

- Refresh tokens são rotacionados a cada uso (o anterior é invalidado)
- Validade padrão do refresh token: 7 dias (30 dias com remember_me)
- Novo access_token herda claims do anterior com timestamps atualizados
- Se refresh token expirou, usuário deve fazer login novamente

## Exemplo de Uso

```bash
curl -X POST https://api.carf.com.br/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIi..."
  }'
```

## Integração Frontend

```typescript
// Interceptor para renovação automática
async function refreshAccessToken(): Promise<string> {
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh_token: getStoredRefreshToken() })
  });

  if (!response.ok) {
    // Redirecionar para login
    throw new AuthenticationError('Session expired');
  }

  const data = await response.json();
  storeTokens(data.access_token, data.refresh_token);
  return data.access_token;
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
