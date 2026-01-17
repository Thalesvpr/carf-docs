# Layers - WEBDOCS

## Camadas da Aplicação

WEBDOCS tem 3 layers: **(1) Content Layer** - arquivos Markdown em `src/content/docs/` com frontmatter YAML definindo title, description, sidebar order, organizados em estrutura de pastas espelhando CENTRAL (domain-model/, architecture/, api/), **(2) Component Layer** - componentes Astro e React para UI customizada (CodeBlock, Mermaid diagrams, API reference tables, interactive examples) importados em Markdown via MDX, **(3) Layout Layer** - templates Starlight customizados em `src/layouts/` definindo header, footer, sidebar navigation, breadcrumbs, table of contents, e theme colors via CSS variables.

## Content Layer

### Estrutura

```
src/content/docs/
├── domain-model/       # Sincronizado de CENTRAL/DOMAIN-MODEL/
├── architecture/       # Sincronizado de CENTRAL/ARCHITECTURE/
├── api/               # Sincronizado de CENTRAL/API/
└── guides/            # Guias específicos do portal
```

### Frontmatter Schema

```typescript
const docsSchema = z.object({
  title: z.string(),
  description: z.string().optional(),
  sidebar: z.object({
    order: z.number().optional(),
    label: z.string().optional(),
    badge: z.object({
      text: z.string(),
      variant: z.enum(['note', 'success', 'caution', 'danger']),
    }).optional(),
  }).optional(),
})
```

## Component Layer

### Built-in Components

```mdx
import { Card, CardGrid, Aside, Code, Steps } from '@astrojs/starlight/components'

<CardGrid>
  <Card title="Quick Start" icon="rocket">
    Start in 5 minutes
  </Card>
  <Card title="API Reference" icon="seti:api">
    Complete API docs
  </Card>
</CardGrid>

<Aside type="caution">
  Important: This feature is experimental
</Aside>
```

### Custom Components

```astro
---
// src/components/MermaidDiagram.astro
import type { Props } from '@astrojs/starlight/props'
---

<div class="mermaid">
  <slot />
</div>

<script type="module">
  import mermaid from 'mermaid'
  mermaid.initialize({ theme: 'dark' })
</script>
```

## Layout Layer

### Main Layout

```astro
---
// src/layouts/DocsLayout.astro
import StarlightPage from '@astrojs/starlight/components/StarlightPage.astro'
---

<StarlightPage {...Astro.props}>
  <slot name="header" />
  <slot />
  <slot name="footer" />
</StarlightPage>
```

### Navigation

Sidebar gerada automaticamente:

```javascript
// astro.config.mjs
sidebar: [
  {
    label: 'Guides',
    items: [
      { label: 'Getting Started', link: '/guides/getting-started/' },
    ],
  },
  {
    label: 'Reference',
    autogenerate: { directory: 'api' },  // Auto-generate from files
  },
]
```

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
