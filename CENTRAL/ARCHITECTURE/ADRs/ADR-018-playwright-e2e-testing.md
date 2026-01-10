# ADR-018: Escolha do Playwright para Testes End-to-End

Decisão arquitetural escolhendo Playwright como framework de testes E2E para frontends React (GEOWEB ADMIN) justificada por cross-browser testing suportando Chromium Firefox WebKit em paralelo detectando bugs browser-specific, auto-wait inteligente aguardando elementos estarem prontos antes de interação eliminando flaky tests causados por race conditions, network interception permitindo mock de API responses testando error states offline scenarios sem dependência de backend, screenshots e videos automáticos em falhas facilitando debugging de tests falhando apenas em CI, trace viewer interativo permitindo time-travel debugging de tests com DOM snapshots network logs, codegen gerando test code automaticamente gravando interações do usuário acelerando escrita inicial de tests, parallel execution rodando tests em múltiplos workers acelerando suite completa em 60-80%, e TypeScript first-class support com autocomplete de seletores e assertions.

Playwright Test Runner especificamente adiciona fixtures para setup/teardown reutilizável, test retry automático em flaky tests, e reporting rico com HTML reporter.

Alternativas consideradas incluem Cypress (rejeitado por executar em browser limitando alguns cenários e impossibilidade de multi-tab testing), Selenium (rejeitado por setup complexo e flakiness alta), Puppeteer (rejeitado por ser Chromium-only sem Firefox/Safari), TestCafe (rejeitado por performance inferior e ecosystem menor), e testes manuais apenas (rejeitado por não escalar e ser error-prone).

Consequências positivas incluem confidence alta em releases, fast feedback em PRs, cobertura cross-browser, debugging facilitado, e ROI positivo reduzindo bugs produção. Consequências negativas incluem overhead manutenção de tests, execução lenta de suite completa (~5-10min), e curva aprendizado seletores.

Configuração utiliza Playwright 1.40+ com projects para Chromium/Firefox, baseURL configurável, timeout 30s, retries 2 em CI, e screenshots/videos em falhas.

Status aprovado e implementado desde 2024-Q4.

## Implementação

Decisão implementada em [ADMIN](../../../PROJECTS/ADMIN/DOCS/HOW-TO/03-testing.md) e [GEOWEB](../../../PROJECTS/GEOWEB/DOCS/HOW-TO/03-testing.md) com tests em `e2e/` executados via `bun run test:e2e`, cobrindo fluxos críticos (login criar tenant gerenciar usuários visualizar mapa), rodando em GitHub Actions CI em cada PR conforme [pipeline docs](../DEPLOYMENT/04-cicd-pipeline.md), e relatórios HTML acessíveis em artifacts.

---

**Data:** 2025-01-10
**Status:** Aprovado e Implementado
**Decisor:** Equipe de Arquitetura + QA
**Última revisão:** 2025-01-10
