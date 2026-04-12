---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-032: Permissoes Granulares

## Descricao

RBAC com permissoes no nivel de recurso e operacao. Nomenclatura padrao: recurso.operacao (units.read, units.write). Roles predefinidos com heranca. Permissoes codificadas em claims JWT.

## Metricas

- Roles: Cadastrador, Supervisor, Admin Municipal, Admin Sistema
- Validacao: backend stateless via JWT claims
- Auditoria: log de todas alteracoes de permissoes

## Criterios de Aceitacao

1. HTTP 403 para acesso sem permissao suficiente
2. Frontend oculta/desabilita acoes nao permitidas
3. Heranca de roles simplifica gerenciamento
