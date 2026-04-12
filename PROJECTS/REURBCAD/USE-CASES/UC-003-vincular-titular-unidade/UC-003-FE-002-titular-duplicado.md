---
id: UC-003-FE-002
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-003-FE-002: Titular Ja Vinculado

Fluxo de excecao do UC-003 quando titular ja possui vinculo com a unidade.

## Condicao

No passo 11 do UC-003, sistema detecta que titular selecionado ja esta vinculado a mesma unidade.

## Fluxo

1. Sistema detecta vinculo existente
2. Sistema exibe modal informando duplicacao
3. Sistema mostra dados do vinculo atual (tipo, percentual, data)
4. Sistema oferece opcoes ao usuario
5. Usuario escolhe Editar Existente ou Cancelar

## Acoes Disponiveis

- **Editar Vinculo Existente**: Abre modal com dados atuais para alteracao
- **Cancelar**: Fecha modal e retorna para lista de titulares

## Retorno

Se Editar, abre modal de edicao do vinculo existente. Se Cancelar, retorna para lista de titulares.
