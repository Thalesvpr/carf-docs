---
modules: [GEOWEB, GEOGIS]
epic: compatibility
---

# RF-043: Exportar Comunidade

Usuários autorizados podem exportar dados da comunidade em múltiplos formatos geoespaciais onde exportação em Shapefile gera arquivo ZIP contendo componentes completos (.shp .shx .dbf .prj .cpg) com geometria de boundary atributos alfanuméricos e projeção adequada (EPSG:4326 ou projeção local configurável), exportação em KML/KMZ para visualização em Google Earth incluindo geometria estilizada com cores apropriadas placemark com informações de comunidade e estruturação hierárquica de folders se exportando múltiplas comunidades simultaneamente, exportação em GeoJSON como formato moderno compatível com aplicações web GIS e análises programáticas onde JSON estruturado contém FeatureCollection com Feature por comunidade incluindo properties completas e geometry em coordenadas WGS84, implementação em módulos GEOWEB e GEOAPI com botões de exportação em interface de detalhes ou listagem processamento assíncrono para grandes volumes geração de arquivo temporário em storage com URL de download com expiração e notificação ao usuário quando exportação completada.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
