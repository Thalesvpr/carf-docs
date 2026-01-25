---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-083: Sistemas de Coordenadas

## Descricao

Suporte a SRIDs comuns no Brasil: EPSG 4326 (WGS84) e SIRGAS 2000 UTM (31982-31985). Reprojecao automatica via PostGIS ST_Transform. Deteccao automatica de CRS em importacoes.

## Metricas

- EPSG 4326: WGS84 para GPS e mapas web
- EPSG 31982-31985: SIRGAS 2000 UTM zonas 22S-25S
- Precisao: sub-metro em transformacoes

## Criterios de Aceitacao

1. Geometrias armazenadas, consultadas e exportadas em qualquer SRID suportado
2. Deteccao automatica de CRS em .prj de Shapefiles e GeoJSON
3. Transformacoes preservam precisao dentro de tolerancias aceitaveis
