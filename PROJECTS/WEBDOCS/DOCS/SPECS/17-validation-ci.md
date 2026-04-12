---
type: leaf
status: review
updated: 2026-02-07
---

# Validacao - Integracao CI

Configuracao de CI para executar validacoes automaticamente. Arquivos relacionados: 17-validation-rules.md e 17-validation-scripts.md.

## Scripts de Validacao

| Script | Comando | Descricao |
|--------|---------|-----------|
| validate | bun run validate:sources e validate:links e validate:images | Executa todas as validacoes |
| validate:sources | bun run scripts/validate-sources.ts | Valida campo source no frontmatter |
| validate:links | bun run scripts/validate-links.ts | Valida links internos |
| validate:images | bun run scripts/validate-images.ts | Valida referencias de imagens |
| validate:terms | bun run scripts/validate-terms.ts | Valida terminologia oficial |
| validate:coverage | bun run scripts/validate-coverage.ts | Verifica cobertura de documentacao |

## Workflow GitHub Actions

O workflow validate.yml dispara em pull requests e push para main quando caminhos src/content/ ou public/images/ sao modificados. O job validate roda em ubuntu-latest com os seguintes passos: checkout do codigo, checkout do repositorio carf/carf-docs no path carf-docs, setup do Bun com versao latest, instalacao de dependencias com bun install, execucao da validacao com variavel DOCS_REPO_PATH apontando para ./carf-docs. Em caso de falha em pull request, usa actions/github-script para comentar no PR informando que a validacao falhou.
