---
status: review
updated: 2026-01-21
---

# Integração com GEOAPI Swagger

Seção /dev/swagger/ do WEBDOCS renderiza documentação interativa da API GEOAPI consumindo especificação OpenAPI diretamente do backend. Integração permite testar endpoints usando token JWT real do desenvolvedor logado.

Especificação OpenAPI é gerada automaticamente pela GEOAPI via Swashbuckle a partir dos controllers .NET com XML comments. Endpoint /swagger/v1/swagger.json retorna JSON atualizado refletindo estado atual da API sem necessidade de manutenção manual de documentação.

Componente SwaggerEmbed.astro executa fetch da especificação durante SSR, inicializa swagger-ui-dist com spec inline, e configura requestInterceptor para adicionar header Authorization: Bearer com token do usuário extraído do cookie de sessão. Try-it-out funciona com autenticação real.

Customização visual aplica tema CARF ao Swagger UI via CSS sobrescrevendo cores padrão para manter consistência com restante do portal. Header e footer do Swagger são escondidos via CSS para não conflitar com layout do WEBDOCS.

Autorização verifica role dev antes de renderizar componente. Usuários sem role recebem mensagem explicando necessidade de acesso de desenvolvedor. Isso previne exposição acidental de endpoints internos ou sensíveis para usuários não autorizados.

Cache da especificação armazenada em memória por 5 minutos reduz carga no backend para usuários que navegam entre páginas. Invalidação manual via query param ?refresh=true força novo fetch para desenvolvedores testando mudanças recentes.

## Componente SwaggerEmbed.astro

```astro
---
// src/components/SwaggerEmbed.astro
import { getSwaggerSpec, invalidateCache } from '../lib/swagger/cache';

interface Props {
  class?: string;
}

const { class: className } = Astro.props;

// Verifica se deve invalidar cache
const refresh = Astro.url.searchParams.get('refresh') === 'true';
if (refresh) {
  invalidateCache();
}

// Fetch da especificação
let spec: object;
let error: string | null = null;

try {
  spec = await getSwaggerSpec();
} catch (e) {
  error = e instanceof Error ? e.message : 'Failed to load API specification';
  spec = {};
}

const specJson = JSON.stringify(spec);
---

{error ? (
  <div class="bg-red-50 dark:bg-red-900/30 border border-red-200 rounded-lg p-4">
    <p class="text-red-800 dark:text-red-200 font-semibold">Erro ao carregar especificação</p>
    <p class="text-sm text-red-600 dark:text-red-300">{error}</p>
    <a href="?refresh=true" class="text-sm text-blue-600 hover:underline mt-2 inline-block">
      Tentar novamente
    </a>
  </div>
) : (
  <div id="swagger-ui" class={className}></div>
)}

<script define:vars={{ specJson, hasError: !!error }}>
  if (!hasError) {
    const initSwagger = () => {
      const spec = JSON.parse(specJson);

      // Função para extrair token do cookie
      const getAuthToken = () => {
        const cookies = document.cookie.split(';');
        for (const cookie of cookies) {
          const [name, value] = cookie.trim().split('=');
          if (name === 'carf_access_token') {
            return decodeURIComponent(value);
          }
        }
        return null;
      };

      // Inicializa Swagger UI
      window.ui = SwaggerUIBundle({
        spec: spec,
        dom_id: '#swagger-ui',
        deepLinking: true,
        presets: [
          SwaggerUIBundle.presets.apis,
          SwaggerUIStandalonePreset
        ],
        plugins: [
          SwaggerUIBundle.plugins.DownloadUrl
        ],
        layout: 'StandaloneLayout',
        persistAuthorization: false,
        displayRequestDuration: true,
        filter: true,
        showExtensions: true,
        showCommonExtensions: true,
        tryItOutEnabled: true,
        requestInterceptor: (request) => {
          const token = getAuthToken();
          if (token) {
            request.headers['Authorization'] = `Bearer ${token}`;
          }
          return request;
        },
        responseInterceptor: (response) => {
          // Log de responses para debug
          if (response.status >= 400) {
            console.warn('[Swagger] Request failed:', response.status, response.url);
          }
          return response;
        }
      });
    };

    // Aguarda DOM e scripts carregarem
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', initSwagger);
    } else {
      // Aguarda scripts do Swagger carregarem
      const checkSwagger = setInterval(() => {
        if (typeof SwaggerUIBundle !== 'undefined') {
          clearInterval(checkSwagger);
          initSwagger();
        }
      }, 100);
    }
  }
</script>

<style is:global>
  /* Reset de estilos do Swagger UI */
  #swagger-ui {
    font-family: var(--sl-font);
  }

  /* Oculta topbar */
  .swagger-ui .topbar {
    display: none;
  }

  /* Cores por método HTTP */
  .swagger-ui .opblock.opblock-get {
    background: rgba(97, 175, 254, 0.1);
    border-color: #61affe;
  }
  .swagger-ui .opblock.opblock-get .opblock-summary-method {
    background: #61affe;
  }

  .swagger-ui .opblock.opblock-post {
    background: rgba(73, 204, 144, 0.1);
    border-color: #49cc90;
  }
  .swagger-ui .opblock.opblock-post .opblock-summary-method {
    background: #49cc90;
  }

  .swagger-ui .opblock.opblock-put {
    background: rgba(252, 161, 48, 0.1);
    border-color: #fca130;
  }
  .swagger-ui .opblock.opblock-put .opblock-summary-method {
    background: #fca130;
  }

  .swagger-ui .opblock.opblock-delete {
    background: rgba(249, 62, 62, 0.1);
    border-color: #f93e3e;
  }
  .swagger-ui .opblock.opblock-delete .opblock-summary-method {
    background: #f93e3e;
  }

  /* Tema escuro */
  [data-theme='dark'] .swagger-ui {
    background: transparent;
  }

  [data-theme='dark'] .swagger-ui,
  [data-theme='dark'] .swagger-ui .opblock-tag,
  [data-theme='dark'] .swagger-ui .opblock .opblock-summary-description,
  [data-theme='dark'] .swagger-ui .opblock .opblock-summary-path,
  [data-theme='dark'] .swagger-ui .opblock-description-wrapper p,
  [data-theme='dark'] .swagger-ui table thead tr th,
  [data-theme='dark'] .swagger-ui table tbody tr td,
  [data-theme='dark'] .swagger-ui .parameter__name,
  [data-theme='dark'] .swagger-ui .parameter__type,
  [data-theme='dark'] .swagger-ui .parameter__deprecated,
  [data-theme='dark'] .swagger-ui .parameter__in,
  [data-theme='dark'] .swagger-ui .response-col_status,
  [data-theme='dark'] .swagger-ui .response-col_description,
  [data-theme='dark'] .swagger-ui .response-col_links,
  [data-theme='dark'] .swagger-ui .tab li,
  [data-theme='dark'] .swagger-ui .model-title,
  [data-theme='dark'] .swagger-ui .model {
    color: var(--sl-color-text);
  }

  [data-theme='dark'] .swagger-ui .opblock .opblock-section-header {
    background: rgba(255, 255, 255, 0.05);
  }

  [data-theme='dark'] .swagger-ui input[type=text],
  [data-theme='dark'] .swagger-ui textarea {
    background: var(--sl-color-bg);
    color: var(--sl-color-text);
    border-color: var(--sl-color-gray-5);
  }

  [data-theme='dark'] .swagger-ui select {
    background: var(--sl-color-bg);
    color: var(--sl-color-text);
  }

  [data-theme='dark'] .swagger-ui .btn {
    color: var(--sl-color-text);
    border-color: var(--sl-color-gray-5);
  }

  [data-theme='dark'] .swagger-ui .model-box {
    background: rgba(255, 255, 255, 0.02);
  }
</style>
```

## Serviço de Cache

```typescript
// src/lib/swagger/cache.ts
interface CacheEntry {
  spec: object;
  timestamp: number;
}

const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutos

let cache: CacheEntry | null = null;

export async function getSwaggerSpec(forceRefresh = false): Promise<object> {
  const now = Date.now();

  // Retorna do cache se válido e não forçou refresh
  if (!forceRefresh && cache && (now - cache.timestamp) < CACHE_TTL_MS) {
    console.log('[swagger-cache] Returning cached spec');
    return cache.spec;
  }

  console.log('[swagger-cache] Fetching fresh spec');

  const swaggerUrl = import.meta.env.GEOAPI_SWAGGER_URL;
  if (!swaggerUrl) {
    throw new Error('GEOAPI_SWAGGER_URL not configured');
  }

  const response = await fetch(swaggerUrl, {
    headers: {
      'Accept': 'application/json',
      'Cache-Control': 'no-cache'
    },
    signal: AbortSignal.timeout(15000) // 15s timeout
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch OpenAPI spec: HTTP ${response.status}`);
  }

  const spec = await response.json();

  // Valida estrutura básica
  if (!spec.openapi && !spec.swagger) {
    throw new Error('Invalid OpenAPI specification');
  }

  // Atualiza cache
  cache = { spec, timestamp: now };

  return spec;
}

export function invalidateCache(): void {
  cache = null;
  console.log('[swagger-cache] Cache invalidated');
}

export function getCacheAge(): number | null {
  if (!cache) return null;
  return Date.now() - cache.timestamp;
}
```

## Página do Swagger

```astro
---
// src/pages/dev/api/swagger.astro
export const prerender = false; // SSR para verificar auth

import DevLayout from '../../../layouts/DevLayout.astro';
import SwaggerEmbed from '../../../components/SwaggerEmbed.astro';

// Middleware já verificou role 'dev'
const user = Astro.locals.user;
---

<DevLayout title="API Reference">
  <div class="max-w-7xl mx-auto px-4 py-6">
    <div class="mb-6">
      <h1 class="text-2xl font-bold">API Reference</h1>
      <p class="text-gray-600 dark:text-gray-400">
        Documentação interativa da GEOAPI. Autenticado como {user?.email}.
      </p>
      <a href="?refresh=true" class="text-sm text-blue-600 hover:underline">
        Recarregar especificação
      </a>
    </div>

    <SwaggerEmbed />
  </div>
</DevLayout>
```

## Variáveis de Ambiente

```bash
# URL do endpoint swagger.json da GEOAPI
GEOAPI_SWAGGER_URL=https://api.carf.com.br/swagger/v1/swagger.json
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
