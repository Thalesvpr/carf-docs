---
modules: [GEOWEB, GEOGIS]
epic: reliability
---

# RF-141: Exportar Camada

Este requisito estabelece que usuários devem poder exportar features de uma camada em múltiplos formatos geoespaciais padrão permitindo interoperabilidade com outros sistemas GIS e backup de dados, onde formatos suportados incluem Shapefile GeoJSON e KML atendendo diferentes casos de uso. A funcionalidade de exportação deve gerar arquivo Shapefile completo com todos componentes .shp .shx .dbf .prj empacotados em ZIP contendo geometrias e atributos das features, GeoJSON como FeatureCollection estruturado conforme especificação RFC 7946 adequado para uso em aplicações web e APIs, e KML para visualização em Google Earth e aplicações que consomem este formato. A exportação deve incluir atributos completos das features onde properties customizadas são mapeadas para campos no DBF do shapefile ou objeto properties no GeoJSON, garantindo que dados descritivos não sejam perdidos durante exportação. O sistema deve garantir que geometrias exportadas são válidas conforme especificação de cada formato, onde validação prévia ou correção automática de geometrias ligeiramente inválidas garante que arquivos gerados sejam aceitos por outros sistemas GIS sem erros. A exportação deve preservar sistema de coordenadas apropriado incluindo arquivo .prj em shapefiles e crs object em GeoJSON. A funcionalidade deve estar disponível nos módulos GEOWEB através de botões de exportação e GEOAPI via endpoints que geram e retornam arquivos.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
