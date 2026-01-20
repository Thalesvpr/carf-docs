---
id: ""
type: ARCH
modules: []
epic: ""
status: review
created: 2026-01-20
updated: 2026-01-20
---

# Pipeline de CI

GitHub Actions executa validações automáticas em pull requests e deploys garantindo qualidade antes de merge e publicação.

## Triggers

```json
{
  "triggers": {
    "push": {
      "branches": ["main", "develop"],
      "paths_ignore": ["**.md", "docs/**"]
    },
    "pull_request": {
      "branches": ["main"],
      "types": ["opened", "synchronize", "reopened"]
    }
  }
}
```

## Stages e Jobs

```json
{
  "stages": {
    "validate": {
      "runs_on": "ubuntu-latest",
      "steps": [
        "bun install --frozen-lockfile",
        "bun run lint",
        "bun run typecheck",
        "bun run validate:sources",
        "bun run validate:coverage",
        "bun run validate:terms"
      ],
      "description": "Validações de código e documentação"
    },
    "build": {
      "runs_on": "ubuntu-latest",
      "needs": ["validate"],
      "steps": [
        "bun install --frozen-lockfile",
        "bun run build",
        "Verificar dist/ gerado"
      ],
      "artifacts": {
        "name": "build-output",
        "path": "dist/",
        "retention_days": 7
      }
    },
    "test": {
      "runs_on": "ubuntu-latest",
      "needs": ["build"],
      "steps": [
        "Download artifact build-output",
        "bun run preview &",
        "bun run test:a11y",
        "bun run test:links",
        "bun run test:e2e"
      ],
      "artifacts": {
        "name": "test-results",
        "path": "test-results/",
        "if": "failure()"
      }
    },
    "lighthouse": {
      "runs_on": "ubuntu-latest",
      "needs": ["build"],
      "steps": [
        "Download artifact build-output",
        "npx @lhci/cli autorun"
      ],
      "thresholds": {
        "performance": 90,
        "accessibility": 100,
        "best-practices": 90,
        "seo": 90
      }
    },
    "deploy_preview": {
      "runs_on": "ubuntu-latest",
      "needs": ["test", "lighthouse"],
      "if": "github.event_name == 'pull_request'",
      "steps": [
        "Deploy to Vercel preview",
        "Comment PR with preview URL"
      ]
    },
    "deploy_production": {
      "runs_on": "ubuntu-latest",
      "needs": ["test", "lighthouse"],
      "if": "github.ref == 'refs/heads/main'",
      "steps": [
        "Deploy to Vercel production",
        "Verify health check"
      ]
    }
  }
}
```

## Validações de Alinhamento CENTRAL/PROJECTS

```json
{
  "alignment_validations": {
    "validate:sources": {
      "command": "bun run scripts/validate-sources.ts",
      "checks": [
        "Campo source presente em todo MDX",
        "Arquivo referenciado existe",
        "Source compatível com seção"
      ],
      "blocks_merge": true
    },
    "validate:coverage": {
      "command": "bun run scripts/validate-coverage.ts",
      "checks": [
        "RFs têm páginas correspondentes",
        "UCs têm manuais correspondentes",
        "Workflows têm guias"
      ],
      "blocks_merge": false,
      "reports": "Coverage report como comment no PR"
    },
    "validate:terms": {
      "command": "bun run scripts/validate-terms.ts",
      "checks": [
        "Nomes de entidades corretos",
        "Valores de status corretos",
        "Nomes de roles corretos"
      ],
      "blocks_merge": false,
      "reports": "Lista de termos incorretos"
    }
  }
}
```

## Testes

```json
{
  "tests": {
    "test:a11y": {
      "tool": "axe-core via Playwright",
      "coverage": "Todas páginas principais",
      "standard": "WCAG 2.1 AA",
      "blocks_merge": true
    },
    "test:links": {
      "tool": "Custom script ou linkinator",
      "checks": [
        "Links internos existem",
        "Links externos respondem",
        "Imagens carregam"
      ],
      "blocks_merge": true
    },
    "test:e2e": {
      "tool": "Playwright",
      "tests": [
        "Navegação básica",
        "Busca funciona",
        "Auth flow completo",
        "Status page carrega"
      ],
      "blocks_merge": true,
      "screenshots_on_failure": true
    }
  }
}
```

## Deploy

```json
{
  "deploy": {
    "platform": "Vercel",
    "preview": {
      "trigger": "Pull request",
      "url_pattern": "https://webdocs-{branch}-carf.vercel.app",
      "auto_comment": true
    },
    "production": {
      "trigger": "Push to main",
      "url": "https://docs.carf.com.br",
      "health_check": "GET / returns 200",
      "rollback": "Automático se health check falhar"
    }
  }
}
```

## Secrets Necessários

```json
{
  "secrets": {
    "VERCEL_TOKEN": "Token de deploy Vercel",
    "VERCEL_ORG_ID": "ID da organização Vercel",
    "VERCEL_PROJECT_ID": "ID do projeto",
    "LHCI_GITHUB_APP_TOKEN": "Token para Lighthouse CI"
  }
}
```

Workflow .github/workflows/ci.yml dispara em push para main e pull requests. Jobs paralelos executam lint, type check, build, testes, e validações de qualidade. Falha em qualquer job bloqueia merge do PR.

Job de lint executa Biome para código TypeScript e Astro, e markdownlint para arquivos Markdown. Configuração em arquivos respectivos na raiz do projeto. Erros de lint falham CI com lista de problemas.

Job de type check executa tsc e astro check validando tipos TypeScript e sintaxe Astro. Erros de tipo indicam problemas que podem causar falhas em runtime. Build não prossegue com erros de tipo.

Job de build executa bun run build gerando site estático. Inclui validação de Content Collections (schema Zod), validação de links internos, e geração de índice Pagefind. Falha de build bloqueia deploy.

Job de testes executa Playwright para testes e2e incluindo axe-core para acessibilidade. Testes rodam contra preview deploy gerado pelo Vercel. Screenshots de falhas armazenados como artifacts para debug.

Job de Lighthouse CI executa após deploy de preview medindo performance e gerando relatório. Thresholds definidos em lighthouserc.js. Falha em métricas críticas adiciona comment no PR com detalhes.

Deploy para produção acontece automaticamente após merge em main quando todos checks passam. Vercel detecta push e inicia deploy. Rollback automático se health check falhar após deploy.

---

**Última atualização:** 2026-01-20
**Status do arquivo**: Review
