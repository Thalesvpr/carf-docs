---
type: leaf
status: review
updated: 2026-02-07
---

# Fluxo de Dados

Especificacao dos fluxos de dados na aplicacao WEBDOCS, cobrindo build time (SSG) e request time (SSR).

## Build Time (SSG)

A maioria das paginas e gerada estaticamente no build. Content Collections sao processadas e validadas.

| Etapa | Input | Processo | Output |
|-------|-------|----------|--------|
| Content Collection | src/content/docs/**/*.mdx | Valida frontmatter com Zod | Collection entries tipadas |
| Page Generation | Entries + [...slug].astro | Renderiza cada entry como HTML | HTML estatico em dist/ |
| Search Index | HTML gerado | Pagefind indexa conteudo | Indice em dist/pagefind/ |
| Sitemap | Todas paginas | @astrojs/sitemap gera XML | dist/sitemap.xml |

## Request Time (SSR)

Rotas com output server ou hybrid sao renderizadas no request.

| Etapa | Trigger | Processo | Output |
|-------|---------|----------|--------|
| Middleware | Toda request HTTP | Ler cookies, decodificar JWT, popular Astro.locals | Request enriquecido |
| Route Matching | Apos middleware | Static serve dist/, dynamic executa server-side | Rota identificada |
| Page Render | Rotas dinamicas | Executa frontmatter, renderiza com Astro.locals e APIs | HTML dinamico |
| API Routes | Request para /api/ | TypeScript processa request | JSON response |

## Cache Strategy

| Tipo | Estrategia | Invalidacao |
|------|-----------|-------------|
| Paginas estaticas | public, max-age=31536000, immutable | Hash no filename |
| Paginas dinamicas | private, no-cache | Conteudo depende do usuario |
| API status | no-store | Dados sempre frescos |
| Swagger spec | Cache interno 5 minutos | TTL expirado |

Fluxos de autenticacao e status page estao em 09-fluxo-dados-detalhes.md.
