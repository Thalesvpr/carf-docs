---
type: leaf
status: review
updated: 2026-02-07
---

# Estrutura de Codigo

Especificacao da estrutura de diretorios e arquivos do codigo fonte do WEBDOCS, definindo onde cada tipo de arquivo deve ser criado. O projeto segue convencoes do Astro com customizacoes para integracao Starlight e bibliotecas CARF. Raiz do projeto em SRC-CODE/carf-webdocs/, gerenciador de pacotes Bun, framework Astro 4.x com template Starlight.

## Content e Pages

| Diretorio | Descricao |
|-----------|-----------|
| src/content/docs/guia/ | Paginas de guia do usuario (MDX) |
| src/content/docs/sistema/ | Paginas sobre o sistema CARF |
| src/content/docs/manuais/ | Subpastas geoweb/, reurbcad/, admin/ |
| src/content/docs/api/ | Documentacao de API |
| src/content/docs/dev/ | Documentacao para desenvolvedores |
| src/content/docs/status/ | Pagina de status (single page) |
| src/content/docs/changelog/ | Historico de versoes |
| src/content/incidents/ | Incidentes para status page |
| src/content/config.ts | Schema Zod para frontmatter |
| src/pages/auth/ | login.astro, callback.astro, logout.ts, cms.astro |
| src/pages/api/ | health.ts, refresh.ts, status.ts |
| src/pages/[...slug].astro | Rota catch-all para Starlight |

## Componentes e Lib

| Diretorio | Descricao |
|-----------|-----------|
| src/components/auth/ | LoginButton, UserMenu, ProtectedContent |
| src/components/status/ | StatusGrid, ServiceCard |
| src/components/content/ | Banner, YouTubeEmbed, SwaggerUI |
| src/components/overrides/ | Header, SiteTitle (overrides Starlight) |
| src/layouts/ | BaseLayout.astro com auth check |
| src/lib/auth/ | pkce.ts, tokens.ts, middleware.ts |
| src/lib/services/ | health.ts, swagger.ts |
| src/lib/config/ | env.ts, services.ts |
| src/styles/ | custom.css para tema Starlight |
| src/assets/ | logo.svg, favicon.svg |
| src/middleware.ts | Entry point do middleware Astro |

Diretorio public/ contem admin/ (Decap CMS index.html e config.yml), images/ estaticas, robots.txt, e favicon.ico. Diretorio tests/ contem e2e/ (Playwright) e unit/ (Vitest).

Convencoes de nomenclatura e onde criar cada tipo de arquivo estao em 07-estrutura-codigo-convencoes.md.
