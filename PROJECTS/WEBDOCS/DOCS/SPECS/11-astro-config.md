---
type: leaf
status: review
updated: 2026-01-21
---

# Configuração Astro

Especificação completa do arquivo astro.config.mjs que define comportamento do framework Astro com integração Starlight para o portal de documentação WEBDOCS.

A configuração base define site como URL de produção do portal, output como hybrid para combinar páginas estáticas com rotas dinâmicas (autenticação e status), e adapter usando @astrojs/vercel/serverless para deploy na plataforma Vercel com suporte a Server-Side Rendering quando necessário.

## Configuração Base

```json
{
  "site": "https://docs.carf.com.br",
  "output": "hybrid",
  "adapter": "@astrojs/vercel/serverless",
  "trailingSlash": "ignore"
}
```

## Integração Starlight

Starlight fornece estrutura de documentação com navegação, busca e tema. A configuração define title como nome exibido no header, logo com caminho para arquivo SVG em src/assets/, social com links para repositórios GitHub, e locales configurando português brasileiro como idioma padrão.

```json
{
  "starlight": {
    "title": "CARF Docs",
    "logo": {
      "src": "./src/assets/logo.svg",
      "alt": "CARF - Sistema de Regularização Fundiária"
    },
    "social": {
      "github": "https://github.com/carf"
    },
    "locales": {
      "root": {
        "label": "Português",
        "lang": "pt-BR"
      }
    },
    "sidebar": "definido em SPECS/18-sidebar-navigation.md",
    "customCss": ["./src/styles/custom.css"],
    "components": {
      "Header": "./src/components/overrides/Header.astro",
      "SiteTitle": "./src/components/overrides/SiteTitle.astro"
    },
    "head": [
      {
        "tag": "meta",
        "attrs": {
          "name": "robots",
          "content": "noindex"
        },
        "condition": "draft pages only"
      }
    ],
    "pagination": true,
    "tableOfContents": {
      "minHeadingLevel": 2,
      "maxHeadingLevel": 3
    },
    "editLink": {
      "baseUrl": "https://github.com/carf/carf-webdocs/edit/main/"
    }
  }
}
```

## Integrações Adicionais

Além do Starlight, o projeto utiliza integrações para funcionalidades específicas. A integração @astrojs/react permite uso de componentes React da biblioteca @carf/ui com hidratação client-side. A integração @astrojs/mdx habilita uso de componentes em arquivos de conteúdo. A integração @astrojs/sitemap gera sitemap.xml automaticamente para SEO.

```json
{
  "integrations": [
    "@astrojs/starlight",
    "@astrojs/react",
    "@astrojs/mdx",
    "@astrojs/sitemap"
  ]
}
```

## Configuração Vite

Build tool Vite requer configuração específica para SSR com bibliotecas compartilhadas CARF. A opção ssr.noExternal lista pacotes que devem ser bundled ao invés de tratados como external, necessário para bibliotecas que usam imports específicos de Node.js.

```json
{
  "vite": {
    "ssr": {
      "noExternal": [
        "@carf/ui",
        "@carf/tscore",
        "@carf/geoapi-client"
      ]
    },
    "optimizeDeps": {
      "include": ["react", "react-dom"]
    }
  }
}
```

## Configuração de Build

Opções de build controlam output do processo de compilação. O campo outDir define diretório de saída como dist/, compressFiles habilita gzip dos assets, e inlineStylesheets configura threshold para inline de CSS pequeno.

```json
{
  "build": {
    "format": "directory",
    "assets": "_astro",
    "inlineStylesheets": "auto"
  }
}
```

## Markdown e MDX

Configuração de processamento Markdown define plugins remark e rehype para transformações do conteúdo. O plugin remark-gfm habilita GitHub Flavored Markdown com tabelas e checkboxes, rehype-slug adiciona IDs aos headings para deep linking, e rehype-autolink-headings cria links automáticos.

```json
{
  "markdown": {
    "remarkPlugins": ["remark-gfm"],
    "rehypePlugins": [
      "rehype-slug",
      ["rehype-autolink-headings", { "behavior": "wrap" }]
    ],
    "shikiConfig": {
      "theme": "github-dark",
      "wrap": true
    }
  }
}
```

## Variáveis de Ambiente

Astro distingue variáveis públicas (prefixo PUBLIC_) expostas ao cliente de variáveis privadas disponíveis apenas server-side. A configuração não define variáveis diretamente, mas documenta prefixos esperados conforme SPECS/12-env-vars.md.

## Arquivo Completo

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import vercel from '@astrojs/vercel/serverless';

// https://astro.build/config
export default defineConfig({
  // URL do site em produção (usado para canonical links e sitemap)
  site: 'https://docs.carf.com.br',

  // Hybrid: páginas estáticas por padrão, SSR opt-in via export const prerender = false
  output: 'hybrid',

  // Adapter para deploy na Vercel com suporte a Server Functions
  adapter: vercel({
    // Habilitar Web Analytics da Vercel
    webAnalytics: { enabled: true },
    // Máximo de duração das funções serverless (segundos)
    maxDuration: 10,
  }),

  // Ignorar trailing slash - /guia e /guia/ são equivalentes
  trailingSlash: 'ignore',

  // Integrações
  integrations: [
    // Starlight - framework de documentação
    starlight({
      title: 'CARF Docs',

      // Logo no header
      logo: {
        src: './src/assets/logo.svg',
        alt: 'CARF - Sistema de Regularização Fundiária',
        replacesTitle: false, // Exibe logo + título
      },

      // Links sociais no header
      social: {
        github: 'https://github.com/carf',
      },

      // Configuração de idioma
      defaultLocale: 'root',
      locales: {
        root: {
          label: 'Português',
          lang: 'pt-BR',
        },
      },

      // Sidebar - definida inline ou em arquivo separado
      sidebar: [
        {
          label: 'Guia',
          autogenerate: { directory: 'guia' },
        },
        {
          label: 'Manuais',
          autogenerate: { directory: 'manuais' },
          collapsed: true,
        },
        {
          label: 'API',
          autogenerate: { directory: 'api' },
          collapsed: true,
        },
        {
          label: 'Status',
          link: '/status/',
        },
      ],

      // CSS customizado
      customCss: [
        './src/styles/custom.css',
        './src/styles/error-pages.css',
      ],

      // Override de componentes Starlight
      components: {
        // Header customizado com UserMenu
        Header: './src/components/overrides/Header.astro',
        // SiteTitle com versão
        SiteTitle: './src/components/overrides/SiteTitle.astro',
      },

      // Tags <head> adicionais
      head: [
        // Favicon
        {
          tag: 'link',
          attrs: {
            rel: 'icon',
            href: '/favicon.svg',
            type: 'image/svg+xml',
          },
        },
        // Preconnect para Keycloak (auth)
        {
          tag: 'link',
          attrs: {
            rel: 'preconnect',
            href: 'https://auth.carf.com.br',
          },
        },
      ],

      // Habilitar paginação prev/next
      pagination: true,

      // Table of Contents config
      tableOfContents: {
        minHeadingLevel: 2,
        maxHeadingLevel: 3,
      },

      // Link para editar no GitHub
      editLink: {
        baseUrl: 'https://github.com/carf/carf-webdocs/edit/main/',
      },

      // Desabilitar créditos do Starlight no footer
      credits: false,

      // Favicon
      favicon: '/favicon.svg',
    }),

    // React para componentes interativos
    react(),

    // MDX para conteúdo com componentes
    mdx(),

    // Sitemap automático para SEO
    sitemap({
      filter: (page) => {
        // Excluir páginas /dev/ do sitemap (protegidas)
        return !page.includes('/dev/');
      },
    }),
  ],

  // Configuração do Vite (bundler)
  vite: {
    // SSR: pacotes que devem ser bundled (não external)
    ssr: {
      noExternal: [
        '@carf/ui',
        '@carf/tscore',
        '@carf/geoapi-client',
      ],
    },

    // Otimização de dependências
    optimizeDeps: {
      include: ['react', 'react-dom'],
    },

    // Resolver aliases
    resolve: {
      alias: {
        '@': '/src',
        '@components': '/src/components',
        '@lib': '/src/lib',
        '@config': '/src/config',
      },
    },
  },

  // Configuração de build
  build: {
    // Formato de URLs (directory = /page/index.html)
    format: 'directory',

    // Diretório de assets com hash
    assets: '_astro',

    // Inline CSS pequeno automaticamente
    inlineStylesheets: 'auto',
  },

  // Configuração de Markdown
  markdown: {
    // Plugins Remark (processamento Markdown)
    remarkPlugins: [],

    // Plugins Rehype (processamento HTML)
    rehypePlugins: [],

    // Syntax highlighting com Shiki
    shikiConfig: {
      theme: 'github-dark',
      wrap: true,
    },
  },

  // Configuração de redirecionamentos
  redirects: {
    // Redirect legacy URLs
    '/docs/[...slug]': '/guia/[...slug]',
  },
});
```

## Registrar Middleware

O middleware deve ser registrado em `src/middleware.ts` (Astro detecta automaticamente):

```typescript
// src/middleware.ts
import { defineMiddleware, sequence } from 'astro:middleware';

// Import dos middlewares
import { authMiddleware } from './lib/auth/middleware';

// Combinar middlewares em sequência
export const onRequest = sequence(authMiddleware);
```

## Types de Ambiente

```typescript
// src/env.d.ts
/// <reference types="astro/client" />

interface ImportMetaEnv {
  readonly PUBLIC_SITE_URL: string;
  readonly KEYCLOAK_URL: string;
  readonly KEYCLOAK_REALM: string;
  readonly KEYCLOAK_CLIENT_ID: string;
  // Nota: Client é público com PKCE, não usa client_secret
  readonly GEOAPI_URL: string;
  readonly GEOAPI_SWAGGER_PATH: string;
  readonly GEOAPI_HEALTH_URL?: string;
  readonly KEYCLOAK_HEALTH_URL?: string;
  readonly MINIO_HEALTH_URL?: string;
  readonly STATUS_POLL_INTERVAL_MS?: string;
  readonly CACHE_TTL_SECONDS?: string;
  readonly LOG_LEVEL?: string;
  readonly GITHUB_CLIENT_ID?: string;
  readonly GITHUB_CLIENT_SECRET?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}

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
    allowedRoles?: string[];
  }
}
```

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
