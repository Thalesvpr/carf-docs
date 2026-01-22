---
type: leaf
status: review
updated: 2026-01-21
---

# Validação - Integração CI

Configuração de CI para executar validações automaticamente.

Arquivos relacionados:
- Regras de validação: `17-validation-rules.md`
- Scripts: `17-validation-scripts.md`

## package.json Scripts

```json
{
  "scripts": {
    "validate": "bun run validate:sources && bun run validate:links && bun run validate:images",
    "validate:sources": "bun run scripts/validate-sources.ts",
    "validate:links": "bun run scripts/validate-links.ts",
    "validate:images": "bun run scripts/validate-images.ts",
    "validate:terms": "bun run scripts/validate-terms.ts",
    "validate:coverage": "bun run scripts/validate-coverage.ts"
  }
}
```

## Workflow GitHub Actions

```yaml
# .github/workflows/validate.yml
name: Validate Documentation

on:
  pull_request:
    paths:
      - 'src/content/**'
      - 'public/images/**'
  push:
    branches: [main]
    paths:
      - 'src/content/**'
      - 'public/images/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Checkout docs repo
        uses: actions/checkout@v4
        with:
          repository: carf/carf-docs
          path: carf-docs

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install

      - name: Run validation
        env:
          DOCS_REPO_PATH: ./carf-docs
        run: bun run validate

      - name: Comment on PR
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: 'Validação de documentação falhou. Verifique os logs.'
            })
```

---

**Última atualização:** 2026-01-21
**Status do arquivo**: Review
