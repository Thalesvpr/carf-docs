---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-142: Busca Espacial de Features

## Descricao

Sistema deve fornecer endpoint de API para busca de features baseada em criterios espaciais permitindo localizacao de elementos geograficos atraves de relacoes geometricas. Queries espaciais utilizam capacidades PostGIS para performance otimizada. Parametros espaciais aceitos incluem bounding box (retangulo envolvente por coordenadas minimas e maximas), raio circular (ponto central e distancia em metros), ou poligono arbitrario (GeoJSON ou WKT). Sistema utiliza indice espacial GIST do PostGIS garantindo queries eficientes mesmo em tabelas com milhoes de features. Resposta retorna features como GeoJSON FeatureCollection incluindo geometrias e atributos, com suporte a paginacao. Sistema suporta combinacao de filtros espaciais com filtros de atributos.

## Criterios de Aceitacao

1. Busca por bbox, raio e poligono
2. Indice espacial GIST para performance
3. Resposta em GeoJSON FeatureCollection
4. Suporte a paginacao
5. Combinacao de filtros espaciais e atributos

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-131, RF-135
