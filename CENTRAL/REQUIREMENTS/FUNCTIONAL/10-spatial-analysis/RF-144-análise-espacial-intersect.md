---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-144: Analise Espacial Intersect

## Descricao

Sistema deve fornecer funcionalidade de interseccao espacial permitindo identificar features que intersectam ou se sobrepoem com geometria de referencia fornecida. Endpoint de intersect aceita geometria de consulta em formato GeoJSON ou WKT representando area de interesse, retornando todas as features de camada especificada que apresentam interseccao espacial. Implementacao utiliza operador ST_Intersects do PostGIS que retorna verdadeiro se geometrias compartilham qualquer porcao do espaco (sobreposicoes parciais, toques de bordas ou contencao completa), aproveitando indices espaciais GIST para performance. Resposta retorna features intersectantes como GeoJSON FeatureCollection com geometrias e atributos. Util para analises como identificar imoveis em zona de risco, vias que atravessam area de interesse ou pontos dentro de bairro especifico.

## Criterios de Aceitacao

1. Geometria de consulta em GeoJSON ou WKT
2. Uso de ST_Intersects do PostGIS
3. Aproveitamento de indices GIST
4. Resposta em GeoJSON FeatureCollection
5. Combinacao com filtros de camada

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-131, RF-142
