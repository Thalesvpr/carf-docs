---
id: UC-003
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-24
---

# UC-003: Vincular Titular a Unidade

> **Contexto no Workflow:** Este UC e complementar, executado pelo Analista durante a preparacao de dados (antes da publicacao PARTE 2) ou em cadastros pre-existentes. Ver [WORKFLOW-MESTRE](../../../../CENTRAL/WORKFLOW-MESTRE/README.md).

## Atores

- Primario: ANALYST
- Secundario: Sistema de notificacao

## Pre-condicoes

- Usuario autenticado com permissao para editar unidades
- Unidade habitacional existente no sistema

## Fluxo Principal

1. Usuario acessa tela de detalhes da unidade
2. Sistema exibe secao Titulares com lista de vinculos existentes
3. Usuario clica em Adicionar Titular
4. Sistema exibe modal com opcoes Buscar Existente ou Criar Novo
5. Usuario busca titular por CPF ou nome (ou cria novo)
6. Sistema exibe titular selecionado com campos de relacionamento
7. Usuario seleciona tipo de relacionamento
8. Usuario informa percentual de propriedade
9. Usuario marca se e titular principal (opcional)
10. Usuario clica Vincular
11. Sistema valida regras de negocio
12. Sistema cria vinculo e registra na timeline
13. Sistema exibe confirmacao e atualiza lista

## Fluxos Alternativos

- FA-001: Importar titulares de planilha

## Fluxos de Excecao

- FE-001: CPF/CNPJ invalido
- FE-002: Titular ja vinculado
- FE-003: Soma de percentuais maior que 100%
- FE-004: Multiplos titulares principais

## Pos-condicoes

- Titular vinculado a unidade com tipo e percentual
- Timeline atualizada com evento de vinculo
- Lista de titulares atualizada na interface
