---
type: leaf
status: review
updated: 2026-01-21
---

# Autenticação

WEBDOCS integra com Keycloak para autenticação de usuários que acessam seção protegida /dev/ e CMS administrativo. Client carf-webdocs configurado como public client usa Authorization Code flow com PKCE.

Fluxo de login inicia quando usuário não autenticado acessa rota protegida. Middleware redireciona para Keycloak /authorize com parâmetros client_id, redirect_uri apontando para /auth/callback, response_type code, code_challenge gerado com S256, e state para proteção CSRF.

Callback em /auth/callback.astro processa response do Keycloak. Código de autorização é trocado por tokens via POST /token incluindo code_verifier do PKCE. Access token e refresh token são armazenados em cookie HTTP-only com flags Secure e SameSite Strict.

Sessão é mantida via cookie carf-session contendo tokens criptografados. Cookie HTTP-only previne acesso via JavaScript protegendo contra XSS. Expiração do cookie alinhada com refresh token (30 minutos idle, 8 horas max).

Refresh silencioso acontece quando access token expira (5 minutos). Middleware detecta token expirado, executa refresh via POST /token com grant_type refresh_token, e atualiza cookies com novos tokens. Processo transparente para usuário.

Logout em /auth/logout invalida sessão local deletando cookies e redireciona para Keycloak /logout com post_logout_redirect_uri. Logout completo do SSO invalida sessão em todas aplicações CARF.

Decap CMS usa mesmo fluxo OAuth com redirect para /admin/callback. Após autenticação, CMS recebe token para autenticar chamadas à GitHub API permitindo commits de edições.

## Especificação de Cookies

```json
{
  "cookie_security": {
    "carf_access_token": {
      "name": "carf_access_token",
      "content": "JWT access token do Keycloak",
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax",
      "path": "/",
      "maxAge": 300,
      "maxAge_description": "5 minutos - igual ao expires_in do token"
    },
    "carf_refresh_token": {
      "name": "carf_refresh_token",
      "content": "Refresh token do Keycloak",
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax",
      "path": "/auth",
      "maxAge": 28800,
      "maxAge_description": "8 horas - sessão de trabalho"
    },
    "carf_auth_state": {
      "name": "carf_auth_state",
      "content": "JSON com code_verifier, state, redirect_to",
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax",
      "path": "/auth",
      "maxAge": 600,
      "maxAge_description": "10 minutos - tempo para completar login"
    }
  }
}
```

### Flags de Segurança Explicadas

```json
{
  "security_flags": {
    "httpOnly": {
      "value": true,
      "reason": "Previne acesso via JavaScript - proteção contra XSS",
      "required": "OBRIGATÓRIO para tokens"
    },
    "secure": {
      "value": true,
      "reason": "Cookie só enviado via HTTPS",
      "dev_note": "Pode ser false em localhost HTTP"
    },
    "sameSite": {
      "value": "Lax",
      "reason": "Enviado em navegação top-level, não em requests cross-site",
      "alternative": "Strict bloquearia login vindo de links externos"
    },
    "path": {
      "access_token": "/",
      "refresh_token": "/auth",
      "reason": "Refresh token só precisa ser enviado para rotas /auth/*"
    }
  }
}
```

### Implementação de Cookies

```typescript
// src/lib/auth/cookies.ts
import type { AstroCookies } from 'astro';

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
  refresh_expires_in: number;
}

export function setAuthCookies(
  cookies: AstroCookies,
  tokens: TokenResponse,
  isProduction: boolean
): void {
  cookies.set('carf_access_token', tokens.access_token, {
    httpOnly: true,
    secure: isProduction,
    sameSite: 'lax',
    path: '/',
    maxAge: tokens.expires_in
  });

  cookies.set('carf_refresh_token', tokens.refresh_token, {
    httpOnly: true,
    secure: isProduction,
    sameSite: 'lax',
    path: '/auth',
    maxAge: tokens.refresh_expires_in
  });
}

export function clearAuthCookies(cookies: AstroCookies): void {
  cookies.delete('carf_access_token', { path: '/' });
  cookies.delete('carf_refresh_token', { path: '/auth' });
}

export function setAuthStateCookie(
  cookies: AstroCookies,
  state: { codeVerifier: string; state: string; redirectTo: string },
  isProduction: boolean
): void {
  const payload = JSON.stringify({
    code_verifier: state.codeVerifier,
    state: state.state,
    redirect_to: state.redirectTo,
    created_at: Date.now()
  });

  cookies.set('carf_auth_state', payload, {
    httpOnly: true,
    secure: isProduction,
    sameSite: 'lax',
    path: '/auth',
    maxAge: 600
  });
}

export function getAuthState(cookies: AstroCookies): {
  codeVerifier: string;
  state: string;
  redirectTo: string;
} | null {
  const cookie = cookies.get('carf_auth_state')?.value;
  if (!cookie) return null;

  try {
    const parsed = JSON.parse(cookie);
    return {
      codeVerifier: parsed.code_verifier,
      state: parsed.state,
      redirectTo: parsed.redirect_to
    };
  } catch {
    return null;
  }
}
```

## Validação JWT

```json
{
  "jwt_validation": {
    "library": "jose",
    "method": "jwtVerify com JWKS",
    "jwks_endpoint": "https://auth.carf.com.br/realms/carf/protocol/openid-connect/certs",
    "issuer_validation": "https://auth.carf.com.br/realms/carf",
    "claims_extracted": [
      "sub (user id)",
      "email",
      "name",
      "preferred_username",
      "realm_access.roles",
      "tenant_id"
    ]
  }
}
```

### Validação Completa

```typescript
// src/lib/auth/jwt.ts
import { jwtVerify, createRemoteJWKSet, type JWTPayload } from 'jose';

interface UserClaims {
  id: string;
  email: string;
  name: string;
  roles: string[];
  tenantId: string | null;
}

let jwksCache: ReturnType<typeof createRemoteJWKSet> | null = null;

function getJWKS(): ReturnType<typeof createRemoteJWKSet> {
  if (!jwksCache) {
    const url = new URL(
      `${import.meta.env.KEYCLOAK_URL}/realms/${import.meta.env.KEYCLOAK_REALM}/protocol/openid-connect/certs`
    );
    jwksCache = createRemoteJWKSet(url);
  }
  return jwksCache;
}

export async function validateToken(token: string): Promise<UserClaims | null> {
  try {
    const { payload } = await jwtVerify(token, getJWKS(), {
      issuer: `${import.meta.env.KEYCLOAK_URL}/realms/${import.meta.env.KEYCLOAK_REALM}`
    });

    const realmAccess = payload.realm_access as { roles: string[] } | undefined;

    return {
      id: payload.sub as string,
      email: payload.email as string,
      name: (payload.name as string) || (payload.preferred_username as string),
      roles: realmAccess?.roles || [],
      tenantId: (payload.tenant_id as string) || null
    };
  } catch (error) {
    // Token inválido, expirado ou assinatura não confere
    return null;
  }
}

export function invalidateJWKSCache(): void {
  jwksCache = null;
}
```

## Fluxo de Refresh Token

```json
{
  "refresh_flow": {
    "trigger": "Access token expirado (5 min)",
    "detection": "Middleware verifica exp claim ou jwtVerify falha",
    "process": [
      "1. Ler refresh_token do cookie",
      "2. POST para Keycloak token endpoint",
      "3. Receber novos access_token e refresh_token",
      "4. Atualizar ambos cookies",
      "5. Retry da request original"
    ],
    "failure_handling": {
      "refresh_expired": "Redirect para login",
      "refresh_revoked": "Redirect para login",
      "keycloak_unavailable": "Retry com backoff ou erro 503"
    }
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
