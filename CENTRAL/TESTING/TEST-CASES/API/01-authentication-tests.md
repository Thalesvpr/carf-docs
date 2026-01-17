# Authentication API Tests

Casos de teste para endpoints de autenticação.

## Login Endpoint

### TC-AUTH-001: Login com credenciais válidas

```gherkin
Cenário: Usuário faz login com credenciais válidas
  Dado que existe um usuário "joao@test.com" com senha "Test123!"
  E o usuário tem acesso ao tenant "tenant-123"
  Quando envio POST /api/auth/login com:
    | username | joao@test.com |
    | password | Test123!      |
    | tenant_id | tenant-123   |
  Então recebo status 200
  E a resposta contém "access_token"
  E a resposta contém "refresh_token"
  E "expires_in" é maior que 0
  E o JWT contém claim "tenant_id" = "tenant-123"
```

### TC-AUTH-002: Login com senha incorreta

```gherkin
Cenário: Login com senha incorreta retorna 401
  Dado que existe um usuário "joao@test.com"
  Quando envio POST /api/auth/login com:
    | username | joao@test.com |
    | password | SenhaErrada   |
  Então recebo status 401
  E a resposta contém "error" = "invalid_credentials"
```

### TC-AUTH-003: Login com usuário inexistente

```gherkin
Cenário: Login com usuário inexistente retorna 401
  Quando envio POST /api/auth/login com:
    | username | naoexiste@test.com |
    | password | QualquerSenha      |
  Então recebo status 401
  E a resposta contém "error" = "invalid_credentials"
```

### TC-AUTH-004: Login sem acesso ao tenant

```gherkin
Cenário: Login em tenant não autorizado retorna 403
  Dado que existe um usuário "joao@test.com"
  E o usuário NÃO tem acesso ao tenant "outro-tenant"
  Quando envio POST /api/auth/login com:
    | username | joao@test.com |
    | tenant_id | outro-tenant |
  Então recebo status 403
  E a resposta contém "error" = "tenant_access_denied"
```

### TC-AUTH-005: Conta bloqueada após tentativas

```gherkin
Cenário: Conta é bloqueada após 5 tentativas falhas
  Dado que existe um usuário "joao@test.com"
  Quando envio 5 requisições POST /api/auth/login com senha incorreta
  E envio POST /api/auth/login com a senha correta
  Então recebo status 423
  E a resposta contém "error" = "account_locked"
```

## Refresh Token Endpoint

### TC-AUTH-010: Refresh token válido

```gherkin
Cenário: Refresh token renova access token
  Dado que tenho um refresh_token válido
  Quando envio POST /api/auth/refresh com:
    | refresh_token | {token_valido} |
  Então recebo status 200
  E a resposta contém novo "access_token"
  E a resposta contém novo "refresh_token"
```

### TC-AUTH-011: Refresh token expirado

```gherkin
Cenário: Refresh token expirado retorna 401
  Dado que tenho um refresh_token expirado
  Quando envio POST /api/auth/refresh com:
    | refresh_token | {token_expirado} |
  Então recebo status 401
  E a resposta contém "error" = "token_expired"
```

## Logout Endpoint

### TC-AUTH-020: Logout revoga tokens

```gherkin
Cenário: Logout revoga refresh token
  Dado que estou autenticado com access_token e refresh_token
  Quando envio POST /api/auth/logout com:
    | refresh_token | {meu_refresh_token} |
  Então recebo status 204
  E o refresh_token não pode mais ser usado
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
