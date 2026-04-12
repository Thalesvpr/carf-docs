---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-143: Analise Espacial Buffer

## Descricao

Sistema deve fornecer funcionalidade de criacao de buffer (zona de influencia) ao redor de features permitindo analise de proximidade e identificacao de areas afetadas. Buffer e poligono que engloba todos os pontos a distancia especificada ou menor da geometria original. Ferramenta aceita parametro de distancia em metros, aplicando operacao via funcoes PostGIS como ST_Buffer com sistema de coordenadas apropriado para calculos metricos precisos. Sistema gera poligono buffer como nova geometria que pode ser visualizada temporariamente no mapa ou salva como nova feature permanente em camada de destino. Suporte a aplicacao de buffer em features individuais ou em lote com opcao de dissolve para unir buffers em geometria unica. Resultado renderizado com estilo diferenciado.

## Criterios de Aceitacao

1. Parametro de distancia em metros
2. Uso de ST_Buffer do PostGIS
3. Visualizacao temporaria ou salvar permanente
4. Buffer individual ou em lote
5. Opcao de dissolve para unir buffers

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-131, RF-132
