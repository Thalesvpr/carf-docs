---
type: leaf
status: review
updated: 2026-02-08
---

# GIS Spatial Patterns

O ecossistema CARF utiliza PostGIS 3.4 como engine geoespacial principal no backend GEOAPI, com SRID 4326 (WGS84) como sistema de coordenadas padrao para armazenamento e EPSG:31983 (SIRGAS 2000 UTM 23S) para calculos metricos precisos.

## Tipos Geometricos

Unidades e comunidades armazenam boundary como geometry(Polygon, 4326) e centroide como geometry(Point, 4326). Quadras (blocks) e lotes (plots) seguem o mesmo padrao. Camadas customizaveis (layers) suportam POINT, LINESTRING e POLYGON conforme layer_type. Todas as geometrias passam por validacao via ST_IsValid antes de persistencia, rejeitando poligonos auto-intersectantes ou com buracos incorretos.

## Funcoes Espaciais

As queries espaciais utilizam funcoes PostGIS em operacoes de negocio. ST_Area calcula area em metros quadrados para preenchimento automatico do campo area de unidades e comunidades. ST_Contains e ST_Intersects verificam sobreposicao entre unidades na mesma comunidade durante criacao e atualizacao. ST_Centroid calcula o ponto central de poligonos para renderizacao de markers em zoom baixo. ST_IsValid valida topologia de geometrias recebidas via API antes de persistir.

## Indices Espaciais

Indices GiST sao criados em todas as colunas geometry para otimizar queries espaciais. O indice GiST em units.boundary acelera verificacao de sobreposicao durante cadastro. O indice GiST em communities.boundary acelera filtros de unidades por area geografica. Indices GIN em layer_features.properties otimizam queries JSONB sobre atributos de features.

## Tiles XYZ

Ortofotos processadas geram tiles no formato XYZ para zoom levels 12 a 20. Cada tile e uma imagem PNG 256x256 pixels servida via endpoint GET /api/orthofotos/{id}/tiles/{z}/{x}/{y} com Cache-Control de 1 dia. Tiles inexistentes retornam 404 para areas sem dados.

## WMS e WMTS

Camadas WMS externas podem ser configuradas por tenant via tabela layers com source_url apontando para servidores WMS/WMTS. O GEOGIS plugin QGIS consome estas camadas para visualizacao de dados complementares como base cartografica, areas de risco e redes de infraestrutura.
