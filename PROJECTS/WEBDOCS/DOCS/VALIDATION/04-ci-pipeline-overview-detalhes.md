---
type: leaf
status: review
updated: 2026-02-07
---

# Pipeline de CI - Testes e Deploy

Detalhes de testes automatizados e configuracao de deploy. Documento complementar a 04-ci-pipeline-overview.md.

## Testes

| Teste | Ferramenta | Cobertura | Bloqueia |
|-------|-----------|-----------|----------|
| test:a11y | axe-core via Playwright | Todas paginas principais, WCAG 2.1 AA | Sim |
| test:links | Custom script ou linkinator | Links internos, externos, imagens | Sim |
| test:e2e | Playwright | Navegacao, busca, auth, status page | Sim |

Testes e2e geram screenshots on failure armazenados como artifacts para debug.

## Lighthouse Thresholds

| Metrica | Threshold |
|---------|-----------|
| Performance | minScore 0.9 |
| Accessibility | minScore 1.0 |
| Best Practices | minScore 0.9 |
| SEO | minScore 0.9 |

## Deploy

| Ambiente | Trigger | URL | Verificacao |
|----------|---------|-----|-------------|
| Preview | Pull request | https://webdocs-{branch}-carf.vercel.app | Auto comment no PR |
| Production | Push to main | https://docs.carf.com.br | GET / returns 200, rollback automatico |
