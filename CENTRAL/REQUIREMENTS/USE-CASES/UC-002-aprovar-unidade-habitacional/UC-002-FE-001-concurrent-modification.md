---
id: UC-002-FE-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-002-FE-001: Concurrent Modification

Fluxo de excecao do UC-002 quando unidade ja foi aprovada por outro usuario.

## Condicao

No passo 9 do UC-002, sistema detecta que unidade foi modificada por outro usuario durante a revisao.

## Fluxo

1. Sistema tenta executar aprovacao
2. Sistema detecta que versao da unidade mudou desde carregamento
3. Sistema exibe mensagem informando quem aprovou e quando
4. Sistema atualiza tela com dados atuais da unidade
5. Sistema desabilita botao Aprovar
6. MANAGER visualiza que unidade ja foi aprovada
7. MANAGER retorna para lista de pendentes

## Resultado

- Unidade permanece com status Approved (aprovada pelo outro usuario)
- MANAGER recebe feedback claro sobre o que ocorreu
- Interface atualizada reflete estado atual

## Retorno

MANAGER retorna para lista de pendentes onde unidade nao aparece mais.
