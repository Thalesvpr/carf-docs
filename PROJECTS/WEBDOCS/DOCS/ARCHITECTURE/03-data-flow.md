# Data Flow - WEBDOCS

## Fluxo de Dados

Data flow no build process: **(1) Markdown files** em `src/content/docs/` → **(2) Astro content collections** validam frontmatter com Zod schemas → **(3) Starlight plugin** processa Markdown aplicando syntax highlighting (Shiki), heading IDs, table of contents extraction → **(4) MDX compiler** transforma components React/Astro → **(5) Astro renderer** gera HTML estático → **(6) Vite bundler** otimiza assets (images, CSS, JS) com code splitting → **(7) Pagefind** indexa conteúdo para search → **(8) Output** em `dist/` pronto para deploy, todo processo é incremental em dev mode com HMR (Hot Module Replacement) atualizando página sem reload.

## Pipeline Detalhado

```
[1] Markdown Source
    ↓
[2] Frontmatter Validation (Zod)
    ↓
[3] Markdown Processing (Starlight)
    - Syntax highlighting (Shiki)
    - Heading anchors
    - ToC extraction
    ↓
[4] MDX Compilation
    - JSX → JavaScript
    - Component imports
    ↓
[5] Astro Rendering
    - Server-side render
    - Partial hydration
    ↓
[6] Asset Optimization (Vite)
    - Minify HTML/CSS/JS
    - Image optimization
    - Code splitting
    ↓
[7] Search Indexing (Pagefind)
    - Extract text content
    - Build search index
    ↓
[8] Static Output (dist/)
    - HTML files
    - Optimized assets
    - Search index
```

## Transformações

### Markdown → HTML

```markdown
# Hello World

This is **bold** text.

\`\`\`typescript
const x = 42
\`\`\`
```

Torna-se:

```html
<h1 id="hello-world">
  <a href="#hello-world">Hello World</a>
</h1>
<p>This is <strong>bold</strong> text.</p>
<pre class="shiki"><code><span class="token keyword">const</span> x = <span class="token number">42</span></code></pre>
```

### Frontmatter Injection

```markdown
<!-- Antes -->
# Domain Model

Content here...

<!-- Depois do sync -->
---
title: 'Domain Model'
description: 'Modelo de domínio do sistema CARF'
sidebar:
  order: 1
---

# Domain Model

Content here...
```

## HMR (Hot Module Replacement)

Em dev mode (`bun run dev`), mudanças são refletidas instantaneamente:

```
1. Salvar arquivo .md
2. Astro detecta mudança
3. Recompila apenas arquivo modificado
4. Injeta atualização no navegador
5. Página atualiza sem reload completo
```

