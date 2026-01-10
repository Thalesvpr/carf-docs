# Key Concepts - WEBDOCS

## Conceitos-Chave

Conceitos-chave: **(1) Static Site Generation (SSG)** - Astro compila todo conteúdo em HTML no build time resultando em sites extremamente rápidos sem necessidade de servidor ou database em runtime, **(2) MDX** - Markdown + JSX permitindo importar e usar componentes React/Astro dentro de arquivos Markdown para interatividade (ex: `<CodeBlock>`, `<MermaidDiagram>`), **(3) Content Collections** - API do Astro para gerenciar conteúdo com type safety via Zod schemas validando frontmatter e providing autocompletion, **(4) Islands Architecture** - componentes interativos (React, Vue) são "islands" de interatividade em página majoritariamente estática, hidratados apenas quando necessário com `client:load` ou `client:visible` reduzindo JavaScript enviado ao cliente, **(5) Zero-JS by Default** - páginas são HTML puro sem JavaScript a menos que explicitamente necessário melhorando performance e SEO.

## SSG vs SSR vs CSR

| Approach | When Rendering | JavaScript | SEO | Performance |
|----------|---------------|------------|-----|-------------|
| **SSG** | Build time | Optional | Excellent | Fastest |
| SSR | Request time | Required | Good | Fast |
| CSR | Browser | Required | Poor | Slow |

WEBDOCS usa **SSG** para máxima performance e SEO.

## Islands Architecture

```astro
---
// Página é HTML estático por padrão
---

<h1>Documentation Page</h1>
<p>This content is static HTML</p>

<!-- Island: componente interativo -->
<SearchBox client:load />
<!-- ↑ Hidratado imediatamente -->

<FeedbackForm client:visible />
<!-- ↑ Hidratado quando visível -->
```

## Content Collections

### Schema Definition

```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content'

const docsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    sidebar: z.object({
      order: z.number().optional(),
    }).optional(),
  }),
})

export const collections = {
  docs: docsCollection,
}
```

### Usage

```typescript
import { getCollection } from 'astro:content'

const docs = await getCollection('docs')

docs.forEach(doc => {
  console.log(doc.data.title)  // Type-safe!
})
```

