---
type: leaf
status: review
updated: 2026-02-07
---

# Configuracao Astro

Especificacao do arquivo astro.config.mjs do WEBDOCS com Astro e Starlight.

## Configuracao Base

| Propriedade | Valor | Descricao |
|-------------|-------|-----------|
| site | https://docs.carf.com.br | URL de producao |
| output | hybrid | Estatico por padrao, SSR opt-in |
| adapter | @astrojs/vercel/serverless | Deploy Vercel, maxDuration 10s |
| trailingSlash | ignore | URLs com e sem barra equivalentes |

## Starlight

| Propriedade | Valor |
|-------------|-------|
| title | CARF Docs |
| logo.src | ./src/assets/logo.svg |
| social.github | https://github.com/carf |
| defaultLocale | pt-BR |
| pagination | true |
| tableOfContents | min 2, max 3 |
| editLink | github.com/carf/carf-webdocs/edit/main/ |
| credits | false |

CustomCss inclui custom.css e error-pages.css. Override de Header com UserMenu e SiteTitle com versao. Head inclui favicon SVG e preconnect para auth.carf.com.br. Sidebar conforme SPECS/18-sidebar-navigation.md.

## Integracoes

| Integracao | Proposito |
|------------|-----------|
| @astrojs/starlight | Documentacao com navegacao e busca |
| @astrojs/react | Componentes React @carf/ui |
| @astrojs/mdx | Componentes em conteudo |
| @astrojs/sitemap | Sitemap automatico, exclui /dev/ |

## Vite e Build

SSR noExternal para @carf/ui, @carf/tscore e @carf/geoapi-client. OptimizeDeps include react e react-dom. Aliases: @ para /src, @components, @lib e @config. Build com format directory, assets _astro e inlineStylesheets auto. Markdown usa Shiki github-dark com wrap. Redirects mapeiam /docs/slug para /guia/slug.

## Middleware e Types

Middleware em src/middleware.ts com defineMiddleware e sequence combinando authMiddleware. Types em src/env.d.ts declaram ImportMetaEnv e App.Locals com dados do usuario. Detalhes em SPECS/12-env-vars.md.
