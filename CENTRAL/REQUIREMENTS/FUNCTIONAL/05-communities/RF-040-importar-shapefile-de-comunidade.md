---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-040: Importar Shapefile de Comunidade

## Descricao

Usuarios com role ADMIN podem importar shapefile contendo poligono de comunidade. Upload aceita arquivo ZIP contendo componentes obrigatorios (.shp, .shx, .dbf, .prj) validando presenca de todos arquivos necessarios. Validacao de geometria garante que features sejam exclusivamente Polygon ou MultiPolygon, verificando validade topologica. Conversao automatica para GeoJSON como formato interno de armazenamento, reprojetando para EPSG:4326 se necessario.

## Criterios de Aceitacao

1. Upload de ZIP com componentes shapefile obrigatorios
2. Validacao de presenca de todos arquivos necessarios
3. Validacao de geometria Polygon ou MultiPolygon
4. Conversao para GeoJSON e reprojecao para WGS84
5. Preview de features antes de confirmacao

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-034
