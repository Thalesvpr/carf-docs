---
status: review
updated: 2026-01-21
---

# Swagger Embutido

Seção /dev/swagger/ renderiza Swagger UI interativo permitindo desenvolvedores explorar e testar endpoints da GEOAPI diretamente no portal de documentação com autenticação real usando token JWT do usuário logado.

Componente SwaggerPage.astro verifica role dev antes de renderizar conteúdo. Usuários sem role recebem página 403 com explicação. Verificação acontece em middleware SSR antes de qualquer fetch de dados sensíveis como especificação OpenAPI.

Fetch da especificação executa durante SSR obtendo /swagger/v1/swagger.json da GEOAPI. Especificação é injetada como JSON inline no HTML evitando CORS issues e reduzindo latência de carregamento. Cache em memória de 5 minutos reduz carga no backend.

Inicialização do swagger-ui-dist acontece client-side após hidratação. Script configura spec com JSON inline, requestInterceptor adicionando Authorization header com token extraído de cookie, persistAuthorization false para não armazenar tokens no localStorage, e deepLinking true para URLs compartilháveis.

Customização visual via CSS sobrescreve cores do Swagger UI para manter consistência com tema CARF. Variáveis CSS mapeiam cores primárias, backgrounds, e tipografia. Header e topbar do Swagger são escondidos para não conflitar com navegação do WEBDOCS.

Try-it-out permite executar requisições reais contra GEOAPI usando token do desenvolvedor logado. Útil para testar endpoints durante desenvolvimento sem configurar ferramentas externas. Responses são exibidos com syntax highlighting e opção de copiar.

## Componente SwaggerPage.astro

```astro
---
// src/pages/dev/api/swagger.astro
import Layout from '../../../layouts/DevLayout.astro';
import { getSwaggerSpec } from '../../../lib/swagger/cache';

// Verificação de role acontece no middleware
// Este arquivo só é alcançado se usuário tem role dev

const spec = await getSwaggerSpec();
const specJson = JSON.stringify(spec);
---

<Layout title="API Reference - Swagger">
  <div id="swagger-ui"></div>

  <script define:vars={{ specJson }}>
    // Carrega swagger-ui após DOM ready
    document.addEventListener('DOMContentLoaded', () => {
      const spec = JSON.parse(specJson);

      // Extrai token do cookie
      const getToken = () => {
        const match = document.cookie.match(/carf_access_token=([^;]+)/);
        return match ? match[1] : null;
      };

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
        requestInterceptor: (req) => {
          const token = getToken();
          if (token) {
            req.headers['Authorization'] = `Bearer ${token}`;
          }
          return req;
        }
      });
    });
  </script>
</Layout>

<style is:global>
  /* Oculta header/topbar do Swagger */
  .swagger-ui .topbar { display: none; }

  /* Cores CARF */
  .swagger-ui .info .title { color: var(--sl-color-text-accent); }
  .swagger-ui .opblock.opblock-get { border-color: #61affe; background: rgba(97, 175, 254, 0.1); }
  .swagger-ui .opblock.opblock-post { border-color: #49cc90; background: rgba(73, 204, 144, 0.1); }
  .swagger-ui .opblock.opblock-put { border-color: #fca130; background: rgba(252, 161, 48, 0.1); }
  .swagger-ui .opblock.opblock-delete { border-color: #f93e3e; background: rgba(249, 62, 62, 0.1); }

  /* Tema escuro */
  [data-theme='dark'] .swagger-ui {
    background: var(--sl-color-bg);
  }
  [data-theme='dark'] .swagger-ui .opblock .opblock-summary-description,
  [data-theme='dark'] .swagger-ui .opblock .opblock-summary-path,
  [data-theme='dark'] .swagger-ui .opblock .opblock-summary-path__deprecated,
  [data-theme='dark'] .swagger-ui table thead tr th,
  [data-theme='dark'] .swagger-ui .parameter__name,
  [data-theme='dark'] .swagger-ui .parameter__type,
  [data-theme='dark'] .swagger-ui .response-col_status,
  [data-theme='dark'] .swagger-ui .response-col_description {
    color: var(--sl-color-text);
  }
</style>
```

## Serviço de Cache da Especificação

```typescript
// src/lib/swagger/cache.ts
interface CacheEntry {
  spec: object;
  timestamp: number;
}

let cache: CacheEntry | null = null;
const CACHE_TTL = 5 * 60 * 1000; // 5 minutos

export async function getSwaggerSpec(forceRefresh = false): Promise<object> {
  const now = Date.now();

  // Retorna cache se válido
  if (!forceRefresh && cache && (now - cache.timestamp) < CACHE_TTL) {
    return cache.spec;
  }

  // Fetch nova especificação
  const swaggerUrl = import.meta.env.GEOAPI_SWAGGER_URL;
  const response = await fetch(swaggerUrl, {
    headers: { 'Accept': 'application/json' },
    signal: AbortSignal.timeout(10000)
  });

  if (!response.ok) {
    throw new Error(`Failed to fetch swagger spec: ${response.status}`);
  }

  const spec = await response.json();

  // Atualiza cache
  cache = { spec, timestamp: now };

  return spec;
}

export function invalidateCache(): void {
  cache = null;
}
```

## Layout DevLayout.astro

```astro
---
// src/layouts/DevLayout.astro
import BaseLayout from './BaseLayout.astro';

interface Props {
  title: string;
}

const { title } = Astro.props;

// Verificar se usuário tem role dev (middleware já fez, mas double-check)
if (!Astro.locals.user?.roles?.includes('dev')) {
  return Astro.redirect('/403');
}
---

<BaseLayout title={title}>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-standalone-preset.js"></script>

  <slot />
</BaseLayout>
```

## Variáveis de Ambiente

```bash
# URL da especificação OpenAPI
GEOAPI_SWAGGER_URL=https://api.carf.com.br/swagger/v1/swagger.json
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
