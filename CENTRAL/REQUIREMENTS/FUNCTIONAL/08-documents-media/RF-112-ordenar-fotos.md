---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-112: Ordenar Fotos

## Descricao

Sistema deve permitir reordenacao de fotos em galerias via interface drag-and-drop. Campo display_order numerico inteiro mantem ordem personalizada ao inves de fixa por data ou nome. Interface permite arrastar miniaturas para reposicionar, recalculando automaticamente valores de display_order das fotos afetadas. Persistencia imediata salva alteracoes no backend apos soltar foto com feedback visual de sucesso. Util para organizar documentacao fotografica em sequencia logica.

## Criterios de Aceitacao

1. Drag-and-drop de miniaturas
2. Campo display_order para ordenacao
3. Recalculo automatico de ordem
4. Persistencia imediata no backend
5. Feedback visual de sucesso

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-111
