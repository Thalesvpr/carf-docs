---
type: leaf
status: review
updated: 2026-02-07
---

# Pipeline de CI - Workflow

Workflow completo para CI/CD do WEBDOCS definido em .github/workflows/ci.yml. Arquivos relacionados: visao geral em 04-ci-pipeline-overview.md, configs em 04-ci-pipeline-configs.md.

## Funcionamento dos Jobs

Job de lint executa Biome para TypeScript/Astro e markdownlint para Markdown. Job de type check executa tsc e astro check. Job de build executa bun run build com validacao de Collections e indice Pagefind.

Job de testes executa Playwright para e2e incluindo axe-core para a11y. Job de Lighthouse CI mede performance. Deploy para producao acontece automaticamente apos merge em main.

## Configuracao do Workflow

Dispara em push para main e pull_request para main. Concurrency group por workflow e ref com cancel-in-progress. Variavel NODE_ENV production.

Detalhes por job em 04-ci-pipeline-workflow-jobs.md.
