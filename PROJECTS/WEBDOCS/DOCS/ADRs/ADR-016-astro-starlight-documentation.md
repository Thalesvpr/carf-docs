---
type: adr
status: rejected
description: "Nao e decisao arquitetural. Ferramenta de documentacao e operacional. Mover para PROJECTS/WEBDOCS."
updated: 2026-01-20
---

# ADR-016: Escolha do Astro + Starlight para Site de Documentação

Decisão arquitetural escolhendo Astro 4 com Starlight theme para site de documentação pública WEBDOCS justificada por static site generation (SSG) gerando HTML puro no build time resultando em sites extremamente rápidos com Lighthouse scores 100/100/100/100 sem JavaScript client-side desnecessário melhorando SEO e acessibilidade, content collections com validation Zod garantindo frontmatter correto e type-safe em Markdown files reduzindo erros de metadados inconsistentes, sidebar navigation automática gerada da estrutura de pastas eliminando configuração manual redundante, search integrado via Pagefind indexando todo conteúdo com fuzzy search e preview snippets sem necessidade de Algolia pago, dark mode toggle built-in respeitando preferência do sistema, i18n ready preparando futuro suporte a português/inglês/espanhol, MDX support permitindo componentes React/Astro em Markdown para interatividade (CodeBlock Mermaid diagrams), syntax highlighting via Shiki com suporte a 100+ linguagens incluindo TypeScript C# SQL, e deployment em Vercel com preview por PR facilitando revisão de documentação antes de merge.

Starlight especificamente adiciona theme otimizado para documentação técnica com table of contents breadcrumbs related pages suggestions, mobile-first responsive design, e acessibilidade WCAG AA compliant. Tema visual importa cores e tokens do design system @carf/ui-components garantindo consistência com demais aplicações do ecossistema CARF sem duplicação de definições.

WEBDOCS possui conteúdo próprio escrito diretamente no repositório ao invés de sincronizar de CENTRAL devido a complexidade e fragilidade de manter sync bidirecional entre documentação técnica granular (CENTRAL) e conteúdo orientado a usuários (WEBDOCS) com estrutura de navegação e tom de voz distintos. Decisão prioriza estabilidade e simplicidade operacional permitindo que equipe de documentação edite conteúdo via Git-based CMS Decap sem dependência de scripts de sincronização propensos a conflitos.

Autenticação Keycloak integrada permite seção protegida /dev/ acessível apenas para usuários com role dev contendo Swagger interativo com try-it-out para testar endpoints da GEOAPI usando token real do desenvolvedor, documentação técnica interna sobre arquitetura e padrões de código, métricas e logs de debug dos serviços em ambiente de desenvolvimento, e guias de contribuição com git workflow e code review. Implementação usa hybrid rendering do Astro onde páginas públicas são SSG e páginas protegidas são SSR com middleware validando JWT token do Keycloak. Role dev é transversal e não concede permissões operacionais no sistema CARF sendo necessária atribuição explícita mesmo para usuários admin ou super-admin.

Features adicionais incluem status page em /status/ mostrando health check tempo real dos serviços GEOAPI PostgreSQL Keycloak MinIO obtido via fetch para endpoints /health de cada serviço, changelog em /changelog/ com release notes das versões do ecossistema CARF, banner de notificações editável via Decap CMS para avisos de manutenção programada ou alertas importantes, e diagramas Mermaid renderizados em build time sem JavaScript client-side.

Alternativas consideradas incluem Docusaurus (rejeitado por ser React-heavy com JavaScript desnecessário degradando performance), VitePress (rejeitado por ser Vue-specific enquanto equipe é React-focused), GitBook (rejeitado por vendor lock-in e custo em tier Pro), Nextra (rejeitado por coupling com Next.js), MkDocs (rejeitado por Python dependency e theme limitado), Docsify (rejeitado por ser SPA client-side prejudicando SEO), e sync com CENTRAL (rejeitado por complexidade de manter mapeamento bidirecional e transformação de conteúdo entre formatos distintos).

Consequências positivas incluem performance excepcional, SEO otimizado, custo zero, developer experience superior com HMR, facilidade de manutenção com CMS visual, e segurança de conteúdo técnico interno via role dev. Consequências negativas incluem curva de aprendizado de Astro, impossibilidade de features interativas complexas sem JavaScript (aceitável para documentação), necessidade de manter conteúdo separado de CENTRAL exigindo cuidado para não divergir conceitualmente, e overhead de auth Keycloak em páginas protegidas (aceitável dado baixo volume de acessos a /dev/).

Configuração utiliza Astro 4.1+ com Starlight plugin, content em src/content/docs/ editável via Decap CMS, frontmatter validation com Zod schemas, Pagefind search indexing habilitado, adapter @astrojs/vercel para SSR nas páginas protegidas, e middleware de auth validando token Keycloak em rotas /dev/*.

Status aprovado e implementado desde 2024-Q4, atualizado em 2026-01 para incluir autenticação Keycloak e CMS.
