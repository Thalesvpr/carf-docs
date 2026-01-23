---
id: UC-001-FE-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-001-FE-001: Validacao Falha

Fluxo de excecao do UC-001 quando validacao de dados falha.

## Condicao

No passo 9 do UC-001, sistema detecta erro de validacao nos dados informados.

## Fluxo

1. Sistema detecta falha em uma ou mais validacoes
2. Sistema interrompe salvamento sem persistir dados
3. Sistema exibe mensagens de erro junto aos campos invalidos
4. Sistema destaca campos com erro visualmente
5. Sistema scrolla para primeiro campo com erro
6. Usuario le mensagens e corrige dados
7. Usuario clica Salvar novamente

## Validacoes

- Campos obrigatorios preenchidos (comunidade, endereco, tipo)
- Geometria valida (fechada, sem auto-intersecao, area minima)
- CPF valido se informado
- Codigo unico na comunidade

## Retorno

Volta ao passo 8 do UC-001 para nova tentativa de salvamento.
