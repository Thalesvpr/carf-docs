---
id: ""
type: ARCH
modules: []
epic: ""
status: review
created: 2026-01-21
updated: 2026-01-21
---

# Fluxo de Dados

Especificação dos fluxos de dados na aplicação WEBDOCS, cobrindo build time (SSG), request time (SSR), autenticação e status page.

## Build Time (SSG)

A maioria das páginas é gerada estaticamente no build. Content Collections são processadas e validadas.

```json
{
  "ssg_flow": {
    "1_content_collection": {
      "input": "src/content/docs/**/*.mdx",
      "process": "Astro lê arquivos, valida frontmatter com schema Zod",
      "output": "Collection entries com data tipada",
      "errors": "Build falha se frontmatter inválido"
    },
    "2_page_generation": {
      "input": "Collection entries + [...slug].astro",
      "process": "Astro renderiza cada entry como página HTML",
      "output": "HTML estático em dist/",
      "optimization": "CSS e JS inline ou bundled"
    },
    "3_search_index": {
      "input": "HTML gerado",
      "process": "Pagefind indexa conteúdo textual",
      "output": "Índice de busca em dist/pagefind/",
      "size": "~10-50kb dependendo do conteúdo"
    },
    "4_sitemap": {
      "input": "Todas páginas geradas",
      "process": "Integration @astrojs/sitemap gera sitemap.xml",
      "output": "dist/sitemap.xml"
    }
  }
}
```

## Request Time (SSR)

Rotas com output: 'server' ou 'hybrid' são renderizadas no request.

```json
{
  "ssr_flow": {
    "1_middleware": {
      "trigger": "Toda request HTTP",
      "process": [
        "Ler cookies de autenticação",
        "Decodificar JWT do access_token",
        "Extrair roles do claim realm_access.roles",
        "Popular Astro.locals.user"
      ],
      "output": "Request enriquecido com dados do usuário"
    },
    "2_route_matching": {
      "trigger": "Após middleware",
      "process": "Astro determina rota baseado no path",
      "types": {
        "static": "Serve HTML pre-renderizado de dist/",
        "dynamic": "Executa código server-side da página"
      }
    },
    "3_page_render": {
      "trigger": "Rotas dinâmicas (auth, status)",
      "process": "Astro executa frontmatter TypeScript, renderiza template",
      "data_sources": [
        "Astro.locals (dados do middleware)",
        "Fetch para APIs externas",
        "Variáveis de ambiente"
      ],
      "output": "HTML dinâmico"
    },
    "4_api_routes": {
      "trigger": "Request para /api/*",
      "process": "Endpoint TypeScript processa request",
      "input": "Request body, query params, cookies",
      "output": "JSON response"
    }
  }
}
```

## Fluxo de Autenticação

Fluxo OAuth2 Authorization Code com PKCE.

```json
{
  "auth_flow": {
    "1_login_click": {
      "trigger": "Usuário clica no botão de login",
      "action": "Redirect para /auth/login",
      "data": "URL atual salva para retorno"
    },
    "2_pkce_generation": {
      "trigger": "/auth/login processa request",
      "action": "Gera code_verifier e code_challenge",
      "storage": "code_verifier salvo em cookie auth_state",
      "redirect": "Para Keycloak authorize endpoint"
    },
    "3_keycloak_auth": {
      "trigger": "Usuário no Keycloak",
      "action": "Login com credenciais",
      "redirect": "Para /auth/callback com code e state"
    },
    "4_token_exchange": {
      "trigger": "/auth/callback recebe code",
      "action": [
        "Validar state contra cookie",
        "POST para Keycloak token endpoint",
        "Receber access_token e refresh_token"
      ],
      "storage": "Tokens salvos em cookies HttpOnly"
    },
    "5_redirect_back": {
      "trigger": "Tokens salvos",
      "action": "Redirect para URL original",
      "cleanup": "Cookie auth_state deletado"
    },
    "6_subsequent_requests": {
      "trigger": "Usuário navega pelo site",
      "action": [
        "Middleware lê cookie access_token",
        "Decodifica JWT",
        "Popula Astro.locals.user"
      ],
      "available": "user.name, user.email, user.roles"
    },
    "7_token_refresh": {
      "trigger": "access_token expira (verificado no middleware)",
      "action": [
        "POST para /api/refresh",
        "Usa refresh_token para obter novo access_token",
        "Atualiza cookie"
      ],
      "fallback": "Se refresh falhar, redirect para login"
    }
  }
}
```

## Fluxo da Status Page

Combinação de SSR inicial com polling client-side.

```json
{
  "status_flow": {
    "1_ssr_fetch": {
      "trigger": "Request para /status/",
      "action": [
        "Ler configuração de serviços",
        "Promise.allSettled para health checks paralelos",
        "Timeout de 5s por serviço"
      ],
      "output": "Status inicial renderizado no HTML"
    },
    "2_html_response": {
      "content": [
        "Grid com cards de serviços",
        "Status atual de cada serviço",
        "Timestamp da verificação",
        "Checkbox para auto-refresh"
      ]
    },
    "3_client_hydration": {
      "trigger": "Página carrega no browser",
      "action": "StatusGrid hidrata com client:idle",
      "state": "useState com status inicial do SSR"
    },
    "4_polling_loop": {
      "trigger": "Auto-refresh habilitado",
      "action": [
        "setInterval a cada 30s",
        "Fetch para /api/status",
        "Atualizar state com novos dados"
      ],
      "ui_update": "Cards atualizam sem reload"
    },
    "5_api_status": {
      "trigger": "GET /api/status",
      "action": "Mesma lógica de health check do SSR",
      "response": "JSON com status de todos serviços",
      "cache": "No-cache para dados sempre frescos"
    }
  }
}
```

## Dados no Middleware

Dados disponíveis em Astro.locals após middleware.

```json
{
  "astro_locals": {
    "user": {
      "type": "User | null",
      "fields": {
        "id": "string (sub claim)",
        "name": "string (name claim)",
        "email": "string (email claim)",
        "roles": "string[] (realm_access.roles claim)"
      },
      "null_when": "Usuário não autenticado"
    },
    "isAuthenticated": {
      "type": "boolean",
      "value": "user !== null"
    }
  }
}
```

## Cache Strategy

```json
{
  "caching": {
    "static_pages": {
      "strategy": "Cache-Control: public, max-age=31536000, immutable",
      "invalidation": "Hash no filename"
    },
    "dynamic_pages": {
      "strategy": "Cache-Control: private, no-cache",
      "reason": "Conteúdo depende do usuário"
    },
    "api_status": {
      "strategy": "Cache-Control: no-store",
      "reason": "Dados sempre frescos"
    },
    "swagger_spec": {
      "strategy": "Cache interno de 5 minutos",
      "invalidation": "TTL expirado"
    }
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
