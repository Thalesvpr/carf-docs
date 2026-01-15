---
modules: [GEOGIS]
epic: performance
---

# RF-040: Importar Shapefile de Comunidade

Usuários com role ADMIN podem importar shapefile contendo polígono de comunidade onde upload aceita arquivo ZIP contendo componentes obrigatórios .shp (geometrias) .shx (índice) .dbf (atributos) .prj (projeção) validando presença de todos arquivos necessários antes de processar, validação de geometria garante que features sejam exclusivamente Polygon ou MultiPolygon rejeitando tipos incompatíveis (Point LineString) e verificando validade topológica (sem auto-intersecções buracos válidos polígonos fechados) alertando sobre problemas antes de importação, conversão automática para GeoJSON como formato interno de armazenamento onde geometrias reprojetadas para EPSG:4326 (WGS84) se necessário simplificadas para otimizar performance de renderização e armazenadas em coluna geography do PostgreSQL permitindo queries espaciais eficientes, implementação em módulos GEOWEB e GEOAPI com componente de upload drag-and-drop preview de features importadas antes de confirmação mapeamento de atributos de DBF para campos de comunidade e feedback de progresso durante processamento de arquivos grandes.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
