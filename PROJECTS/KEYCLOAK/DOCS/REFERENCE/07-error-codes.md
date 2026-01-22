---
type: leaf
status: rejected
description: "REFERENCE usa tabelas extensivas e code blocks - formato referencia incompativel com prosa densa"
updated: 2026-01-22
---

# Error Codes

Códigos de erro OAuth2/OIDC e HTTP retornados pelo Keycloak, seguindo RFC 6749 (OAuth 2.0) e OpenID Connect Core 1.0.

## Erros OAuth2 (RFC 6749)

Erros retornados nos endpoints de autorização e token.

### invalid_request

Request malformado ou faltando parâmetros obrigatórios.

| Contexto | Causa Comum | Solução |
|:---------|:------------|:--------|
| Authorization | `client_id`, `redirect_uri` ou `response_type` ausente | Verificar URL de autorização |
| Token | `grant_type` ou `code` ausente | Verificar payload do POST |
| Token | `redirect_uri` não corresponde ao usado na autorização | Usar mesma `redirect_uri` |

**Exemplo de resposta:**
```json
{
  "error": "invalid_request",
  "error_description": "Missing parameter: redirect_uri"
}
```

### invalid_client

Falha na autenticação do client.

| Causa | Solução |
|:------|:--------|
| `client_id` não existe | Verificar ID do client no Admin Console |
| `client_secret` incorreto | Regenerar secret e atualizar aplicação |
| Client desabilitado | Habilitar client no Admin Console |
| Autenticação faltando para client confidencial | Incluir `client_id` e `client_secret` |

**Exemplo:**
```json
{
  "error": "invalid_client",
  "error_description": "Invalid client credentials"
}
```

### invalid_grant

Authorization code ou refresh token inválido.

| Causa | Solução |
|:------|:--------|
| Code expirado (>60s default) | Trocar code imediatamente após obtenção |
| Code já foi usado | Authorization codes são single-use |
| Refresh token expirado | Re-autenticar usuário |
| Refresh token revogado | Re-autenticar usuário |
| PKCE `code_verifier` incorreto | Verificar geração do verifier |

**Exemplo:**
```json
{
  "error": "invalid_grant",
  "error_description": "Code not valid"
}
```

### unauthorized_client

Client não autorizado para o grant type solicitado.

| Causa | Solução |
|:------|:--------|
| Client credentials em client público | Converter para client confidencial |
| Authorization code flow desabilitado | Habilitar `standardFlowEnabled` |
| Direct access grants desabilitado | Habilitar `directAccessGrantsEnabled` |

**Exemplo:**
```json
{
  "error": "unauthorized_client",
  "error_description": "Client not allowed for direct access grants"
}
```

### unsupported_grant_type

Grant type não suportado ou não habilitado.

| Grant Type | Configuração Necessária |
|:-----------|:------------------------|
| `authorization_code` | `standardFlowEnabled: true` |
| `refresh_token` | Automático com auth code |
| `client_credentials` | `serviceAccountsEnabled: true` |
| `password` | `directAccessGrantsEnabled: true` (não recomendado) |

**Exemplo:**
```json
{
  "error": "unsupported_grant_type",
  "error_description": "Invalid grant_type"
}
```

### invalid_scope

Scope solicitado não existe ou não é permitido.

| Causa | Solução |
|:------|:--------|
| Scope não existe no realm | Criar client scope |
| Scope não atribuído ao client | Adicionar em default ou optional scopes |
| Scope offline_access em client sem permissão | Atribuir scope ao client |

**Exemplo:**
```json
{
  "error": "invalid_scope",
  "error_description": "Invalid scopes: tenants"
}
```

### access_denied

Usuário negou autorização ou acesso foi bloqueado.

| Causa | Solução |
|:------|:--------|
| Usuário clicou "Cancelar" no consent | Informar usuário sobre necessidade |
| Conta desabilitada | Verificar status no Admin Console |
| Brute force lock | Aguardar timeout ou unlock manual |
| Required action pendente | Completar ação requerida |

**Exemplo no redirect:**
```
https://app.example.com/callback?
  error=access_denied&
  error_description=User+denied+access
```

### server_error

Erro interno do servidor.

| Causa | Solução |
|:------|:--------|
| Erro de database | Verificar conectividade PostgreSQL |
| Configuração inválida | Verificar logs do Keycloak |
| Timeout | Aumentar recursos ou otimizar queries |

### temporarily_unavailable

Servidor sobrecarregado ou em manutenção.

| Causa | Solução |
|:------|:--------|
| Alta carga | Implementar retry com backoff |
| Manutenção | Aguardar disponibilidade |

## Códigos HTTP

### 200 OK

Operação bem-sucedida.

### 201 Created

Recurso criado com sucesso. Header `Location` contém URL do novo recurso.

```http
HTTP/1.1 201 Created
Location: /admin/realms/carf/users/f47ac10b-58cc-4372-a567-0e02b2c3d479
```

### 204 No Content

Operação bem-sucedida sem corpo de resposta (DELETE, PUT).

### 400 Bad Request

Request inválido. Corpo contém detalhes do erro.

```json
{
  "error": "invalid_request",
  "error_description": "Missing parameter: username"
}
```

**Ação**: Validar payload antes de enviar, verificar campos obrigatórios.

### 401 Unauthorized

Token inválido, expirado ou ausente.

```json
{
  "error": "invalid_token",
  "error_description": "Token is not active"
}
```

**Ação**: Fazer refresh do token ou re-autenticar.

### 403 Forbidden

Token válido mas sem permissão para o recurso.

```json
{
  "error": "access_denied",
  "error_description": "User does not have permission"
}
```

**Ação**: Verificar roles do usuário, solicitar permissões adicionais.

### 404 Not Found

Recurso não existe.

```json
{
  "error": "User not found"
}
```

**Ação**: Verificar ID do recurso, criar se necessário.

### 409 Conflict

Conflito com estado atual (ex: username/email duplicado).

```json
{
  "errorMessage": "User exists with same username"
}
```

**Ação**: Usar valor único ou atualizar registro existente.

### 429 Too Many Requests

Rate limit excedido.

**Ação**: Implementar backoff exponencial.

```typescript
async function fetchWithRetry(url: string, options: RequestInit, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    const response = await fetch(url, options)

    if (response.status !== 429) {
      return response
    }

    const retryAfter = response.headers.get('Retry-After')
    const delay = retryAfter ? parseInt(retryAfter) * 1000 : Math.pow(2, i) * 1000

    await new Promise(resolve => setTimeout(resolve, delay))
  }

  throw new Error('Max retries exceeded')
}
```

### 500 Internal Server Error

Erro interno do Keycloak.

**Ação**: Verificar logs do servidor, reportar bug se persistir.

### 503 Service Unavailable

Servidor indisponível ou sobrecarregado.

**Ação**: Retry com backoff, verificar health endpoints.

## Mensagens de Erro de Autenticação

Mensagens exibidas na tela de login (internacionalizáveis via `messages_*.properties`).

| Chave | Mensagem (pt-BR) | Causa |
|:------|:-----------------|:------|
| `invalidUserMessage` | Usuário ou senha inválidos | Login falhou |
| `accountDisabledMessage` | Conta desabilitada | `enabled: false` |
| `accountTemporarilyDisabledMessage` | Conta temporariamente bloqueada | Brute force |
| `expiredCodeMessage` | Código expirado | Auth code ou action token |
| `sessionExpiredMessage` | Sessão expirada | SSO timeout |
| `invalidEmailMessage` | Email inválido | Validação de email |
| `missingPasswordMessage` | Senha não informada | Campo vazio |
| `notMatchPasswordMessage` | Senhas não conferem | Registro/reset |

## Tratamento de Erros no Frontend

```typescript
// hooks/use-auth.ts
import { useCallback } from 'react'

interface AuthError {
  error: string
  error_description?: string
}

export function useAuth() {
  const handleAuthError = useCallback((error: AuthError) => {
    switch (error.error) {
      case 'invalid_grant':
        // Token expirado, re-autenticar
        window.location.href = '/login'
        break

      case 'access_denied':
        // Sem permissão
        toast.error('Você não tem permissão para esta ação')
        break

      case 'invalid_client':
        // Erro de configuração
        console.error('Client configuration error:', error)
        toast.error('Erro de configuração. Contate o suporte.')
        break

      case 'invalid_scope':
        // Scope não permitido
        console.warn('Scope not allowed:', error)
        break

      default:
        toast.error(error.error_description || 'Erro de autenticação')
    }
  }, [])

  return { handleAuthError }
}
```

## Referências

- [OAuth 2.0 RFC 6749 - Error Codes](https://tools.ietf.org/html/rfc6749#section-5.2)
- [OpenID Connect Core - Error Codes](https://openid.net/specs/openid-connect-core-1_0.html#AuthError)
- [Keycloak Error Messages](https://github.com/keycloak/keycloak/tree/main/themes/src/main/resources/theme/base/login/messages)
