---
id: UC-005-FE-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-005-FE-001: Perda de Conexao Durante Sync

Fluxo de excecao do UC-005 quando conexao e perdida durante sincronizacao.

## Condicao

Em qualquer fase do UC-005 (PULL ou PUSH), app detecta perda de conexao com internet.

## Fluxo

1. App detecta perda de conexao
2. App pausa sincronizacao imediatamente
3. App salva checkpoint do estado atual
4. Sistema exibe modal informando pausa
5. Sistema oferece opcoes ao usuario

## Acoes Disponiveis

- **Retentar Agora**: Verifica conexao e retoma de checkpoint
- **Cancelar**: Aborta e agenda retry automatico

## Checkpoint Salvo

- ID do ultimo item sincronizado
- Fase atual (PULL ou PUSH)
- Itens restantes

## Retorno

Sincronizacao pausada com checkpoint. Retomada automatica quando conexao volta.

## Pos-condicoes

- Estado de sincronizacao preservado
- Listener de conectividade ativo para retomada automatica
