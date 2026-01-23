---
id: UC-002-FE-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-002-FE-002: Solicitar Alteracoes

Fluxo de excecao do UC-002 quando MANAGER identifica necessidade de correcoes antes de aprovar.

## Condicao

No passo 5 do UC-002, MANAGER identifica dados incorretos ou incompletos que impedem aprovacao.

## Fluxo

1. MANAGER identifica problemas nos dados ou geometria
2. MANAGER clica em Solicitar Alteracoes
3. Sistema exibe modal com formulario de solicitacao
4. MANAGER descreve alteracoes necessarias
5. MANAGER seleciona prioridade da solicitacao
6. MANAGER confirma envio
7. Sistema atualiza status para Requires Changes
8. Sistema registra solicitacao na timeline
9. Sistema notifica criador da unidade
10. Sistema exibe confirmacao ao MANAGER

## Fluxo de Correcao

1. Criador recebe notificacao com descricao das alteracoes
2. Criador acessa tela de edicao com banner destacando solicitacao
3. Criador realiza correcoes nos campos indicados
4. Criador salva alteracoes
5. Sistema atualiza status para Pending Approval
6. Unidade retorna para fila de aprovacao

## Resultado

- Unidade com status Requires Changes
- Criador notificado sobre correcoes necessarias
- Timeline registra solicitacao

## Retorno

Unidade sai da lista Pending Approval e aguarda correcao pelo criador.
