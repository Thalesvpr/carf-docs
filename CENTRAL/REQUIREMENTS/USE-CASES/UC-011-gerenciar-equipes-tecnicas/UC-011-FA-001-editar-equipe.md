---
id: UC-011-FA-001
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-011-FA-001: Editar Equipe Existente

Fluxo alternativo do UC-011 para modificar dados de equipe ja cadastrada.

## Condicao

No passo 3 do UC-011, usuario clica em editar equipe existente ao inves de criar nova.

## Fluxo

1. Usuario clica icone editar na equipe desejada
2. Sistema abre formulario pre-preenchido com dados atuais
3. Usuario altera nome, descricao ou status
4. Usuario pode trocar lider se necessario
5. Usuario clica Salvar Alteracoes
6. Sistema valida dados (nome unico excluindo propria equipe)
7. Sistema atualiza registro
8. Sistema notifica novo lider se alterado
9. Sistema exibe confirmacao e atualiza listagem

## Campos Editaveis

- Nome da equipe
- Descricao
- Lider responsavel
- Status (Ativa/Inativa)

## Retorno

Equipe atualizada. Listagem reflete alteracoes imediatamente.
