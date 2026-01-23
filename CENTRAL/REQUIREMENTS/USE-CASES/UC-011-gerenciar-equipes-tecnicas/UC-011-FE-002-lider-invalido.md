---
id: UC-011-FE-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-011-FE-002: Lider Invalido ou Inativo

Fluxo de excecao do UC-011 quando lider selecionado nao esta disponivel.

## Condicao

No passo 9 do UC-011, sistema detecta que usuario selecionado como lider esta inativo ou foi removido.

## Fluxo

1. Sistema valida lider selecionado
2. Sistema detecta usuario inativo ou inexistente
3. Sistema bloqueia criacao
4. Sistema exibe modal de erro
5. Sistema recarrega dropdown com usuarios ativos
6. Sistema reseta campo lider
7. Usuario seleciona outro lider da lista atualizada
8. Usuario tenta criar novamente

## Causas Comuns

- Usuario desativado entre carregar formulario e submeter
- Usuario removido do sistema
- Selecao de usuario de outro tenant (erro de dados)

## Retorno

Criacao bloqueada. Usuario seleciona lider ativo e retenta.
