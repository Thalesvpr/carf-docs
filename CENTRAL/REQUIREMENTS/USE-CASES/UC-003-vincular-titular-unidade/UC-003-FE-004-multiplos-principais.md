---
id: UC-003-FE-004
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-003-FE-004: Multiplos Titulares Principais

Fluxo de excecao do UC-003 quando usuario tenta marcar novo titular como principal mas ja existe outro.

## Condicao

No passo 11 do UC-003, usuario marca titular como principal mas unidade ja possui outro titular principal.

## Fluxo

1. Sistema detecta titular principal existente
2. Sistema exibe modal de confirmacao
3. Sistema informa nome do titular principal atual
4. Sistema pergunta se deseja substituir
5. Usuario escolhe acao

## Acoes Disponiveis

- **Confirmar e Desmarcar Atual**: Desmarca atual e marca novo como principal
- **Manter Atual**: Cria vinculo sem marcar como principal
- **Cancelar**: Aborta operacao

## Resultado

- Se confirmar, timeline registra ambas mudancas
- Apenas um titular permanece como principal

## Retorno

Titular vinculado com ajuste de principal conforme escolha, ou operacao cancelada.
