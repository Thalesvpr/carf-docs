---
type: leaf
status: review
updated: 2026-01-21
---

# Caching Strategy

Estratégias de cache para otimização de performance do WEBDOCS. Define TTLs, invalidação e headers para cada tipo de recurso.

## Visão Geral

```json
{
  "cache_layers": {
    "browser": "Cache-Control headers para assets estáticos",
    "cdn": "Vercel Edge Cache para páginas e assets",
    "application": "In-memory cache para dados dinâmicos",
    "service_worker": "Opcional para offline support"
  },
  "strategy": "Stale-while-revalidate para dados dinâmicos, immutable para assets com hash"
}
```

## Cache por Tipo de Recurso

### Assets Estáticos (Imutáveis)

```json
{
  "static_assets": {
    "pattern": "/_astro/*",
    "files": ["*.js", "*.css", "*.woff2", "*.png", "*.jpg", "*.svg"],
    "headers": {
      "Cache-Control": "public, max-age=31536000, immutable"
    },
    "ttl": "1 ano",
    "reason": "Astro adiciona hash no nome do arquivo, conteúdo nunca muda"
  }
}
```

### Páginas HTML

```json
{
  "html_pages": {
    "static_pages": {
      "pattern": "/guia/*, /manuais/*",
      "headers": {
        "Cache-Control": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=86400"
      },
      "ttl_browser": "1 hora",
      "ttl_cdn": "24 horas",
      "reason": "Conteúdo muda raramente, CDN serve stale enquanto revalida"
    },
    "dynamic_pages": {
      "pattern": "/status/, /api/swagger/",
      "headers": {
        "Cache-Control": "public, max-age=0, s-maxage=60, stale-while-revalidate=300"
      },
      "ttl_browser": "0 (sempre revalida)",
      "ttl_cdn": "1 minuto",
      "reason": "Dados em tempo real, mas CDN ajuda em picos de tráfego"
    },
    "protected_pages": {
      "pattern": "/dev/*",
      "headers": {
        "Cache-Control": "private, no-cache, no-store, must-revalidate"
      },
      "reason": "Conteúdo sensível, nunca cachear"
    }
  }
}
```

### API Endpoints

```json
{
  "api_endpoints": {
    "/api/health": {
      "method": "GET",
      "cache": "no-cache",
      "reason": "Status em tempo real"
    },
    "/api/swagger": {
      "method": "GET",
      "cache": "application_memory",
      "ttl": 300,
      "reason": "Spec OpenAPI muda raramente"
    },
    "/api/status": {
      "method": "GET",
      "cache": "no-cache",
      "reason": "Health checks devem ser sempre frescos"
    }
  }
}
```

## Cache In-Memory (Application Level)

### Swagger Spec Cache

```json
{
  "swagger_cache": {
    "implementation": "Map em memória",
    "key": "swagger_spec_${version}",
    "ttl": 300,
    "invalidation": "Manual via ?refresh=true ou restart do servidor",
    "size_limit": "1 spec por ambiente"
  }
}
```

```typescript
// src/lib/cache/swagger-cache.ts
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
}

class SwaggerCache {
  private cache: Map<string, CacheEntry<unknown>> = new Map();
  private defaultTTL = 5 * 60 * 1000; // 5 minutos

  async get<T>(key: string, fetcher: () => Promise<T>, ttl?: number): Promise<T> {
    const entry = this.cache.get(key) as CacheEntry<T> | undefined;
    const now = Date.now();

    // Cache hit e não expirado
    if (entry && now - entry.timestamp < entry.ttl) {
      return entry.data;
    }

    // Cache miss ou expirado - buscar novo dado
    const data = await fetcher();

    this.cache.set(key, {
      data,
      timestamp: now,
      ttl: ttl ?? this.defaultTTL
    });

    return data;
  }

  invalidate(key: string): void {
    this.cache.delete(key);
  }

  invalidateAll(): void {
    this.cache.clear();
  }
}

export const swaggerCache = new SwaggerCache();
```

Uso:

```typescript
// src/pages/api/swagger.ts
import { swaggerCache } from '../../lib/cache/swagger-cache';

export async function GET({ url }) {
  const forceRefresh = url.searchParams.get('refresh') === 'true';

  if (forceRefresh) {
    swaggerCache.invalidate('geoapi_swagger');
  }

  const spec = await swaggerCache.get(
    'geoapi_swagger',
    async () => {
      const response = await fetch(`${import.meta.env.GEOAPI_URL}/swagger/v1/swagger.json`);
      return response.json();
    },
    5 * 60 * 1000 // 5 minutos
  );

  return new Response(JSON.stringify(spec), {
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'public, max-age=60'
    }
  });
}
```

### JWKS Cache

```json
{
  "jwks_cache": {
    "implementation": "jose library built-in ou Map customizado",
    "key": "keycloak_jwks",
    "ttl": 86400,
    "invalidation_triggers": [
      "JWT validation fails with 'unknown key'",
      "24 horas desde última atualização"
    ],
    "reason": "Chaves públicas mudam raramente, mas devem ser atualizadas em rotação"
  }
}
```

```typescript
// src/lib/auth/jwks-cache.ts
import { createRemoteJWKSet } from 'jose';

interface JWKSCacheEntry {
  jwks: ReturnType<typeof createRemoteJWKSet>;
  timestamp: number;
}

class JWKSCache {
  private cache: JWKSCacheEntry | null = null;
  private ttl = 24 * 60 * 60 * 1000; // 24 horas

  getJWKS(): ReturnType<typeof createRemoteJWKSet> {
    const now = Date.now();

    // Cache válido
    if (this.cache && now - this.cache.timestamp < this.ttl) {
      return this.cache.jwks;
    }

    // Criar novo JWKS (jose faz cache interno também)
    const jwksUrl = new URL(
      `${import.meta.env.KEYCLOAK_URL}/realms/${import.meta.env.KEYCLOAK_REALM}/protocol/openid-connect/certs`
    );

    const jwks = createRemoteJWKSet(jwksUrl);

    this.cache = {
      jwks,
      timestamp: now
    };

    return jwks;
  }

  invalidate(): void {
    this.cache = null;
  }
}

export const jwksCache = new JWKSCache();
```

## Vercel Edge Cache (CDN)

### vercel.json Configuration

```json
{
  "headers": [
    {
      "source": "/_astro/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=31536000, immutable"
        }
      ]
    },
    {
      "source": "/guia/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=86400"
        }
      ]
    },
    {
      "source": "/manuais/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=86400"
        }
      ]
    },
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, s-maxage=60, stale-while-revalidate=300"
        }
      ]
    },
    {
      "source": "/status",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "public, max-age=0, s-maxage=30, stale-while-revalidate=60"
        }
      ]
    },
    {
      "source": "/dev/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "private, no-cache, no-store, must-revalidate"
        }
      ]
    }
  ]
}
```

## Cache Headers Explicados

```json
{
  "headers_reference": {
    "public": "Pode ser cacheado por CDN e browser",
    "private": "Apenas browser pode cachear (conteúdo personalizado)",
    "max-age": "Tempo em segundos que browser considera cache válido",
    "s-maxage": "Tempo que CDN (shared cache) considera válido",
    "stale-while-revalidate": "CDN serve stale enquanto busca novo em background",
    "immutable": "Indica que conteúdo nunca muda (assets com hash)",
    "no-cache": "Sempre revalidar antes de usar cache",
    "no-store": "Nunca armazenar em cache",
    "must-revalidate": "Após expiração, deve revalidar antes de usar"
  }
}
```

## Invalidação de Cache

### Manual via Query Parameter

```json
{
  "manual_invalidation": {
    "swagger": {
      "url": "/api/swagger?refresh=true",
      "effect": "Invalida cache in-memory e busca nova spec"
    },
    "jwks": {
      "trigger": "JWT validation failure",
      "effect": "jwksCache.invalidate() e retry"
    }
  }
}
```

### Invalidação Automática (Deploy)

```json
{
  "deploy_invalidation": {
    "vercel": {
      "behavior": "Novo deploy = novo edge cache",
      "immutable_assets": "Hash muda = nova URL = novo cache"
    },
    "in_memory": {
      "behavior": "Restart do servidor = cache limpo",
      "cold_start": "Primeira request após deploy = cache miss"
    }
  }
}
```

## Status Page (Sem Cache)

```json
{
  "status_page": {
    "caching": "Nenhum - sempre server-rendered",
    "reason": "Health checks devem refletir estado atual",
    "headers": {
      "Cache-Control": "no-cache, no-store, must-revalidate",
      "Pragma": "no-cache",
      "Expires": "0"
    },
    "implementation": "SSR em cada request"
  }
}
```

```typescript
// src/pages/status.astro
---
// Forçar no-cache no response
Astro.response.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
Astro.response.headers.set('Pragma', 'no-cache');
Astro.response.headers.set('Expires', '0');

// Health checks executados em cada request
const healthResults = await checkAllServices();
---
```

## Métricas de Cache

```json
{
  "monitoring": {
    "vercel_analytics": {
      "cache_hit_rate": "% de requests servidas do edge",
      "origin_requests": "Requests que chegam ao servidor"
    },
    "application_metrics": {
      "swagger_cache_hits": "Contador de cache hits",
      "swagger_cache_misses": "Contador de cache misses",
      "jwks_refreshes": "Contador de refreshes de JWKS"
    }
  }
}
```

## Troubleshooting

```json
{
  "common_issues": {
    "stale_content_after_deploy": {
      "cause": "Browser cache com max-age alto",
      "solution": "Hard refresh (Ctrl+Shift+R) ou limpar cache"
    },
    "swagger_outdated": {
      "cause": "Cache in-memory não invalidado",
      "solution": "Acessar /api/swagger?refresh=true"
    },
    "jwt_validation_fails_new_key": {
      "cause": "JWKS cache com chave antiga",
      "solution": "Invalidar JWKS cache via código ou restart"
    },
    "protected_content_cached": {
      "cause": "CDN cacheando página /dev/",
      "solution": "Verificar headers Cache-Control: private"
    }
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
