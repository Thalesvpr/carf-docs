---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-117: Visualizar Foto no Mapa

## Descricao

Sistema deve exibir fotos com coordenadas geograficas como marcadores clicaveis no mapa interativo REURBWEB. Cada foto com geometria Point renderizada como pin diferenciado. Marcadores clicaveis exibem popup com miniatura, data de captura, tipo e descricao permitindo identificacao rapida. Popup inclui link para galeria completa ou visualizacao ampliada. Agrupamento em clusters quando multiplas fotos proximas em zoom distante, expandindo ao aproximar. Camada de fotos no mapa pode ser ativada ou desativada.

## Criterios de Aceitacao

1. Marcadores clicaveis para fotos geotagged
2. Popup com miniatura e metadados
3. Link para visualizacao ampliada
4. Clustering de marcadores proximos
5. Camada togglavel no mapa

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-110, RF-053
