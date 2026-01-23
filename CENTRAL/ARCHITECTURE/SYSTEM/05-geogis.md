---
type: leaf
status: current
updated: 2026-01-22
---

# GEOGIS

Plugin QGIS em Python para analises espaciais avancadas e geoprocessamento batch integrando com dados do CARF. Usado por especialistas GIS para validacao topologica em massa, geracao de mapas tematicos e exportacao de dados para outros sistemas.

Stack com QGIS 3.28+, Python 3.9, PyQGIS para acesso a funcionalidades do QGIS, GDAL para processamento raster, Shapely para geometrias e PyProj para reprojecoes. Autenticacao OAuth2 PKCE com desktop flow usando servidor HTTP local temporario e armazenamento seguro de tokens.

## Capacidades

Conexao WFS com GEOAPI para carregar camadas de unidades, comunidades e blocos. Ferramentas de validacao topologica identificando sobreposicoes e gaps. Geoprocessamento batch como buffer, dissolve e spatial join. Importacao de shapefiles com matching automatico de atributos. Exportacao de mapas em layouts padronizados. Detalhes tecnicos em [PROJECTS/GEOGIS/DOCS/](../../../PROJECTS/GEOGIS/DOCS/README.md).
