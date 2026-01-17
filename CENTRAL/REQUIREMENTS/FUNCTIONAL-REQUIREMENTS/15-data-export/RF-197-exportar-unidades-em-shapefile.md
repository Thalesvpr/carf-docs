---
modules: [GEOGIS]
epic: compatibility
---

# RF-197: Exportar Unidades em Shapefile

O sistema oferece funcionalidade de exportação de unidades territoriais no formato Shapefile, padrão de facto da indústria GIS que garante máxima interoperabilidade com softwares de geoprocessamento desktop como ArcGIS, QGIS e AutoCAD Map, permitindo análises avançadas e integração com workflows externos. A geração de Shapefile cria todos os arquivos componentes obrigatórios incluindo .shp contendo geometrias das features, .shx com índice espacial, .dbf com tabela de atributos e .prj definindo sistema de coordenadas, além de arquivos opcionais como .cpg especificando encoding UTF-8 para correta visualização de caracteres acentuados. Antes da exportação, sistema permite aplicação de filtros que segmentam unidades a exportar conforme critérios como comunidade, status, tipo de ocupação, período de cadastramento ou área espacial de interesse, evitando geração de arquivos excessivamente grandes e focando exportação em subconjunto relevante para análise específica. O arquivo final é empacotado automaticamente em formato ZIP contendo todos os componentes do Shapefile, disponibilizado para download através do navegador ou enviado por email, facilitando distribuição e garantindo que todos os arquivos necessários sejam transferidos conjuntamente sem risco de perda de componentes que tornaria Shapefile inutilizável.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
