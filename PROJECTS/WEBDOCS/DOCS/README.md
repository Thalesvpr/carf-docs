# WEBDOCS - Portal de Documentação

Documentação do portal VitePress.

## Visão Geral

WEBDOCS é portal de documentação estática gerado por VitePress (Vue 3) servindo toda documentação CARF de forma navegável e searchable.

### Características

- **VitePress** - Static site generator baseado em Vue 3
- **Markdown** - Documentação em formato markdown
- **@carf/tscore** - Biblioteca compartilhada (auth para áreas restritas)
- **Mermaid** - Diagramas em markdown
- **Search** - Busca full-text integrada
- **GitHub Pages** - Deployment automático

## Tecnologias

- VitePress (Vue 3 + Vite)
- TypeScript 5
- @carf/tscore ^0.1.0 (auth/vue)
- Markdown + Mermaid
- Bun runtime

## Setup Local

```bash
# Clonar
git clone https://github.com/Thalesvpr/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE
cd PROJECTS/WEBDOCS/SRC-CODE

# Instalar dependências
bun install

# Dev server
bun dev

# Build production
bun build

# Preview production build
bun preview
```

## Estrutura

```
PROJECTS/WEBDOCS/
├── DOCS/                   # Documentação (esta pasta)
│   ├── README.md           # Este arquivo
│   └── ARCHITECTURE/       # Arquitetura específica
└── SRC-CODE/               # Código-fonte VitePress (carf-webdocs repo)
    ├── .vitepress/
    │   ├── config.ts       # Config VitePress
    │   └── theme/
    │       └── index.ts    # Theme customizado
    ├── docs/               # Markdown docs (synced de CENTRAL/)
    │   ├── index.md        # Homepage
    │   ├── architecture/   # Docs arquitetura
    │   ├── api/            # API reference
    │   └── ...
    └── sync-docs.ts        # Script sincronização CENTRAL/ → docs/
```

## Sincronização Documentação

WEBDOCS não mantém docs manualmente. Docs são sincronizados automaticamente de `carf-docs/CENTRAL/`:

```bash
# sync-docs.ts
import { cpSync } from 'fs'

// Copia CENTRAL/ para docs/
cpSync('../../../CENTRAL', './docs', { recursive: true })
```

CI/CD roda sync antes de build garantindo docs sempre atualizados.

## Integração @carf/tscore

WEBDOCS usa @carf/tscore/auth/vue para proteger áreas restritas (futuro):

### Setup Autenticação

```typescript
// .vitepress/theme/index.ts
import DefaultTheme from 'vitepress/theme'
import { initAuth } from '@carf/tscore/auth/vue'
import { KeycloakClient } from '@carf/tscore/auth'

const keycloakClient = new KeycloakClient({
  url: import.meta.env.VITE_KEYCLOAK_URL,
  realm: 'carf',
  clientId: 'webdocs'
})

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    initAuth(app, keycloakClient)
  }
}
```

### Componente Vue Protegido

```vue
<!-- .vitepress/theme/components/ProtectedContent.vue -->
<script setup lang="ts">
import { useAuth } from '@carf/tscore/auth/vue'
import { Role } from '@carf/tscore/types'

const { isAuthenticated, hasRole, login } = useAuth()
</script>

<template>
  <div v-if="!isAuthenticated">
    <p>Conteúdo restrito. Por favor faça login.</p>
    <button @click="login">Login</button>
  </div>
  <div v-else>
    <slot></slot>
  </div>
</template>
```

## VitePress Config

```typescript
// .vitepress/config.ts
import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'CARF Docs',
  description: 'Documentação sistema CARF',

  themeConfig: {
    logo: '/logo.svg',

    nav: [
      { text: 'Início', link: '/' },
      { text: 'Arquitetura', link: '/architecture/' },
      { text: 'API', link: '/api/' },
      { text: 'Requisitos', link: '/requirements/' }
    ],

    sidebar: {
      '/architecture/': [
        {
          text: 'ADRs',
          items: [
            { text: 'ADR-001: .NET 9 Backend', link: '/architecture/adrs/adr-001' },
            { text: 'ADR-011: Shared Library', link: '/architecture/adrs/adr-011' }
          ]
        }
      ]
    },

    search: {
      provider: 'local'
    }
  },

  markdown: {
    config: (md) => {
      // Mermaid diagrams
      md.use(require('markdown-it-mermaid'))
    }
  }
})
```

## Deployment GitHub Pages

CI/CD workflow:

```yaml
# .github/workflows/deploy.yml
name: Deploy Docs

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - uses: oven-sh/setup-bun@v1

      - name: Install dependencies
        run: bun install

      - name: Sync docs from carf-docs
        run: bun run sync-docs

      - name: Build VitePress
        run: bun run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: .vitepress/dist
```

**URL:** https://thalesvpr.github.io/carf-webdocs/

## Mermaid Diagramas

Suporte nativo Mermaid para diagramas:

```markdown
## Arquitetura Polyrepo

mermaid
graph LR
  A[carf-docs] --> B[carf-tscore]
  A --> C[carf-geoapi]
  A --> D[carf-geoweb]
  B --> D
  B --> E[carf-admin]
  B --> F[carf-webdocs]
```

## Responsabilidades

WEBDOCS serve:

- **Documentação Técnica** - ADRs, arquitetura, patterns
- **API Reference** - Endpoints, schemas, exemplos
- **Requisitos** - Funcionais e não-funcionais
- **Guias** - How-tos, troubleshooting
- **Regras de Negócio** - Processos REURB, validações

## Documentação

- [Arquitetura](./ARCHITECTURE/README.md) - Decisões técnicas específicas do WEBDOCS

## Links

- **Repositório:** https://github.com/Thalesvpr/carf-webdocs
- **GitHub Pages:** https://thalesvpr.github.io/carf-webdocs/
- **@carf/tscore:** [Biblioteca compartilhada](../../TSCORE/DOCS/README.md)

---

**Última atualização:** 2026-01-09
