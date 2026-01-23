---
id: UC-011-FA-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-011-FA-002: Alterar Lider da Equipe

Fluxo alternativo do UC-011 para transferir lideranca para outro membro.

## Condicao

Na tela de detalhes da equipe, usuario clica em Alterar Lider.

## Fluxo

1. Usuario clica botao Alterar Lider
2. Sistema exibe dropdown com membros atuais da equipe
3. Usuario seleciona novo lider
4. Sistema exibe modal de confirmacao
5. Usuario confirma alteracao
6. Sistema atualiza lider da equipe
7. Sistema ajusta papel do antigo lider para Coordenador
8. Sistema notifica antigo lider sobre mudanca
9. Sistema notifica novo lider sobre designacao

## Restricoes

- Novo lider deve ser membro ativo da equipe
- Antigo lider permanece como membro

## Retorno

Lideranca transferida. Ambos usuarios notificados sobre mudanca.
