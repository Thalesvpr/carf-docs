---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-217: Excluir Camada WMS/WMTS

## Descricao

Sistema deve permitir remocao de servicos WMS/WMTS configurados atraves de soft delete que marca registro como excluido sem remover fisicamente dados, preservando historico e permitindo restauracao futura. Dialogo de confirmacao obrigatoria alerta sobre impactos listando usuarios que visualizam a camada e dependencias. Ao confirmar, camada removida imediatamente do seletor de todos os usuarios ativos via WebSocket ou polling. Administradores podem consultar camadas excluidas atraves de filtro especifico na listagem, permitindo revisao de historico e restauracao via operacao de undelete acessivel apenas a super_admin.

## Criterios de Aceitacao

1. Soft delete preservando historico
2. Dialogo de confirmacao com impactos
3. Remocao imediata do seletor via WebSocket
4. Filtro para visualizar excluidos
5. Restauracao por super_admin

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-215
