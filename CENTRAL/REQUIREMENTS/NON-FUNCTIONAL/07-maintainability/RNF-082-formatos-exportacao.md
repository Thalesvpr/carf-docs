---
id: RNF-082
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-082: Formatos de Exportacao

## Descricao

Exportacao em multiplos formatos: Shapefile para GIS profissional, GeoJSON para web, KML/KMZ para Google Earth, CSV para planilhas, Excel formatado, PDF para relatorios formais.

## Metricas

- Shapefile: .shp, .shx, .dbf, .prj completos
- GeoJSON: JSON estruturado para web
- KML/KMZ: estilizacao e descricoes
- CSV/Excel/PDF: dados tabulares e relatorios

## Criterios de Aceitacao

1. Cada formato valido e importavel em ferramentas padrao
2. Grandes volumes processados em background com notificacao
3. Metadados incluem origem, data e filtros aplicados
