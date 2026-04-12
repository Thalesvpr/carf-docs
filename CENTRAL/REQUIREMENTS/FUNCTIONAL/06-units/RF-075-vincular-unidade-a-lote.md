---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-075: Vincular Unidade a Lote

## Descricao

Sistema deve permitir vinculacao de unidades habitacionais a lotes especificos atraves de foreign key plot_id no modelo de unidade. Relacionamento estabelece hierarquia quadra-lote-unidade util em parcelamento formal do solo. Vinculacao inclui validacao garantindo que unidade so pode ser associada a lote da mesma quadra. Sistema oferece filtros por lote nas interfaces de listagem permitindo visualizacao de unidades de determinado lote. Recurso opcional valioso em regularizacao fundiaria com parcelamento planejado.

## Criterios de Aceitacao

1. Campo plot_id no modelo de unidade
2. Validacao de pertencimento a mesma quadra
3. Filtro de unidades por lote
4. Hierarquia quadra-lote-unidade
5. Campo opcional (nullable)

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-074, RF-070
