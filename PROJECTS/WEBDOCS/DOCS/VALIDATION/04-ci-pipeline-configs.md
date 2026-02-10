---
type: leaf
status: review
updated: 2026-02-07
---

# Pipeline de CI - Configuracoes

Arquivos de configuracao necessarios para o pipeline CI. Arquivos relacionados: visao geral em 04-ci-pipeline-overview.md, workflow completo em 04-ci-pipeline-workflow.md.

## Secrets Necessarios

| Secret | Descricao |
|--------|-----------|
| VERCEL_TOKEN | Token de deploy Vercel |
| VERCEL_ORG_ID | ID da organizacao Vercel |
| VERCEL_PROJECT_ID | ID do projeto |
| LHCI_GITHUB_APP_TOKEN | Token para Lighthouse CI |
| DOCS_REPO_TOKEN | Token para acessar carf-docs |

## Lighthouse CI (lighthouserc.js)

Configuracao de coleta usa comando startServer bun run preview com pattern localhost. URLs verificadas incluem raiz (localhost:4321/), guia (localhost:4321/guia/), e status (localhost:4321/status/). Executa 3 runs por URL.

### Thresholds de Assertiva

| Metrica | Nivel | Threshold |
|---------|-------|-----------|
| Performance | error | minScore 0.9 |
| Accessibility | error | minScore 1.0 |
| Best Practices | error | minScore 0.9 |
| SEO | error | minScore 0.9 |
| First Contentful Paint | warn | maxNumericValue 2000ms |
| Largest Contentful Paint | error | maxNumericValue 2500ms |
| Cumulative Layout Shift | error | maxNumericValue 0.1 |
| Total Blocking Time | warn | maxNumericValue 300ms |

Upload usa target temporary-public-storage para relatorios publicos temporarios.

## Scripts do package.json

| Script | Comando | Descricao |
|--------|---------|-----------|
| dev | astro dev | Servidor de desenvolvimento |
| build | astro build | Build de producao |
| preview | astro preview | Preview do build |
| lint | biome check . | Verificacao de lint |
| lint:fix | biome check --apply . | Correcao automatica de lint |
| typecheck | tsc --noEmit | Verificacao de tipos TypeScript |
| validate | validate:sources + validate:coverage | Todas validacoes |
| validate:sources | bun run scripts/validate-sources.ts | Valida campos source dos MDX |
| validate:coverage | bun run scripts/validate-coverage.ts | Valida cobertura de documentacao |
| validate:terms | bun run scripts/validate-terms.ts | Valida terminologia |
| test:e2e | playwright test | Testes end-to-end |
| test:a11y | playwright test --project=a11y | Testes de acessibilidade |
