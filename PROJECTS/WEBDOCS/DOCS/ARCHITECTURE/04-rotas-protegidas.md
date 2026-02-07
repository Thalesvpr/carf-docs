---
type: leaf
status: review
updated: 2026-01-21
---

# Rotas Protegidas

Todas as rotas do WEBDOCS são protegidas e requerem autenticação. O middleware de autorização em src/middleware.ts verifica autenticação e roles do usuário antes de renderizar qualquer conteúdo, controlando acesso às diferentes seções do portal baseado na hierarquia RBAC definida em PROJECTS/KEYCLOAK/DOCS/INTEGRATION/RBAC/.

## Hierarquia de Roles

O sistema CARF define seis roles com permissões de visualização específicas no WEBDOCS. A hierarquia segue modelo de herança onde roles superiores incluem permissões das inferiores, exceto a role dev que é transversal.

```json
{
  "roles": {
    "user": {
      "description": "Usuário padrão com acesso a documentação básica",
      "sections": ["guia"],
      "inherits": null
    },
    "field-cadastrator": {
      "description": "Cadastrador de campo com acesso restrito a mapa e formularios",
      "sections": ["guia", "manuais"],
      "inherits": "user"
    },
    "field-coordinator": {
      "description": "Coordenador de campo com menu mobile completo e supervisao",
      "sections": ["guia", "manuais"],
      "inherits": "field-cadastrator"
    },
    "analyst": {
      "description": "Analista REURB com acesso ao sistema e relatórios",
      "sections": ["guia", "sistema", "manuais"],
      "inherits": "field-coordinator"
    },
    "admin": {
      "description": "Administrador de tenant com acesso a status e changelog",
      "sections": ["guia", "sistema", "manuais", "status", "changelog"],
      "inherits": "analyst"
    },
    "super-admin": {
      "description": "Super administrador multi-tenant com acesso à API",
      "sections": ["guia", "sistema", "manuais", "api", "status", "changelog"],
      "inherits": "admin"
    },
    "dev": {
      "description": "Desenvolvedor com acesso total incluindo seção dev",
      "sections": ["guia", "sistema", "manuais", "api", "dev", "status", "changelog"],
      "inherits": null,
      "note": "Role transversal - pode ser combinada com qualquer role operacional"
    }
  }
}
```

A role dev é transversal e não participa da hierarquia de herança. Deve ser atribuída explicitamente e pode ser combinada com qualquer role operacional. Um usuário com role analyst e dev terá acesso tanto às seções de analyst quanto à seção dev.

## Mapeamento Rota para Seção

Cada rota do portal é mapeada para uma seção que determina quais roles podem acessá-la. O mapeamento é simples e baseado no primeiro segmento do path.

```json
{
  "routeMapping": {
    "/guia/*": "guia",
    "/sistema/*": "sistema",
    "/manuais/*": "manuais",
    "/api/*": "api",
    "/dev/*": "dev",
    "/status/*": "status",
    "/changelog/*": "changelog"
  }
}
```

## Lógica do Middleware

O middleware executa em toda requisição seguindo fluxo sequencial de verificação. Primeiro verifica presença do cookie access_token. Se ausente, redireciona para /auth/login preservando URL original no parâmetro redirect para retorno após autenticação.

Se cookie presente, decodifica o JWT sem validar assinatura no edge (validação completa acontece apenas para operações sensíveis). Extrai roles do claim realm_access.roles que contém array com todas roles atribuídas ao usuário no Keycloak.

Determina a seção da rota atual baseado no mapeamento acima. Verifica se alguma das roles do usuário permite acesso à seção, considerando herança. Se nenhuma role permitir acesso, retorna página 403 com explicação e sugestão de contato com administrador.

Se token expirado (claim exp menor que timestamp atual), tenta refresh silencioso usando refresh_token. Se refresh falhar por token revogado ou sessão expirada, redireciona para login.

## Cookies Esperados

```json
{
  "cookies": {
    "access_token": {
      "httpOnly": true,
      "secure": true,
      "sameSite": "lax",
      "path": "/",
      "description": "JWT de acesso para autenticação"
    },
    "refresh_token": {
      "httpOnly": true,
      "secure": true,
      "sameSite": "lax",
      "path": "/auth",
      "description": "Token para renovação do access_token"
    }
  }
}
```

O cookie access_token é enviado em todas requisições (path /) enquanto refresh_token é enviado apenas para rotas /auth/* onde a renovação acontece, minimizando exposição.

## Tratamento de Erros

Usuário não autenticado recebe redirect 302 para /auth/login?redirect={url_atual} preservando destino original. Após login bem-sucedido, callback redireciona para URL preservada.

Usuário autenticado sem permissão recebe página 403 customizada renderizada pelo Astro com explicação clara de que a seção requer permissão específica, lista das roles que teriam acesso, e link para logout ou retorno à home.

Token expirado dispara tentativa de refresh silencioso antes de qualquer resposta de erro. Sucesso no refresh é transparente ao usuário. Falha no refresh resulta em redirect para login com mensagem de sessão expirada.

## Performance

Validação de assinatura JWT usa chave pública obtida do Keycloak JWKS endpoint. Cache da chave pública é mantido por 24 horas ou até falha de validação indicando possível rotação de chaves. Decodificação do JWT no edge não valida assinatura para reduzir latência, confiando no httpOnly do cookie para integridade.

## Implementação do Middleware

### Arquivo e Exports

```json
{
  "middleware": {
    "file": "src/middleware.ts",
    "export": "onRequest",
    "type": "MiddlewareHandler from astro:middleware"
  }
}
```

### Astro Locals

O middleware popula `Astro.locals` com informações do usuário autenticado para uso em páginas e componentes:

```typescript
// src/env.d.ts
declare namespace App {
  interface Locals {
    user: {
      id: string;
      email: string;
      name: string;
      roles: string[];
      tenantId: string | null;
    } | null;
    isAuthenticated: boolean;
    allowedRoles?: string[]; // Populado em caso de 403
  }
}
```

### Estrutura Completa do Middleware

```typescript
// src/middleware.ts
import { defineMiddleware, sequence } from 'astro:middleware';
import { jwtVerify, createRemoteJWKSet } from 'jose';

// Cache do JWKS
let jwksCache: ReturnType<typeof createRemoteJWKSet> | null = null;

function getJWKS() {
  if (!jwksCache) {
    const jwksUrl = new URL(
      `${import.meta.env.KEYCLOAK_URL}/realms/${import.meta.env.KEYCLOAK_REALM}/protocol/openid-connect/certs`
    );
    jwksCache = createRemoteJWKSet(jwksUrl);
  }
  return jwksCache;
}

// Mapeamento de rotas para seções
const routeToSection: Record<string, string> = {
  '/guia': 'guia',
  '/manuais': 'manuais',
  '/sistema': 'sistema',
  '/api': 'api',
  '/dev': 'dev',
  '/status': 'status',
  '/changelog': 'changelog'
};

// Permissões por role (já considera herança)
const rolePermissions: Record<string, string[]> = {
  'user': ['guia'],
  'field-cadastrator': ['guia', 'manuais'],
  'field-coordinator': ['guia', 'manuais'],
  'analyst': ['guia', 'manuais', 'sistema'],
  'admin': ['guia', 'manuais', 'sistema', 'status', 'changelog'],
  'super-admin': ['guia', 'manuais', 'sistema', 'api', 'status', 'changelog'],
  'dev': ['guia', 'manuais', 'sistema', 'api', 'dev', 'status', 'changelog']
};

function getSectionFromPath(pathname: string): string | null {
  const segments = pathname.split('/').filter(Boolean);
  if (segments.length === 0) return null;
  const firstSegment = '/' + segments[0];
  return routeToSection[firstSegment] || null;
}

function userCanAccessSection(roles: string[], section: string): boolean {
  for (const role of roles) {
    const allowedSections = rolePermissions[role] || [];
    if (allowedSections.includes(section)) {
      return true;
    }
  }
  return false;
}

function getAllowedRolesForSection(section: string): string[] {
  return Object.entries(rolePermissions)
    .filter(([_, sections]) => sections.includes(section))
    .map(([role]) => role);
}

const authMiddleware = defineMiddleware(async ({ locals, cookies, url, redirect, rewrite }, next) => {
  // Rotas públicas
  const publicPaths = ['/auth/', '/api/health', '/_astro/', '/favicon'];
  if (publicPaths.some(p => url.pathname.startsWith(p))) {
    return next();
  }

  // Ler access token
  const accessToken = cookies.get('carf_access_token')?.value;

  if (!accessToken) {
    // Não autenticado - redirect para login
    const redirectUrl = encodeURIComponent(url.pathname + url.search);
    return redirect(`/auth/login?redirect=${redirectUrl}`);
  }

  try {
    // Validar JWT
    const { payload } = await jwtVerify(accessToken, getJWKS(), {
      issuer: `${import.meta.env.KEYCLOAK_URL}/realms/${import.meta.env.KEYCLOAK_REALM}`
    });

    // Extrair dados do usuário
    const realmAccess = payload.realm_access as { roles: string[] } | undefined;
    const roles = realmAccess?.roles || [];

    locals.user = {
      id: payload.sub as string,
      email: payload.email as string,
      name: payload.name as string || payload.preferred_username as string,
      roles,
      tenantId: payload.tenant_id as string | null
    };
    locals.isAuthenticated = true;

    // Verificar permissão da seção
    const section = getSectionFromPath(url.pathname);

    if (section && !userCanAccessSection(roles, section)) {
      // Usuário não tem permissão
      locals.allowedRoles = getAllowedRolesForSection(section);
      return rewrite('/403');
    }

    return next();

  } catch (error) {
    // Token inválido ou expirado
    if (error instanceof Error && error.message.includes('expired')) {
      // Tentar refresh
      const refreshToken = cookies.get('carf_refresh_token')?.value;

      if (refreshToken) {
        try {
          const response = await fetch(
            `${import.meta.env.KEYCLOAK_URL}/realms/${import.meta.env.KEYCLOAK_REALM}/protocol/openid-connect/token`,
            {
              method: 'POST',
              headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
              body: new URLSearchParams({
                grant_type: 'refresh_token',
                client_id: import.meta.env.KEYCLOAK_CLIENT_ID,
                refresh_token: refreshToken
              })
            }
          );

          if (response.ok) {
            const tokens = await response.json();

            // Atualizar cookies
            cookies.set('carf_access_token', tokens.access_token, {
              httpOnly: true,
              secure: import.meta.env.PROD,
              sameSite: 'lax',
              path: '/',
              maxAge: tokens.expires_in
            });

            cookies.set('carf_refresh_token', tokens.refresh_token, {
              httpOnly: true,
              secure: import.meta.env.PROD,
              sameSite: 'lax',
              path: '/auth',
              maxAge: tokens.refresh_expires_in
            });

            // Retry com novo token
            return redirect(url.pathname + url.search);
          }
        } catch {
          // Refresh falhou
        }
      }
    }

    // Limpar cookies inválidos e redirect para login
    cookies.delete('carf_access_token', { path: '/' });
    cookies.delete('carf_refresh_token', { path: '/auth' });

    const redirectUrl = encodeURIComponent(url.pathname + url.search);
    return redirect(`/auth/login?redirect=${redirectUrl}`);
  }
});

export const onRequest = sequence(authMiddleware);
```

### Dependência: jose

```json
{
  "dependency": {
    "package": "jose",
    "version": "^5.2.0",
    "purpose": "JWT verification com JWKS",
    "install": "bun add jose"
  }
}
```

### Uso em Páginas

```astro
---
// src/pages/dev/index.astro
const { user, isAuthenticated } = Astro.locals;

if (!isAuthenticated) {
  return Astro.redirect('/auth/login');
}
---

<p>Bem-vindo, {user?.name}</p>
<p>Suas roles: {user?.roles.join(', ')}</p>
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
