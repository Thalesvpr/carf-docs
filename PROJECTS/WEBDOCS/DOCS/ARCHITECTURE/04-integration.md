# Integration - WEBDOCS

## Integração com CENTRAL

Integração com CENTRAL via script `sync-docs.sh` que copia arquivos de `CENTRAL/**/*.md` para `src/content/docs/` transformando paths relativos (ex: `../../DOMAIN-MODEL/` → `/domain-model/`), injeta frontmatter automaticamente inferindo title do H1 e description do primeiro parágrafo, preserva estrutura de pastas, e gera redirects para arquivos movidos, search integration usa Pagefind que indexa todo HTML gerado criando índice JSON em `dist/pagefind/` com suporte a fuzzy search e preview snippets, analytics via Vercel Analytics ou Google Analytics 4 tracking pageviews e search queries, e future integration com @carf/tscore para áreas autenticadas (docs privadas) via protected routes no Astro middleware.

## Sync Workflow

```bash
# .github/workflows/sync-docs.yml
name: Sync Documentation

on:
  repository_dispatch:
    types: [docs-updated]
  schedule:
    - cron: '0 0 * * *'

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./scripts/sync-docs.sh
      - run: git add . && git commit -m "docs: sync from CENTRAL"
      - run: git push
```

## Path Transformations

```javascript
// scripts/transform-paths.js
const transformations = [
  { from: /\.\.\/\.\.\/DOMAIN-MODEL\//g, to: '/domain-model/' },
  { from: /\.\.\/\.\.\/ARCHITECTURE\//g, to: '/architecture/' },
  { from: /\.\.\/\.\.\/API\//g, to: '/api/' },
]

function transformMarkdown(content) {
  transformations.forEach(({ from, to }) => {
    content = content.replace(from, to)
  })
  return content
}
```

## Search Integration

### Pagefind Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config'
import starlight from '@astrojs/starlight'

export default defineConfig({
  integrations: [
    starlight({
      plugins: [
        pagefindPlugin({
          indexing: {
            bundlePath: 'pagefind',
            exclude: ['/404'],
          },
        }),
      ],
    }),
  ],
})
```

### Usage

```javascript
// Search component
const results = await pagefind.search('Clean Architecture')

results.forEach(result => {
  console.log(result.meta.title)      // "Clean Architecture Overview"
  console.log(result.meta.excerpt)    // Preview snippet
  console.log(result.meta.url)        // "/architecture/patterns/clean/"
})
```

## Analytics

### Vercel Analytics

```typescript
// src/layouts/BaseLayout.astro
import { inject } from '@vercel/analytics'

inject()  // Automatic pageview tracking
```

### Custom Events

```typescript
// Track search queries
import { track } from '@vercel/analytics'

track('search', { query: searchTerm })
```

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
