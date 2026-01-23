---
id: RNF-058
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-058: Linting e Formatacao

## Descricao

ESLint para analise estatica e Prettier para formatacao automatica. Pre-commit hooks via Husky executam validacao antes de commits. CI falha em erros de linting nao corrigidos.

## Metricas

- Linting: ESLint com regras por tecnologia
- Formatacao: Prettier automatico
- Hooks: Husky pre-commit obrigatorio

## Criterios de Aceitacao

1. Pre-commit hooks bloqueiam codigo fora dos padroes
2. CI falha em PRs com violacoes de linting
3. Formatacao padronizada elimina discussoes de estilo
