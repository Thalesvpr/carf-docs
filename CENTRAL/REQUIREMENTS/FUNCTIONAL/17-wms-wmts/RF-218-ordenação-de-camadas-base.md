---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-218: Ordenacao de Camadas Base

## Descricao

Sistema deve oferecer interface administrativa de ordenacao de camadas base definindo z-index que controla quais camadas aparecem acima ou abaixo de outras quando multiplas estao ativas simultaneamente, garantindo hierarquia visual apropriada. Interface implementa drag-and-drop intuitivo permitindo reordenar camadas arrastando itens para cima ou para baixo em lista vertical. Ao alterar ordem, sistema atualiza automaticamente campo display_order no banco de dados garantindo persistencia. Mudancas refletidas imediatamente no mapa de todos os usuarios ativos via sincronizacao em tempo real sem necessidade de recarregar pagina.

## Criterios de Aceitacao

1. Interface drag-and-drop
2. Controle de z-index
3. Persistencia em display_order
4. Sincronizacao em tempo real
5. Hierarquia visual configuravel

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-212, RF-213
