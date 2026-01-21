---
status: review
updated: 2026-01-21
---

# Endpoints de Autenticação

Especificação dos endpoints de autenticação do WEBDOCS que implementam fluxo OAuth2 Authorization Code com PKCE para integração com Keycloak.

## Visão Geral do Fluxo

O fluxo de autenticação segue padrão OAuth2 Authorization Code com PKCE para máxima segurança. Usuário inicia login, é redirecionado ao Keycloak, autentica, retorna com código, que é trocado por tokens salvos em cookies HttpOnly.

```json
{
  "flow": {
    "1": "Usuário clica em login",
    "2": "GET /auth/login gera PKCE e redireciona para Keycloak",
    "3": "Usuário autentica no Keycloak",
    "4": "Keycloak redireciona para /auth/callback com code",
    "5": "POST para Keycloak token endpoint troca code por tokens",
    "6": "Tokens salvos em cookies HttpOnly",
    "7": "Usuário redirecionado para página original"
  }
}
```

## GET /auth/login

Endpoint que inicia fluxo de autenticação gerando PKCE challenge e redirecionando para Keycloak.

```json
{
  "endpoint": "GET /auth/login",
  "path": "src/pages/auth/login.astro",
  "query_params": {
    "redirect": {
      "type": "string",
      "required": false,
      "default": "/",
      "description": "URL para retornar após login bem-sucedido",
      "validation": "Deve ser path relativo do mesmo domínio"
    }
  },
  "behavior": {
    "1_generate_pkce": {
      "code_verifier": "String aleatória de 43-128 caracteres",
      "code_challenge": "SHA256 hash do verifier, base64url encoded",
      "method": "S256"
    },
    "2_save_state": {
      "cookie": "carf_auth_state",
      "content": {
        "code_verifier": "Salvo para validação no callback",
        "redirect": "URL original para retorno",
        "state": "Valor aleatório para prevenir CSRF"
      },
      "options": {
        "httpOnly": true,
        "secure": true,
        "sameSite": "lax",
        "maxAge": 600,
        "path": "/auth"
      }
    },
    "3_redirect": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/auth",
      "params": {
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "redirect_uri": "${PUBLIC_SITE_URL}/auth/callback",
        "response_type": "code",
        "scope": "openid profile email",
        "code_challenge": "${code_challenge}",
        "code_challenge_method": "S256",
        "state": "${state}"
      }
    }
  },
  "response": {
    "success": "302 Redirect para Keycloak authorize endpoint",
    "error": "500 se falha ao gerar PKCE"
  }
}
```

## GET /auth/callback

Endpoint que recebe código do Keycloak e troca por tokens.

```json
{
  "endpoint": "GET /auth/callback",
  "path": "src/pages/auth/callback.astro",
  "query_params": {
    "code": {
      "type": "string",
      "required": true,
      "description": "Authorization code do Keycloak"
    },
    "state": {
      "type": "string",
      "required": true,
      "description": "Nonce para validação contra CSRF"
    },
    "error": {
      "type": "string",
      "description": "Código de erro se autenticação falhou"
    },
    "error_description": {
      "type": "string",
      "description": "Descrição do erro"
    }
  },
  "behavior": {
    "1_validate_state": {
      "action": "Ler cookie carf_auth_state e comparar state com query param",
      "error": "Redirect para /auth/login se não bater"
    },
    "2_check_error": {
      "action": "Se error param presente, exibir página de erro",
      "display": "Mensagem amigável baseada no error_description"
    },
    "3_exchange_code": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token",
      "method": "POST",
      "note": "Public client com PKCE - não usa client_secret",
      "body": {
        "grant_type": "authorization_code",
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "code": "${code}",
        "redirect_uri": "${PUBLIC_SITE_URL}/auth/callback",
        "code_verifier": "${code_verifier_from_cookie}"
      }
    },
    "4_save_tokens": {
      "access_token": {
        "cookie": "carf_access_token",
        "httpOnly": true,
        "secure": true,
        "sameSite": "lax",
        "path": "/",
        "maxAge": "expires_in do response"
      },
      "refresh_token": {
        "cookie": "carf_refresh_token",
        "httpOnly": true,
        "secure": true,
        "sameSite": "lax",
        "path": "/auth",
        "maxAge": "refresh_expires_in do response"
      }
    },
    "5_cleanup": {
      "action": "Deletar cookie carf_auth_state"
    },
    "6_redirect": {
      "action": "Redirect para URL salva no state ou /"
    }
  },
  "response": {
    "success": "302 Redirect para página original",
    "error_state": "302 Redirect para /auth/login",
    "error_exchange": "Página de erro com retry link"
  }
}
```

## POST /auth/logout

Endpoint que limpa tokens e redireciona para logout do Keycloak.

```json
{
  "endpoint": "POST /auth/logout",
  "path": "src/pages/auth/logout.ts",
  "behavior": {
    "1_clear_cookies": {
      "carf_access_token": "Deletar cookie setando maxAge=0",
      "carf_refresh_token": "Deletar cookie setando maxAge=0"
    },
    "2_redirect": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/logout",
      "params": {
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "post_logout_redirect_uri": "${PUBLIC_SITE_URL}"
      }
    }
  },
  "response": {
    "success": "302 Redirect para Keycloak logout"
  }
}
```

## POST /auth/refresh

Endpoint que renova access_token usando refresh_token.

```json
{
  "endpoint": "POST /auth/refresh",
  "path": "src/pages/api/refresh.ts",
  "behavior": {
    "1_read_refresh": {
      "action": "Ler carf_refresh_token do cookie",
      "error": "401 se cookie ausente"
    },
    "2_exchange": {
      "url": "${KEYCLOAK_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token",
      "method": "POST",
      "note": "Public client - não usa client_secret",
      "body": {
        "grant_type": "refresh_token",
        "client_id": "${KEYCLOAK_CLIENT_ID}",
        "refresh_token": "${refresh_token}"
      }
    },
    "3_update_cookies": {
      "action": "Atualizar carf_access_token e carf_refresh_token cookies com novos valores"
    }
  },
  "response": {
    "success": {
      "status": 200,
      "body": { "success": true, "expiresIn": "number" }
    },
    "error_missing": {
      "status": 401,
      "body": { "error": "no_refresh_token" }
    },
    "error_expired": {
      "status": 401,
      "body": { "error": "refresh_token_expired" }
    },
    "error_keycloak": {
      "status": 502,
      "body": { "error": "keycloak_unavailable" }
    }
  }
}
```

## GET /auth/cms

Endpoint especial para autenticação do Decap CMS via OAuth.

```json
{
  "endpoint": "GET /auth/cms",
  "path": "src/pages/auth/cms.astro",
  "description": "Proxy de autenticação para Decap CMS acessar GitHub",
  "behavior": {
    "flow": "OAuth implicit para GitHub via Decap backend",
    "reference": "Documentado em SPECS/15-decap-cms-overview.md"
  }
}
```

## Segurança

Todas as comunicações usam HTTPS em produção. Tokens são armazenados em cookies HttpOnly prevenindo acesso via JavaScript. Refresh token tem path restrito a /auth/ minimizando exposição. PKCE previne ataques de interceptação de código. State/nonce previne CSRF.

## Exemplos de Request/Response

### Login - Request

```http
GET /auth/login?redirect=/dev/middleware HTTP/1.1
Host: docs.carf.com.br
```

### Login - Response (Redirect para Keycloak)

```http
HTTP/1.1 302 Found
Location: https://auth.carf.com.br/realms/carf/protocol/openid-connect/auth?client_id=carf-webdocs&redirect_uri=https%3A%2F%2Fdocs.carf.com.br%2Fauth%2Fcallback&response_type=code&scope=openid%20profile%20email&code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&code_challenge_method=S256&state=af0ifjsldkj
Set-Cookie: carf_auth_state={"code_verifier":"dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk","state":"af0ifjsldkj","redirect_to":"/dev/middleware","created_at":1705766400000}; HttpOnly; Secure; SameSite=Lax; Path=/auth; Max-Age=600
```

### Callback - Request (Vindo do Keycloak)

```http
GET /auth/callback?code=SplxlOBeZQQYbYS6WxSbIA&state=af0ifjsldkj HTTP/1.1
Host: docs.carf.com.br
Cookie: carf_auth_state={"code_verifier":"dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk","state":"af0ifjsldkj","redirect_to":"/dev/middleware","created_at":1705766400000}
```

### Callback - Token Exchange (Server-to-Server)

```http
POST /realms/carf/protocol/openid-connect/token HTTP/1.1
Host: auth.carf.com.br
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&client_id=carf-webdocs&code=SplxlOBeZQQYbYS6WxSbIA&redirect_uri=https%3A%2F%2Fdocs.carf.com.br%2Fauth%2Fcallback&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

### Callback - Token Response do Keycloak

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjEifQ.eyJleHAiOjE3MDU3NjY3MDAsImlhdCI6MTcwNTc2NjQwMCwianRpIjoiYWJjMTIzIiwiaXNzIjoiaHR0cHM6Ly9hdXRoLmNhcmYuY29tLmJyL3JlYWxtcy9jYXJmIiwic3ViIjoiMTIzNDU2Nzg5MCIsInR5cCI6IkJlYXJlciIsImF6cCI6ImNhcmYtd2ViZG9jcyIsInNlc3Npb25fc3RhdGUiOiJzZXNzaW9uMTIzIiwiZW1haWwiOiJ1c2VyQGV4YW1wbGUuY29tIiwibmFtZSI6IkpvYW8gU2lsdmEiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJqb2FvLnNpbHZhIiwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbImFuYWx5c3QiLCJkZXYiXX0sInRlbmFudF9pZCI6InRlbmFudC0xMjMifQ.signature",
  "expires_in": 300,
  "refresh_expires_in": 28800,
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDU3OTUyMDAsImlhdCI6MTcwNTc2NjQwMCwianRpIjoicmVmcmVzaDEyMyIsImlzcyI6Imh0dHBzOi8vYXV0aC5jYXJmLmNvbS5ici9yZWFsbXMvY2FyZiIsInR5cCI6IlJlZnJlc2giLCJzZXNzaW9uX3N0YXRlIjoic2Vzc2lvbjEyMyJ9.signature",
  "token_type": "Bearer",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "not-before-policy": 0,
  "session_state": "session123",
  "scope": "openid profile email"
}
```

### Callback - Response (Sucesso)

```http
HTTP/1.1 302 Found
Location: /dev/middleware
Set-Cookie: carf_access_token=eyJhbGciOiJSUzI1NiIs...; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=300
Set-Cookie: carf_refresh_token=eyJhbGciOiJIUzI1NiIs...; HttpOnly; Secure; SameSite=Lax; Path=/auth; Max-Age=28800
Set-Cookie: carf_auth_state=; HttpOnly; Secure; SameSite=Lax; Path=/auth; Max-Age=0
```

### Callback - Error Response (State Mismatch)

```http
HTTP/1.1 302 Found
Location: /auth/login?error=state_mismatch&message=Sessão%20expirada.%20Tente%20novamente.
```

### Refresh - Request

```http
POST /auth/refresh HTTP/1.1
Host: docs.carf.com.br
Cookie: carf_refresh_token=eyJhbGciOiJIUzI1NiIs...
```

### Refresh - Success Response

```http
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: carf_access_token=eyJhbGciOiJSUzI1NiIs...(novo); HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=300
Set-Cookie: carf_refresh_token=eyJhbGciOiJIUzI1NiIs...(novo); HttpOnly; Secure; SameSite=Lax; Path=/auth; Max-Age=28800

{
  "success": true,
  "expiresIn": 300
}
```

### Refresh - Error Responses

```json
// 401 - No refresh token
{
  "error": "no_refresh_token",
  "message": "Refresh token não encontrado. Faça login novamente."
}

// 401 - Refresh token expired
{
  "error": "refresh_token_expired",
  "message": "Sessão expirada. Faça login novamente."
}

// 502 - Keycloak unavailable
{
  "error": "keycloak_unavailable",
  "message": "Serviço de autenticação indisponível. Tente novamente em alguns minutos."
}
```

### Logout - Request

```http
POST /auth/logout HTTP/1.1
Host: docs.carf.com.br
Cookie: carf_access_token=eyJhbGciOiJSUzI1NiIs...
```

### Logout - Response

```http
HTTP/1.1 302 Found
Location: https://auth.carf.com.br/realms/carf/protocol/openid-connect/logout?client_id=carf-webdocs&post_logout_redirect_uri=https%3A%2F%2Fdocs.carf.com.br%2F
Set-Cookie: carf_access_token=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0
Set-Cookie: carf_refresh_token=; HttpOnly; Secure; SameSite=Lax; Path=/auth; Max-Age=0
```

## Timing e Retry

```json
{
  "timing": {
    "token_exchange": {
      "timeout": 10000,
      "retry_on_5xx": true,
      "max_retries": 2,
      "backoff": "exponential"
    },
    "refresh": {
      "timeout": 5000,
      "retry_on_5xx": true,
      "max_retries": 1
    }
  },
  "error_handling": {
    "keycloak_timeout": "Mostrar página de erro com retry button",
    "keycloak_5xx": "Retry automático com backoff",
    "keycloak_4xx": "Redirect para login (credenciais inválidas)"
  }
}
```

## JWT Payload Exemplo

Access token decodificado (payload):

```json
{
  "exp": 1705766700,
  "iat": 1705766400,
  "jti": "abc123",
  "iss": "https://auth.carf.com.br/realms/carf",
  "sub": "1234567890",
  "typ": "Bearer",
  "azp": "carf-webdocs",
  "session_state": "session123",
  "email": "user@example.com",
  "name": "Joao Silva",
  "preferred_username": "joao.silva",
  "realm_access": {
    "roles": ["analyst", "dev"]
  },
  "tenant_id": "tenant-123"
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
