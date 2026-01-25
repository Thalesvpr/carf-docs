---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-131: Tipos de Geometria

## Descricao

Sistema deve suportar conjunto abrangente de tipos de geometria GIS conforme especificacao OGC Simple Features: Point para localizacao pontual, LineString para sequencia conectada de pontos, Polygon para area fechada com potencial de buracos, MultiPoint para conjunto de pontos nao conectados, MultiLineString para colecao de linhas, e MultiPolygon para multiplas areas disjuntas. Enum de tipos no backend garante valores consistentes em toda aplicacao. Tipo definido no nivel da camada e todas features devem respeitar tipo configurado. Validacao de geometrias verifica estrutura correta do GeoJSON ou WKT incluindo numero de coordenadas, fechamento de aneis em poligonos e ausencia de auto-intersecoes. Renderizacao adapta apresentacao visual ao tipo. Sistema utiliza tipos geometricos nativos do PostGIS garantindo queries espaciais eficientes.

## Criterios de Aceitacao

1. Suporte a Point, LineString, Polygon e Multi*
2. Enum de tipos no backend
3. Validacao conforme tipo da camada
4. Verificacao de estrutura geometrica
5. Uso de tipos nativos PostGIS

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-127, RF-132
