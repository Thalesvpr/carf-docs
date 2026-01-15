---
modules: [GEOAPI, GEOWEB, GEOGIS]
epic: compatibility
---

# US-072: Exportar em Shapefile

Como gestor, quero exportar dados de unidades em formato Shapefile para que integração com sistemas de informação geográfica (GIS) externos como ArcGIS QGIS ou AutoCAD Map seja possível, onde a funcionalidade deve gerar conjunto completo de arquivos Shapefile incluindo geometrias (.shp) atributos (.dbf) índice espacial (.shx) e projeção (.prj), garantindo utilização de SRID correto (EPSG:4326 WGS84 ou conforme configuração do projeto), permitindo seleção de atributos específicos a serem incluídos no arquivo .dbf e disponibilização de arquivo ZIP consolidado para download contendo todos componentes necessários. Esta funcionalidade é implementada pelo módulo GEOWEB com interface de exportação consumindo GEOAPI através do endpoint POST /api/exports?format=shapefile que utiliza bibliotecas geoespaciais (GDAL/OGR Shapely Fiona) para geração de arquivos, integrada ao RF-197 (Exportação Shapefile) e UC-007 (Exportar Dados Geográficos). Os critérios de aceitação incluem geração de conjunto completo de arquivos Shapefile com todos componentes obrigatórios (.shp .dbf .shx .prj), utilização de sistema de referência espacial correto (EPSG:4326 ou configurado) especificado no arquivo .prj, interface permitindo seleção de colunas/atributos a incluir no arquivo .dbf evitando exportação de campos desnecessários, consolidação automática de todos arquivos gerados em arquivo ZIP único para download, preservação de tipos de dados adequados no .dbf (string numeric date) conforme schema original, suporte a geometrias complexas incluindo polígonos com buracos (inner rings) e multipolígonos, aplicação de filtros ativos no momento da exportação exportando apenas registros visíveis conforme critérios do usuário, limitação de quantidade de registros exportados se necessário para evitar arquivos excessivamente grandes, feedback de progresso durante geração especialmente para datasets grandes, e validação de geometrias antes de exportar evitando geometrias inválidas que causariam erro em softwares GIS. A rastreabilidade conecta esta user story ao RF-197 (Exportação Shapefile) UC-007 (Exportar Dados) e endpoint POST /api/exports?format=shapefile, garantindo interoperabilidade com ecossistema GIS padrão da indústria.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
