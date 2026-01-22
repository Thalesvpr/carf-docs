---
type: leaf
status: review
updated: 2026-01-21
---

# Pipeline de CI - Workflow GitHub Actions

Workflow completo para CI/CD do WEBDOCS.

Arquivos relacionados:
- Visão geral: `04-ci-pipeline-overview.md`
- Configurações: `04-ci-pipeline-configs.md`

## Funcionamento dos Jobs

Job de lint executa Biome para código TypeScript e Astro, e markdownlint para arquivos Markdown. Configuração em arquivos respectivos na raiz do projeto. Erros de lint falham CI com lista de problemas.

Job de type check executa tsc e astro check validando tipos TypeScript e sintaxe Astro. Erros de tipo indicam problemas que podem causar falhas em runtime. Build não prossegue com erros de tipo.

Job de build executa bun run build gerando site estático. Inclui validação de Content Collections (schema Zod), validação de links internos, e geração de índice Pagefind. Falha de build bloqueia deploy.

Job de testes executa Playwright para testes e2e incluindo axe-core para acessibilidade. Testes rodam contra preview deploy gerado pelo Vercel. Screenshots de falhas armazenados como artifacts para debug.

Job de Lighthouse CI executa após deploy de preview medindo performance e gerando relatório. Thresholds definidos em lighthouserc.js. Falha em métricas críticas adiciona comment no PR com detalhes.

Deploy para produção acontece automaticamente após merge em main quando todos checks passam. Vercel detecta push e inicia deploy. Rollback automático se health check falhar após deploy.

## Workflow Completo (.github/workflows/ci.yml)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_ENV: production

jobs:
  # ===========================================
  # VALIDATE
  # ===========================================
  validate:
    name: Validate
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Lint
        run: bun run lint

      - name: Type check
        run: bun run typecheck

      - name: Astro check
        run: bun run astro check

  # ===========================================
  # VALIDATE DOCS
  # ===========================================
  validate-docs:
    name: Validate Documentation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Checkout carf-docs
        uses: actions/checkout@v4
        with:
          repository: carf/carf-docs
          path: carf-docs
          token: ${{ secrets.DOCS_REPO_TOKEN }}

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Validate sources
        env:
          DOCS_REPO_PATH: ./carf-docs
        run: bun run validate:sources

      - name: Validate coverage
        env:
          DOCS_REPO_PATH: ./carf-docs
        run: bun run validate:coverage
        continue-on-error: true

  # ===========================================
  # BUILD
  # ===========================================
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [validate]
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Build
        run: bun run build
        env:
          PUBLIC_SITE_URL: https://docs.carf.com.br
          KEYCLOAK_URL: https://auth.carf.com.br
          KEYCLOAK_REALM: carf
          KEYCLOAK_CLIENT_ID: carf-webdocs

      - name: Upload build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: build-output
          path: dist/
          retention-days: 7

  # ===========================================
  # TEST
  # ===========================================
  test:
    name: Test
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Install Playwright browsers
        run: bunx playwright install --with-deps chromium

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - name: Start preview server
        run: bun run preview &
        env:
          PORT: 4321

      - name: Wait for server
        run: npx wait-on http://localhost:4321

      - name: Run E2E tests
        run: bun run test:e2e

      - name: Run accessibility tests
        run: bun run test:a11y

      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: test-results
          path: |
            test-results/
            playwright-report/

  # ===========================================
  # LIGHTHOUSE
  # ===========================================
  lighthouse:
    name: Lighthouse
    runs-on: ubuntu-latest
    needs: [build]
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}

  # ===========================================
  # DEPLOY PREVIEW
  # ===========================================
  deploy-preview:
    name: Deploy Preview
    runs-on: ubuntu-latest
    needs: [test, validate-docs]
    if: github.event_name == 'pull_request'
    environment:
      name: preview
      url: ${{ steps.deploy.outputs.url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - name: Deploy to Vercel
        id: deploy
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          working-directory: ./dist

      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🚀 Preview deployed: ${{ steps.deploy.outputs.url }}`
            })

  # ===========================================
  # DEPLOY PRODUCTION
  # ===========================================
  deploy-production:
    name: Deploy Production
    runs-on: ubuntu-latest
    needs: [test, lighthouse, validate-docs]
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment:
      name: production
      url: https://docs.carf.com.br
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download build artifacts
        uses: actions/download-artifact@v4
        with:
          name: build-output
          path: dist/

      - name: Deploy to Vercel Production
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
          working-directory: ./dist

      - name: Health check
        run: |
          sleep 30
          curl -f https://docs.carf.com.br/api/health || exit 1
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
