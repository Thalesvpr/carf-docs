---
type: readme
status: review
updated: 2026-01-22
---

# DOMAIN-RULES

Regras de negocio do dominio REURB. Define COMO as coisas funcionam - base legal, transicoes de estado, e validacoes.

## Estrutura

| Pasta | Conteudo |
|-------|----------|
| [LEGAL](./LEGAL/README.md) | Base legal - Lei 13.465/2017, REURB-S, REURB-E |
| [WORKFLOWS](./WORKFLOWS/README.md) | Maquinas de estado e transicoes permitidas |
| [VALIDATIONS](./VALIDATIONS/README.md) | Regras de validacao de dados de negocio |

## Diferenca para DOMAIN

- **DOMAIN**: O QUE sao as coisas (conceitos, glossario)
- **DOMAIN-RULES**: COMO as coisas funcionam (regras, restricoes)

## Diferenca para CENTRAL/WORKFLOWS

- **DOMAIN-RULES/WORKFLOWS**: Regras de transicao (maquina de estados pura)
- **CENTRAL/WORKFLOWS**: Processos end-to-end (fluxo completo de negocio)
