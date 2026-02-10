---
type: leaf
status: review
updated: 2026-02-07
---

# Pipeline de CI - Visao Geral

GitHub Actions executa validacoes automaticas em pull requests e deploys garantindo qualidade antes de merge. Arquivos relacionados: workflow em 04-ci-pipeline-workflow.md, configs em 04-ci-pipeline-configs.md.

## Triggers

| Evento | Branches | Condicao |
|--------|----------|----------|
| push | main, develop | Ignora .md e docs/ |
| pull_request | main | opened, synchronize, reopened |

## Stages e Jobs

| Stage | Depende de | Descricao |
|-------|------------|-----------|
| validate | nenhum | Lint, typecheck, validacoes de docs |
| build | validate | Build Astro, artifacts em dist/ (7 dias) |
| test | build | Preview, testes a11y/links/e2e |
| lighthouse | build | Performance com thresholds |
| deploy_preview | test + lighthouse | Vercel preview (apenas PR) |
| deploy_production | test + lighthouse | Vercel production (apenas main) |

## Validacoes de Alinhamento

| Validacao | Checks | Bloqueia |
|-----------|--------|----------|
| validate:sources | Source presente, arquivo existe, compativel com secao | Sim |
| validate:coverage | RFs tem paginas, UCs tem manuais, workflows tem guias | Nao |
| validate:terms | Nomes de entidades, status, roles corretos | Nao |

Detalhes de testes e deploy em 04-ci-pipeline-overview-detalhes.md.
