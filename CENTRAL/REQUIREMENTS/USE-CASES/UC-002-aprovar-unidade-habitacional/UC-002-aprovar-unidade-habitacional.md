---
id: UC-002
type: UC
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# UC-002: Aprovar Unidade Habitacional

## Atores

- Primario: MANAGER
- Secundario: Sistema de notificacao

## Pre-condicoes

- Usuario autenticado com role MANAGER
- Unidade com status Pending Approval

## Fluxo Principal

1. MANAGER acessa lista de unidades pendentes
2. Sistema exibe unidades com status Pending Approval ordenadas por antiguidade
3. MANAGER seleciona unidade para revisar
4. Sistema exibe detalhes completos (dados, geometria, fotos, titulares)
5. MANAGER revisa informacoes e geometria no mapa
6. MANAGER clica em Aprovar
7. Sistema exibe modal de confirmacao com campo para comentario
8. MANAGER confirma aprovacao
9. Sistema atualiza status para Approved
10. Sistema registra aprovador e timestamp
11. Sistema envia notificacao ao criador da unidade
12. Sistema exibe confirmacao e atualiza lista

## Fluxos Alternativos

- FA-001: Aprovar em lote

## Fluxos de Excecao

- FE-001: Unidade ja foi aprovada (concurrent modification)
- FE-002: Solicitar alteracoes

## Pos-condicoes

- Unidade com status Approved
- Registro de auditoria criado
- Notificacao enviada ao criador
