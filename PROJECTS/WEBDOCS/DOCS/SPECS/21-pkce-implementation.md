---
status: review
updated: 2026-01-21
---

# PKCE Implementation

Proof Key for Code Exchange (PKCE) é extensão do OAuth 2.0 que protege contra ataques de interceptação de código de autorização. Obrigatório para public clients como WEBDOCS que não podem manter client_secret seguro.

## Visão Geral do Fluxo

```json
{
  "pkce_flow": {
    "step_1": {
      "action": "Gerar code_verifier",
      "description": "String aleatória de 43-128 caracteres",
      "storage": "Cookie httpOnly temporário"
    },
    "step_2": {
      "action": "Gerar code_challenge",
      "description": "SHA256 hash do verifier, base64url encoded",
      "send_to": "Authorization endpoint"
    },
    "step_3": {
      "action": "Usuário autentica no Keycloak",
      "result": "Redirect para callback com code"
    },
    "step_4": {
      "action": "Trocar code por tokens",
      "send": "code + code_verifier",
      "validation": "Keycloak verifica SHA256(verifier) == challenge"
    }
  }
}
```

## Implementação com Web Crypto API

### Gerar Code Verifier

```json
{
  "code_verifier": {
    "charset": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~",
    "length": {
      "min": 43,
      "max": 128,
      "recommended": 64
    },
    "algorithm": {
      "implementation": "Web Crypto API getRandomValues",
      "steps": [
        "1. Criar Uint8Array de 64 bytes",
        "2. Preencher com crypto.getRandomValues()",
        "3. Mapear cada byte para charset[byte % charset.length]",
        "4. Juntar em string"
      ]
    }
  }
}
```

Pseudocódigo TypeScript:

```typescript
// src/lib/auth/pkce.ts
function generateCodeVerifier(): string {
  const charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
  const randomBytes = new Uint8Array(64);
  crypto.getRandomValues(randomBytes);
  return Array.from(randomBytes)
    .map(byte => charset[byte % charset.length])
    .join('');
}
```

### Gerar Code Challenge

```json
{
  "code_challenge": {
    "method": "S256",
    "algorithm": {
      "steps": [
        "1. Converter verifier para Uint8Array (UTF-8)",
        "2. Calcular SHA-256 hash",
        "3. Converter hash para base64url (sem padding)"
      ]
    },
    "base64url": {
      "replace": {
        "+": "-",
        "/": "_"
      },
      "remove": "= (padding)"
    }
  }
}
```

Pseudocódigo TypeScript:

```typescript
// src/lib/auth/pkce.ts
async function generateCodeChallenge(verifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest('SHA-256', data);
  const base64 = btoa(String.fromCharCode(...new Uint8Array(digest)));
  return base64
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');
}
```

## Storage do State e Verifier

```json
{
  "storage": {
    "cookie_name": "carf_auth_state",
    "cookie_config": {
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax",
      "path": "/auth",
      "maxAge": 600
    },
    "payload": {
      "state": "string - CSRF protection",
      "code_verifier": "string - PKCE verifier",
      "redirect_to": "string - URL original do usuário",
      "created_at": "number - timestamp para expiração"
    },
    "encoding": "JSON.stringify + base64url (não criptografado)"
  }
}
```

Pseudocódigo TypeScript:

```typescript
// src/lib/auth/state.ts
interface AuthState {
  state: string;
  code_verifier: string;
  redirect_to: string;
  created_at: number;
}

function generateState(): string {
  const randomBytes = new Uint8Array(32);
  crypto.getRandomValues(randomBytes);
  return Array.from(randomBytes)
    .map(b => b.toString(16).padStart(2, '0'))
    .join('');
}

function createAuthStateCookie(redirectTo: string): { cookie: string; state: string; codeChallenge: string } {
  const state = generateState();
  const codeVerifier = generateCodeVerifier();
  const codeChallenge = await generateCodeChallenge(codeVerifier);

  const payload: AuthState = {
    state,
    code_verifier: codeVerifier,
    redirect_to: redirectTo,
    created_at: Date.now()
  };

  const encoded = btoa(JSON.stringify(payload))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=/g, '');

  return {
    cookie: `carf_auth_state=${encoded}; HttpOnly; Secure; SameSite=Lax; Path=/auth; Max-Age=600`,
    state,
    codeChallenge
  };
}
```

## Fluxo Completo: Login

```json
{
  "login_flow": {
    "endpoint": "GET /auth/login",
    "query_params": {
      "redirect": "URL para retornar após login (opcional, default: /)"
    },
    "steps": [
      {
        "step": 1,
        "action": "Gerar code_verifier (64 chars)",
        "output": "string aleatória"
      },
      {
        "step": 2,
        "action": "Gerar code_challenge (SHA256 base64url)",
        "output": "hash do verifier"
      },
      {
        "step": 3,
        "action": "Gerar state (32 bytes hex)",
        "output": "string para CSRF protection"
      },
      {
        "step": 4,
        "action": "Salvar em cookie",
        "cookie": "carf_auth_state com verifier, state, redirect_to"
      },
      {
        "step": 5,
        "action": "Redirect para Keycloak",
        "url": "authorization_endpoint com params"
      }
    ]
  }
}
```

Authorization URL completa:

```json
{
  "authorization_url": {
    "base": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/auth",
    "params": {
      "client_id": "carf-webdocs",
      "redirect_uri": "https://docs.carf.com.br/auth/callback",
      "response_type": "code",
      "scope": "openid profile email",
      "state": "<GENERATED_STATE>",
      "code_challenge": "<GENERATED_CHALLENGE>",
      "code_challenge_method": "S256"
    }
  }
}
```

## Fluxo Completo: Callback

```json
{
  "callback_flow": {
    "endpoint": "GET /auth/callback",
    "query_params": {
      "code": "authorization code do Keycloak",
      "state": "state enviado no login"
    },
    "steps": [
      {
        "step": 1,
        "action": "Ler cookie carf_auth_state",
        "validation": "Cookie deve existir e não estar expirado"
      },
      {
        "step": 2,
        "action": "Validar state",
        "validation": "query.state === cookie.state"
      },
      {
        "step": 3,
        "action": "Trocar code por tokens",
        "request": "POST token_endpoint com code e code_verifier"
      },
      {
        "step": 4,
        "action": "Salvar tokens em cookies",
        "cookies": "carf_access_token, carf_refresh_token"
      },
      {
        "step": 5,
        "action": "Deletar cookie de state",
        "reason": "One-time use"
      },
      {
        "step": 6,
        "action": "Redirect para redirect_to",
        "url": "URL original do usuário"
      }
    ]
  }
}
```

Token Exchange Request:

```json
{
  "token_request": {
    "method": "POST",
    "url": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/token",
    "headers": {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    "body": {
      "grant_type": "authorization_code",
      "client_id": "carf-webdocs",
      "code": "<AUTHORIZATION_CODE>",
      "redirect_uri": "https://docs.carf.com.br/auth/callback",
      "code_verifier": "<CODE_VERIFIER_FROM_COOKIE>"
    }
  }
}
```

Token Response:

```json
{
  "token_response": {
    "access_token": "eyJhbGciOiJSUzI1NiIs...",
    "expires_in": 300,
    "refresh_expires_in": 28800,
    "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer",
    "id_token": "eyJhbGciOiJSUzI1NiIs...",
    "not-before-policy": 0,
    "session_state": "uuid",
    "scope": "openid profile email"
  }
}
```

## Timing e Expiração

```json
{
  "timing": {
    "auth_state_cookie": {
      "max_age": 600,
      "reason": "10 minutos para completar login"
    },
    "code_validity": {
      "keycloak_default": 60,
      "reason": "1 minuto para trocar por tokens"
    },
    "access_token": {
      "expires_in": 300,
      "reason": "5 minutos - curto para segurança"
    },
    "refresh_token": {
      "expires_in": 28800,
      "reason": "8 horas - sessão de trabalho"
    }
  }
}
```

## Tratamento de Erros

```json
{
  "error_handling": {
    "state_mismatch": {
      "cause": "CSRF attack ou cookie expirado",
      "action": "Redirect para /auth/login com mensagem",
      "log": "Warning - potential CSRF attempt"
    },
    "code_expired": {
      "cause": "Usuário demorou para autorizar",
      "action": "Redirect para /auth/login",
      "message": "Sessão expirada. Tente novamente."
    },
    "invalid_grant": {
      "cause": "Code já usado ou verifier incorreto",
      "action": "Redirect para /auth/login",
      "message": "Erro de autenticação. Tente novamente."
    },
    "cookie_missing": {
      "cause": "Cookie deletado ou third-party cookies bloqueados",
      "action": "Redirect para /auth/login",
      "message": "Cookies necessários para autenticação."
    }
  }
}
```

## Segurança

```json
{
  "security_considerations": {
    "pkce_protection": "Previne code interception attacks",
    "state_protection": "Previne CSRF attacks",
    "httponly_cookies": "Previne XSS access ao verifier",
    "short_lived_state": "Minimiza window of attack",
    "one_time_use": "State/verifier usados apenas uma vez"
  },
  "do_not": [
    "Armazenar code_verifier em localStorage",
    "Usar method=plain (sempre usar S256)",
    "Reutilizar state ou verifier",
    "Aceitar state sem validação"
  ]
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
