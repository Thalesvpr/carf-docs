# ADR-016: Escolha do Astro + Starlight para Site de Documentação

Decisão arquitetural escolhendo Astro 4 com Starlight theme para site de documentação pública WEBDOCS justificada por static site generation (SSG) gerando HTML puro no build time resultando em sites extremamente rápidos com Lighthouse scores 100/100/100/100 sem JavaScript client-side desnecessário melhorando SEO e acessibilidade, content collections com validation Zod garantindo frontmatter correto e type-safe em Markdown files reduzindo erros de metadados inconsistentes, sidebar navigation automática gerada da estrutura de pastas eliminando configuração manual redundante, search integrado via Pagefind indexando todo conteúdo com fuzzy search e preview snippets sem necessidade de Algolia pago, dark mode toggle built-in respeitando preferência do sistema, i18n ready preparando futuro suporte a português/inglês/espanhol, MDX support permitindo componentes React/Astro em Markdown para interatividade (CodeBlock Mermaid diagrams), syntax highlighting via Shiki com suporte a 100+ linguagens incluindo TypeScript C# SQL, e deployment em Vercel com preview por PR facilitando revisão de documentação antes de merge.

Starlight especificamente adiciona theme otimizado para documentação técnica com table of contents breadcrumbs related pages suggestions, mobile-first responsive design, e acessibilidade WCAG AA compliant.

Alternativas consideradas incluem Docusaurus (rejeitado por ser React-heavy com JavaScript desnecessário degradando performance), VitePress (rejeitado por ser Vue-specific enquanto equipe é React-focused), GitBook (rejeitado por vendor lock-in e custo em tier Pro), Nextra (rejeitado por coupling com Next.js), MkDocs (rejeitado por Python dependency e theme limitado), e Docsify (rejeitado por ser SPA client-side prejudicando SEO).

Consequências positivas incluem performance excepcional, SEO otimizado, custo zero, developer experience superior com HMR, e facilidade de manutenção. Consequências negativas incluem curva de aprendizado de Astro, impossibilidade de features interativas complexas sem JavaScript (aceitável para documentação estática), e migration complexity se decidirmos trocar framework.

Configuração utiliza Astro 4.1+ com Starlight plugin, content em `src/content/docs/` sincronizado de CENTRAL via script automatizado, frontmatter validation com Zod schemas, e Pagefind search indexing habilitado.

Status aprovado e implementado desde 2024-Q4.

---

**Data:** 2025-01-10
**Status:** Aprovado e Implementado
**Decisor:** Equipe de Arquitetura + Documentação
**Última revisão:** 2025-01-10
