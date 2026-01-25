---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-033: Notificacoes In-App

## Descricao

Usuarios recebem notificacoes de acoes relevantes incluindo aprovacoes de unidades, comentarios em documentos, solicitacoes de alteracao por MANAGER, atribuicao a nova equipe ou comunidade e outras interacoes importantes. Badge de notificacoes nao lidas exibido em icone na barra de navegacao mostrando quantidade numerica com destaque visual. Painel de notificacoes exibe lista cronologica reversa com timestamp, tipo, resumo e link direto para recurso relacionado.

## Criterios de Aceitacao

1. Badge com contador de notificacoes nao lidas
2. Painel cronologico com timestamp e resumo
3. Link direto para recurso relacionado
4. Marcacao de lido/nao-lido individual e em lote
5. Atualizacao em tempo real via polling ou WebSocket

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-001
