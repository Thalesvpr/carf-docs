---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-012: Controle de Acesso por Recurso

## Descricao

O sistema deve verificar permissoes especificas para cada operacao CRUD em recursos protegidos. Verificacao ocorre antes de executar qualquer operacao, validando role e permissoes do usuario autenticado. Tentativas de acesso negado retornam HTTP 403 Forbidden e sao registradas em log de auditoria para analise de seguranca.

## Criterios de Aceitacao

1. Verificacao de permissao antes de cada operacao CRUD
2. HTTP 403 retornado para acesso nao autorizado
3. Mensagem descritiva do motivo da negacao
4. Log de auditoria registra tentativas negadas
5. Middleware intercepta requisicoes antes dos controllers

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-005, RF-006
