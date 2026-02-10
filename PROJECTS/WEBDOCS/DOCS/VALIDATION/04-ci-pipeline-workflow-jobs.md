---
type: leaf
status: review
updated: 2026-02-07
---

# Pipeline de CI - Detalhes dos Jobs

Detalhes de cada job do workflow CI. Documento complementar a 04-ci-pipeline-workflow.md.

## Job validate

Runner ubuntu-latest. Checkout, setup Bun latest, install frozen-lockfile, lint, typecheck, astro check.

## Job validate-docs

Runner ubuntu-latest. Checkout repo principal e carf-docs (com DOCS_REPO_TOKEN). Setup Bun, install, validate:sources com DOCS_REPO_PATH=./carf-docs, validate:coverage com continue-on-error.

## Job build

Depende de validate. Checkout, Bun, install, build com envs PUBLIC_SITE_URL, KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID. Upload artifact build-output de dist/ com retencao 7 dias.

## Job test

Depende de build. Checkout, Bun, install, Playwright chromium, download build-output para dist/, preview server porta 4321, wait-on, test:e2e e test:a11y. Upload test-results se falhar.

## Job lighthouse

Depende de build. Checkout, Node 20, download build-output, @lhci/cli autorun com LHCI_GITHUB_APP_TOKEN.

## Job deploy-preview

Depende de test e validate-docs, apenas em pull_request. Deploy via vercel-action com tokens. Comment no PR com URL via github-script.

## Job deploy-production

Depende de test, lighthouse, validate-docs, apenas em push main. Deploy Vercel com --prod. Health check via curl apos 30 segundos.
