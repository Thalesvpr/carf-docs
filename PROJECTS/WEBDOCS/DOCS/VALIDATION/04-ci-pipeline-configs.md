---
type: leaf
status: review
updated: 2026-01-21
---

# Pipeline de CI - Configurações

Arquivos de configuração necessários para o pipeline CI.

Arquivos relacionados:
- Visão geral: `04-ci-pipeline-overview.md`
- Workflow completo: `04-ci-pipeline-workflow.md`

## Secrets Necessários

```json
{
  "secrets": {
    "VERCEL_TOKEN": "Token de deploy Vercel",
    "VERCEL_ORG_ID": "ID da organização Vercel",
    "VERCEL_PROJECT_ID": "ID do projeto",
    "LHCI_GITHUB_APP_TOKEN": "Token para Lighthouse CI",
    "DOCS_REPO_TOKEN": "Token para acessar carf-docs"
  }
}
```

## lighthouserc.js

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      startServerCommand: 'bun run preview',
      startServerReadyPattern: 'localhost',
      url: [
        'http://localhost:4321/',
        'http://localhost:4321/guia/',
        'http://localhost:4321/status/'
      ],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 1.0 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['error', { minScore: 0.9 }],
        // Specific audits
        'first-contentful-paint': ['warn', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['warn', { maxNumericValue: 300 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

## Scripts do package.json

```json
{
  "scripts": {
    "dev": "astro dev",
    "build": "astro build",
    "preview": "astro preview",
    "lint": "biome check .",
    "lint:fix": "biome check --apply .",
    "typecheck": "tsc --noEmit",
    "validate": "bun run validate:sources && bun run validate:coverage",
    "validate:sources": "bun run scripts/validate-sources.ts",
    "validate:coverage": "bun run scripts/validate-coverage.ts",
    "validate:terms": "bun run scripts/validate-terms.ts",
    "test:e2e": "playwright test",
    "test:a11y": "playwright test --project=a11y"
  }
}
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
