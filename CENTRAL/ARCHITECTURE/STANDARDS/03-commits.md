---
type: standard
status: review
updated: 2026-01-22
---

# STD-003: Commits

## Regra

Mensagens de commit seguem Conventional Commits com tipo, escopo opcional e descricao. Tipos permitidos sao feat, fix, docs, style, refactor, test, chore. Escopo indica projeto afetado. Descricao em minusculas sem ponto final. Commits devem ser atomicos representando uma unica mudanca logica.

## Justificativa

Formato padrao permite geracao automatica de changelog e release notes. Commits atomicos facilitam bisect e revert quando necessario.

## Aplicacao

Aplica-se a todos os repositorios do ecossistema CARF. Hook de pre-commit valida formato. Exemplos validos: feat(geoapi): add holder validation, fix(reurbcad): resolve sync conflict on poor connection.
