---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-213: Adicionar Camada WMTS

## Descricao

Sistema deve possibilitar adicao de camadas WMTS (Web Map Tile Service) que fornecem tiles pre-renderizados otimizados para desempenho superior a WMS tradicional, especialmente adequadas para basemaps de alta resolucao como imagens de satelite. Configuracao requer URL do servidor WMTS e permite selecao de TileMatrixSet apropriado definindo esquema de piramide de tiles com sistemas de coordenadas e niveis de zoom. Interface permite configurar identificador do layer, formato de imagem preferencial (PNG para transparencia, JPEG para tamanho reduzido), e parametros adicionais como dimensoes temporais. Camadas WMTS proporcionam navegacao mais fluida devido a caching natural do formato tiled.

## Criterios de Aceitacao

1. Configuracao via URL com GetCapabilities
2. Selecao de TileMatrixSet
3. Formato de imagem configuravel (PNG/JPEG)
4. Suporte a dimensoes temporais opcionais
5. Cache automatico de tiles

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-214
