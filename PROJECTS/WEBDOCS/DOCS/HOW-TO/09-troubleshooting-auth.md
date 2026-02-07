---
type: leaf
status: review
updated: 2026-01-21
---

# Troubleshooting - Autenticação

Resolução de problemas de autenticação e CORS.

Arquivos relacionados:
- Problemas de build: `09-troubleshooting-build.md`
- Problemas de runtime: `09-troubleshooting-runtime.md`

## Login Redirect Loop

**Sintoma:** Usuário é redirecionado infinitamente entre WEBDOCS e Keycloak.

```json
{
  "problem": "redirect_loop",
  "symptoms": [
    "Browser mostra 'too many redirects'",
    "URL alterna entre /auth/login e Keycloak",
    "Cookies não são persistidos"
  ]
}
```

**Causas e Soluções:**

```json
{
  "cause_1": {
    "description": "Cookie não está sendo salvo",
    "check": "DevTools > Application > Cookies",
    "solutions": [
      "Verificar se Secure=true apenas em HTTPS",
      "Em localhost, usar Secure=false ou HTTPS local",
      "Verificar SameSite não é 'Strict' (usar 'Lax')"
    ]
  },
  "cause_2": {
    "description": "Redirect URI não cadastrada no Keycloak",
    "check": "Keycloak Admin > Clients > carf-webdocs > Valid Redirect URIs",
    "solutions": [
      "Adicionar http://localhost:4321/auth/callback",
      "Adicionar URL exata incluindo porta"
    ]
  },
  "cause_3": {
    "description": "State mismatch",
    "check": "Console do browser por erro 'state mismatch'",
    "solutions": [
      "Limpar todos cookies do domínio",
      "Verificar se cookie carf_auth_state está sendo salvo",
      "Aumentar Max-Age do cookie de state"
    ]
  }
}
```

## Token Expired Errors

**Sintoma:** Usuário autenticado recebe erro 401 após alguns minutos.

```json
{
  "problem": "token_expired",
  "symptoms": [
    "401 Unauthorized em API calls",
    "Usuário é deslogado inesperadamente",
    "Console mostra 'token expired'"
  ]
}
```

**Soluções:**

```json
{
  "solution_1": {
    "description": "Implementar refresh automático",
    "code_location": "src/middleware.ts",
    "action": "Verificar expiração e chamar /auth/refresh antes de expirar"
  },
  "solution_2": {
    "description": "Aumentar token lifetime no Keycloak",
    "location": "Keycloak > Realm Settings > Tokens",
    "values": {
      "Access Token Lifespan": "300 (5 min) ou mais",
      "SSO Session Idle": "1800 (30 min)"
    }
  },
  "solution_3": {
    "description": "Forçar re-login",
    "action": "Redirect para /auth/login quando refresh falha"
  }
}
```

## 403 Forbidden em Seção Permitida

**Sintoma:** Usuário com role correta recebe 403.

```json
{
  "problem": "forbidden_wrong_role",
  "debug_steps": [
    "1. Verificar roles no JWT: jwt.io para decodificar",
    "2. Verificar claim realm_access.roles existe",
    "3. Verificar mapeamento de roles no middleware",
    "4. Verificar herança de roles está implementada"
  ]
}
```

**Verificação de JWT:**

```bash
# Copiar access_token do cookie e decodificar
# Em jwt.io ou via código:

# Payload esperado:
{
  "realm_access": {
    "roles": ["user", "field-coordinator"]
  },
  "tenant_id": "uuid-do-tenant"
}
```

## Problemas de CORS

### Erro de CORS em Fetch para API

**Sintoma:** `Access-Control-Allow-Origin` error no console.

```json
{
  "problem": "cors_error",
  "symptoms": [
    "Fetch failed: CORS policy",
    "No 'Access-Control-Allow-Origin' header"
  ]
}
```

**Soluções:**

```json
{
  "keycloak_cors": {
    "location": "Keycloak > Clients > carf-webdocs > Web Origins",
    "add": [
      "http://localhost:4321",
      "https://docs.carf.com.br"
    ]
  },
  "geoapi_cors": {
    "location": "GeoAPI appsettings.json ou Program.cs",
    "add_origin": "https://docs.carf.com.br"
  },
  "proxy_solution": {
    "description": "Usar API route do Astro como proxy",
    "example": "/api/proxy/[...path].ts proxies para GeoAPI"
  }
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
