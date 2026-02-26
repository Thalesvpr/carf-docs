---
id: UC-011-FE-001
type: UC
modules: []
status: review
created: 2026-01-23
updated: 2026-01-23
---

# UC-011-FE-001: Nome de Equipe Duplicado

Fluxo de excecao do UC-011 quando nome da equipe ja existe no sistema.

## Condicao

No passo 9 do UC-011, sistema detecta que ja existe equipe com mesmo nome.

## Fluxo

1. Sistema valida unicidade do nome
2. Sistema detecta nome duplicado
3. Sistema bloqueia criacao
4. Sistema exibe modal de erro
5. Sistema mantem formulario com dados preenchidos
6. Sistema destaca campo nome com erro
7. Usuario altera nome para variante unica
8. Usuario tenta criar novamente

## Causas Comuns

- Nome identico a equipe ativa existente
- Nome igual a equipe inativa arquivada
- Variacao minima nao detectada pelo usuario

## Retorno

Criacao bloqueada. Usuario altera nome e retenta.
