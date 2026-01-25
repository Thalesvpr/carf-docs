---
id: UC-009-FE-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-009-FE-001: Unidade sem Titular Principal

Fluxo de excecao do UC-009 quando unidade nao possui titular principal vinculado.

## Condicao

No passo 3 do UC-009, sistema detecta que unidade nao possui titular marcado como principal.

## Fluxo

1. Usuario clica em Iniciar Processo de Legitimacao
2. Sistema valida pre-condicoes
3. Sistema detecta ausencia de titular principal
4. Sistema bloqueia criacao do processo
5. Sistema exibe modal informando obrigatoriedade
6. Usuario escolhe vincular titular ou cancelar
7. Se vincular, sistema redireciona para tela de vinculacao
8. Usuario vincula titular e marca como principal
9. Usuario retorna e inicia processo normalmente

## Causas Comuns

- Cadastro incompleto aguardando coleta de documentos
- Multiplos titulares sem definicao de principal
- Unidade importada sem dados de titularidade

## Retorno

Processo bloqueado ate vinculacao de titular principal. Usuario redirecionado para completar cadastro.
