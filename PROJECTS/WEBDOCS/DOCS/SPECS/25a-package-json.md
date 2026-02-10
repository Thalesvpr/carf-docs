---
type: leaf
status: review
updated: 2026-02-07
---

# Package.json e Dependencias

Configuracao do package.json do WEBDOCS. Relacionado com 25b-tooling-config.md.

## Projeto

Nome carf-webdocs versao 0.1.0, type module, private, node >= 20.0.0, packageManager bun@1.1.0.

## Scripts

| Script | Descricao |
|--------|-----------|
| dev / build / preview / check | Comandos Astro padrao |
| validate | Executa validate:content e validate:sources |
| lint / lint:fix / format | Biome check e format |
| test / test:watch | Vitest |
| test:e2e / test:e2e:ui | Playwright |

## Dependencias

| Pacote | Versao | Descricao |
|--------|--------|-----------|
| astro | ^4.16.0 | Framework principal |
| @astrojs/starlight | ^0.28.0 | Template documentacao |
| @astrojs/react | ^3.6.0 | Componentes React |
| @astrojs/mdx | ^3.1.0 | MDX em content |
| @astrojs/sitemap | ^3.2.0 | Sitemap automatico |
| @astrojs/vercel | ^7.8.0 | Deploy Vercel SSR |
| react / react-dom | ^18.3.1 | Runtime React |
| jose | ^5.9.0 | JWT/JWKS no middleware |
| zod | ^3.23.0 | Schema validation |

## Dependencias CARF

@carf/tscore, @carf/geoapi-client e @carf/ui como workspace:* resolvendo para versao local no monorepo.

## Dev Dependencies

| Pacote | Versao |
|--------|--------|
| typescript | ^5.6.0 |
| @types/react, @types/react-dom | ^18.3.0 |
| @biomejs/biome | ^1.9.0 |
| vitest | ^2.1.0 |
| @playwright/test | ^1.48.0 |
| @astrojs/check | ^0.9.0 |
