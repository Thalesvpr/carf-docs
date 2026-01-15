---
modules: [GEOAPI]
epic: performance
---

# RF-142: Busca Espacial de Features

Este requisito especifica que o sistema deve fornecer endpoint de API para busca de features baseada em critérios espaciais permitindo localização de elementos geográficos através de relações geométricas ao invés de apenas atributos alfanuméricos, onde queries espaciais utilizam capacidades PostGIS para performance otimizada. O endpoint deve aceitar parâmetros espaciais diversos incluindo bounding box bbox como retângulo envolvente definido por coordenadas mínimas e máximas encontrando features que intersectam esta área, raio circular definido por ponto central e distância em metros retornando features dentro do buffer especificado, ou polígono arbitrário fornecido como GeoJSON ou WKT identificando features que intersectam ou estão contidas na geometria de busca. O sistema deve utilizar índice espacial GIST do PostGIS garantindo que queries espaciais sejam executadas eficientemente mesmo em tabelas com milhões de features, onde índice permite descartar rapidamente features que definitivamente não satisfazem critério espacial antes de computar relacionamentos geométricos complexos. A resposta do endpoint deve retornar features encontradas como GeoJSON FeatureCollection incluindo geometrias completas e atributos de cada feature que satisfez critério de busca, onde resultado pode ser paginado se volume for grande. O sistema deve suportar combinação de filtros espaciais com filtros de atributos permitindo queries como encontre todas edificações tipo residencial dentro de raio de 500m do ponto X. A funcionalidade é implementada no módulo GEOAPI através de endpoints de busca otimizados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
