# Overview da Arquitetura - WEBDOCS

## Visão Geral

WEBDOCS é site estático gerado com Astro 4 + Starlight theme servindo documentação pública do projeto CARF sincronizada com `CENTRAL/` via processo automatizado que copia arquivos Markdown para `src/content/docs/` aplicando transformações (fix de paths relativos, frontmatter injection), build process do Astro compila Markdown em HTML estático com syntax highlighting via Shiki, search via Pagefind indexing todo conteúdo, e deploy para Vercel com preview deployments em PRs e production deploy em merges para main, site acessível em `https://docs.carf.gov.br` (ou similar) com navegação em sidebar gerada automaticamente do structure de pastas, dark mode toggle, e i18n ready para futuro suporte pt-BR/en.

## Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────┐
│                       Source Content                        │
│                    CENTRAL/**/*.md                          │
│                    (Source of Truth)                        │
└──────────────┬─────────────────────────────────────────────┘
               │
               │ sync-docs.sh (automated sync)
               ▼
┌──────────────────────────────────────────────────────────┐
│                  WEBDOCS Repository                       │
│                                                           │
│  src/content/docs/                                        │
│  ├── domain-model/       ← synced from CENTRAL/          │
│  ├── architecture/                                        │
│  ├── api/                                                 │
│  └── ...                                                  │
└──────────────┬──────────────────────────────────────────┘
               │
               │ Astro build process
               ▼
┌──────────────────────────────────────────────────────────┐
│              Build Pipeline (Astro)                       │
│                                                           │
│  1. MDX Compiler → Transform Markdown                     │
│  2. Shiki → Syntax highlighting                           │
│  3. Starlight → Generate sidebar/ToC                      │
│  4. Vite → Bundle assets                                  │
│  5. Pagefind → Index search                               │
└──────────────┬──────────────────────────────────────────┘
               │
               │ dist/ (static HTML/CSS/JS)
               ▼
┌──────────────────────────────────────────────────────────┐
│                    Vercel CDN                             │
│                                                           │
│  ✓ Global edge network                                   │
│  ✓ Automatic HTTPS                                       │
│  ✓ Preview deployments                                   │
│  ✓ Analytics                                             │
└──────────────────────────────────────────────────────────┘
               │
               │ https://docs.carf.gov.br
               ▼
         [Users / Developers]
```

## Componentes Principais

### 1. Content Layer

Arquivos Markdown em `src/content/docs/` organizados em estrutura de pastas:

```
src/content/docs/
├── index.md                    # Homepage
├── domain-model/
│   ├── index.md
│   ├── entities.md
│   └── relationships.md
├── architecture/
│   ├── adrs/
│   └── patterns/
├── api/
│   ├── authentication.md
│   └── endpoints/
└── guides/
    ├── getting-started.md
    └── deployment.md
```

### 2. Frontmatter

Metadados YAML no topo de cada Markdown:

```yaml
---
title: 'Domain Model'
description: 'Modelo de domínio do sistema CARF'
sidebar:
  order: 1
  badge:
    text: 'New'
    variant: 'success'
---
```

### 3. Starlight Theme

- **Sidebar navigation** - Gerada automaticamente da estrutura de pastas
- **Table of contents** - Headings extraídos do Markdown
- **Dark mode** - Toggle light/dark theme
- **Search** - Pagefind full-text search
- **i18n** - Multi-language support (futuro)

### 4. MDX Support

Permite usar componentes React/Astro em Markdown:

```mdx
import { Card } from '@astrojs/starlight/components'

# Documentation

<Card title="Quick Start" icon="rocket">
  Get started in 5 minutes!
</Card>
```

### 5. Search (Pagefind)

Index automático de todo conteúdo:

```javascript
// Executado no build
import { index } from 'pagefind'

await index({
  source: 'dist',
  bundle_dir: 'dist/pagefind',
})
```

## Fluxo de Sync

### 1. Trigger

```yaml
# .github/workflows/sync-docs.yml
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  workflow_dispatch:      # Manual trigger
  repository_dispatch:    # Triggered by CENTRAL repo
```

### 2. Script

```bash
# scripts/sync-docs.sh
#!/bin/bash

# 1. Clonar repo CENTRAL
git clone https://github.com/user/carf-docs.git /tmp/carf-docs

# 2. Copiar arquivos
cp -r /tmp/carf-docs/CENTRAL/* src/content/docs/

# 3. Transformar paths relativos
find src/content/docs -name "*.md" -exec sed -i 's|../../DOMAIN-MODEL/|/domain-model/|g' {} \;

# 4. Inject frontmatter
node scripts/inject-frontmatter.js

# 5. Commit changes
git add src/content/docs
git commit -m "docs: sync from CENTRAL $(date +%Y-%m-%d)"
git push
```

## Build Process

### 1. Development

```bash
bun run dev
# → Astro dev server em http://localhost:4321
# → Hot reload automático
```

### 2. Production Build

```bash
bun run build
# 1. Validate frontmatter (Zod schemas)
# 2. Process MDX files
# 3. Syntax highlighting (Shiki)
# 4. Generate sidebar/ToC
# 5. Bundle assets (Vite)
# 6. Index search (Pagefind)
# 7. Output to dist/
```

### 3. Output Structure

```
dist/
├── index.html
├── domain-model/
│   └── index.html
├── _astro/
│   ├── [hash].css
│   └── [hash].js
└── pagefind/
    ├── pagefind.js
    └── index.json
```

## Performance

### Optimization Techniques

1. **Static Generation** - Zero JavaScript for content pages
2. **Code Splitting** - Separate bundles per route
3. **Image Optimization** - Automatic resizing/compression
4. **Prefetching** - Preload next pages on hover
5. **Minification** - HTML/CSS/JS minified
6. **Caching** - CDN caching headers

### Metrics

- **Lighthouse Score:** 100/100/100/100 (Performance/Accessibility/Best Practices/SEO)
- **First Contentful Paint:** <1s
- **Time to Interactive:** <2s
- **Total Bundle Size:** <100KB

