---
id: RNF-081
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-081: Formatos de Importacao

## Descricao

Importacao de formatos GIS comuns: Shapefile (.shp/.shx/.dbf/.prj), GeoJSON, KML/KMZ, CSV com coordenadas. Validacao de geometrias e tratamento de erros com importacoes parciais.

## Metricas

- Shapefile: .shp, .shx, .dbf, .prj
- GeoJSON: validacao de estrutura, MultiPolygon, GeometryCollection
- KML/KMZ: parsing XML, descompressao
- CSV: deteccao automatica de delimitadores

## Criterios de Aceitacao

1. Cada formato parseado com tratamento de erros apropriado
2. Geometrias invalidas reportadas ao usuario
3. Importacoes parciais permitem correcao de registros problematicos
