---
status: review
updated: 2026-01-21
---

# ADR-001: Astro + Starlight como Framework

Decisão escolhendo Astro 4 com Starlight theme para o portal WEBDOCS justificada por static site generation gerando HTML puro no build time com Lighthouse scores próximos a 100 em todas métricas, Content Collections com validação Zod garantindo frontmatter type-safe, sidebar navigation automática da estrutura de pastas, search integrado via Pagefind sem custo de Algolia, dark mode built-in, suporte a MDX para componentes interativos, syntax highlighting via Shiki, e deploy simples em Vercel com preview por PR.

Starlight adiciona tema otimizado para documentação técnica com table of contents, breadcrumbs, mobile-first design e acessibilidade WCAG AA. Hybrid rendering do Astro permite SSG para páginas públicas e SSR para páginas protegidas por autenticação.

Alternativas rejeitadas: Docusaurus (JavaScript excessivo), VitePress (Vue-specific), GitBook (vendor lock-in), Nextra (coupling Next.js), MkDocs (Python dependency), Docsify (SPA prejudica SEO).

Consequências positivas: performance excepcional, SEO otimizado, custo zero, DX superior. Consequências negativas: curva aprendizado Astro, limitação em features interativas complexas.
