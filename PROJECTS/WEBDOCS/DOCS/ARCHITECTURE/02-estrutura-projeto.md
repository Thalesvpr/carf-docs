---
type: leaf
status: review
updated: 2026-01-21
---

# Estrutura do Projeto

Organização de pastas em SRC-CODE/carf-webdocs/ segue convenções do Astro com customizações para Content Collections, autenticação e CMS.

Pasta src/ contém código fonte do projeto. Subpasta content/docs/ armazena documentos Markdown organizados por seção (guia, sistema, manuais, api, dev, changelog). Subpasta pages/ contém páginas especiais que não são content (status.astro, auth/callback.astro). Subpasta components/ agrupa componentes Astro reutilizáveis. Subpasta layouts/ define layouts base para páginas. Subpasta styles/ contém CSS global e imports de ui-components.

Pasta public/ contém assets estáticos servidos diretamente sem processamento. Subpasta images/ organiza screenshots e diagramas por seção. Subpasta admin/ contém configuração do Decap CMS (config.yml e index.html).

Pasta src/content/config.ts define schemas Zod para Content Collections especificando campos obrigatórios e opcionais do frontmatter. Alterações no schema requerem atualização de documentos existentes.

Arquivo astro.config.mjs configura Astro, Starlight, integrações (MDX, Sitemap, Vercel), sidebar navigation, e tema visual. Arquivo principal de configuração do projeto.

Arquivo .env.example documenta variáveis de ambiente necessárias incluindo URLs do Keycloak, client ID, e URLs de serviços para status page. Arquivo .env local não commitado contém valores reais.

Pasta scripts/ contém utilitários de desenvolvimento como validação de estrutura, geração de frontmatter, e helpers para Decap CMS.
