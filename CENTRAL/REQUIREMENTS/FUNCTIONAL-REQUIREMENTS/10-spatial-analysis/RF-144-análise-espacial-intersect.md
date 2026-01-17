---
modules: [GEOAPI]
epic: performance
---

# RF-144: Análise Espacial: Intersect

Este requisito especifica que o sistema deve fornecer funcionalidade de intersecção espacial permitindo identificar features que intersectam ou se sobrepõem com geometria de referência fornecida, onde análise utiliza relacionamentos topológicos para encontrar coincidências espaciais. O sistema deve expor endpoint de intersect que aceita geometria de consulta como parâmetro fornecida em formato GeoJSON ou WKT representando área polígono linha ou ponto de interesse, retornando todas as features de camada especificada que apresentam qualquer tipo de intersecção espacial com geometria fornecida. A implementação deve utilizar operador ST_Intersects do PostGIS que retorna verdadeiro se geometrias compartilham qualquer porção do espaço incluindo sobreposições parciais toques de bordas ou contenção completa, aproveitando índices espaciais GIST para performance otimizada mesmo em datasets grandes. O endpoint deve retornar features intersectantes como GeoJSON FeatureCollection incluindo geometrias completas e atributos de cada feature que satisfaz critério, onde resultado pode incluir metadados adicionais como área de interseção ou tipo de relacionamento espacial se relevante. A funcionalidade é útil para análises como identificar imóveis afetados por zona de risco definida como polígono, encontrar vias que atravessam área de interesse ou localizar pontos de coleta dentro de bairro específico. A funcionalidade é implementada no módulo GEOAPI através de endpoints de análise espacial.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
