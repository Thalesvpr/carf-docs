---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-199: Exportar Unidades em GeoJSON

## Descricao

Sistema deve disponibilizar exportacao de unidades em formato GeoJSON, padrao moderno baseado em JSON amplamente utilizado em aplicacoes web e APIs que oferece estrutura simples e legivel para humanos e maquinas. Geracao produz GeoJSON valido conforme especificacao RFC 7946 incluindo FeatureCollection com array de Features onde cada unidade e representada com geometry codificando forma espacial e properties contendo atributos alfanumericos como identificacao, tipo, area e status. Metadados incluem sistema de coordenadas, data de exportacao e filtros aplicados. Arquivo .geojson disponibilizado para download, compativel com bibliotecas JavaScript como Leaflet e OpenLayers, ferramentas Python como Geopandas, e APIs REST. Dados filtrados por tenant_id.

## Criterios de Aceitacao

1. Formato RFC 7946 valido
2. FeatureCollection com geometry e properties
3. Metadados de exportacao
4. Download direto de .geojson
5. Segregacao por tenant_id

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-044, RF-127
