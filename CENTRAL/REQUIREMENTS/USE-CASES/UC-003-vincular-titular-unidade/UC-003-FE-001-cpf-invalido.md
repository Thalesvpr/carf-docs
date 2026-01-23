---
id: UC-003-FE-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-003-FE-001: CPF/CNPJ Invalido

Fluxo de excecao do UC-003 quando CPF ou CNPJ informado e invalido.

## Condicao

Durante criacao de novo titular, usuario informa CPF/CNPJ com digitos verificadores incorretos ou sequencia invalida.

## Fluxo

1. Usuario preenche campo CPF/CNPJ
2. Sistema valida em tempo real apos completar digitos
3. Sistema detecta CPF/CNPJ invalido
4. Sistema exibe icone de erro ao lado do campo
5. Sistema adiciona borda vermelha no campo
6. Sistema desabilita botao de vinculacao
7. Usuario corrige os digitos
8. Sistema re-valida e remove indicadores de erro
9. Sistema habilita botao de vinculacao

## Validacoes

- Comprimento exato (11 para CPF, 14 para CNPJ)
- Sequencias repetidas nao permitidas
- Digitos verificadores conforme algoritmo oficial

## Retorno

Usuario corrige CPF/CNPJ e retorna ao fluxo de criacao de titular.
