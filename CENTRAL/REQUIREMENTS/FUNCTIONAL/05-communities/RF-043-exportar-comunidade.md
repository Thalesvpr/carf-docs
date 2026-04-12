---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-043: Exportar Comunidade

## Descricao

Usuarios autorizados podem exportar dados da comunidade em multiplos formatos geoespaciais. Exportacao em Shapefile gera arquivo ZIP contendo componentes completos (.shp, .shx, .dbf, .prj) com geometria e atributos. Exportacao em KML/KMZ para visualizacao em Google Earth incluindo geometria estilizada. Exportacao em GeoJSON como formato moderno compativel com aplicacoes web GIS. Processamento assincrono para grandes volumes com notificacao ao usuario quando completado.

## Criterios de Aceitacao

1. Exportacao em Shapefile (ZIP completo)
2. Exportacao em KML/KMZ com estilizacao
3. Exportacao em GeoJSON com FeatureCollection
4. Processamento assincrono para grandes volumes
5. URL de download com expiracao temporaria

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-034
