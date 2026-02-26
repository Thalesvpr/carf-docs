---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-141: Exportar Camada

## Descricao

Sistema deve permitir exportacao de features de uma camada em multiplos formatos geoespaciais padrao para interoperabilidade com outros sistemas GIS e backup de dados. Formatos suportados incluem Shapefile completo (.shp, .shx, .dbf, .prj empacotados em ZIP), GeoJSON como FeatureCollection conforme RFC 7946 adequado para aplicacoes web, e KML para visualizacao em Google Earth. Exportacao inclui atributos completos das features onde properties customizadas sao mapeadas para campos no DBF ou objeto properties no GeoJSON. Sistema garante geometrias exportadas validas conforme especificacao de cada formato, com validacao previa ou correcao automatica de geometrias ligeiramente invalidas. Exportacao preserva sistema de coordenadas apropriado incluindo arquivo .prj em shapefiles e crs object em GeoJSON.

## Criterios de Aceitacao

1. Exportacao em Shapefile, GeoJSON e KML
2. Inclusao de atributos completos
3. Validacao de geometrias exportadas
4. Preservacao de sistema de coordenadas
5. Empacotamento em ZIP para shapefiles

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-127, RF-130, RF-136
