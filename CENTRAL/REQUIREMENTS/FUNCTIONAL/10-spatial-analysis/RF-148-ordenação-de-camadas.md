---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-148: Ordenacao de Camadas

## Descricao

Sistema deve permitir reordenar camadas no painel de controle modificando ordem de empilhamento (Z-index) de renderizacao no mapa, onde camadas no topo da lista sao renderizadas sobre camadas inferiores. Interface implementa drag and drop no painel de camadas com feedback visual mostrando posicao de insercao via linha indicadora. Modelo de dados inclui campo display_order numerico em cada camada armazenando ordem de exibicao, onde valores menores indicam camadas base renderizadas primeiro e valores maiores representam overlays renderizados por cima. Ao reordenar via drag and drop, sistema recalcula automaticamente valores de display_order mantendo sequencia contigua. Atualizacao de renderizacao no mapa ocorre imediatamente apos reordenacao sem necessidade de refresh manual.

## Criterios de Aceitacao

1. Drag and drop para reordenar
2. Feedback visual durante arrasto
3. Campo display_order persistido
4. Recalculo automatico de ordem
5. Atualizacao imediata no mapa

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-130
