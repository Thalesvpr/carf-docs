---
modules: [GEOAPI, GEOGIS]
epic: performance
---

# RF-131: Tipos de Geometria

Este requisito estabelece que o sistema deve suportar conjunto abrangente de tipos de geometria GIS padrão conforme especificação OGC Simple Features permitindo representação de diversas formas geoespaciais, onde tipos suportados incluem Point para localização pontual única, LineString para sequência conectada de pontos formando linha ou trajeto, Polygon para área fechada com potencial de buracos internos, MultiPoint para conjunto de pontos não conectados, MultiLineString para coleção de linhas separadas, e MultiPolygon para múltiplas áreas possivelmente disjuntas. O sistema deve implementar enum de tipos no backend garantindo valores consistentes e validados em toda aplicação, onde tipo é definido no nível da camada e todas features criadas naquela camada devem respeitar tipo configurado. O sistema deve validar geometrias submetidas conforme tipo esperado rejeitando dados que não correspondem ao tipo da camada, onde validação verifica estrutura correta do GeoJSON ou WKT incluindo número adequado de coordenadas fechamento de anéis em polígonos e ausência de auto-interseções inválidas. A renderização no mapa deve adaptar apresentação visual ao tipo de geometria, onde pontos são renderizados como marcadores ou ícones, linhas como traços com espessura e cor configuradas, e polígonos como áreas preenchidas com borda opcional. O sistema deve utilizar tipos geométricos nativos do PostGIS garantindo queries espaciais eficientes. A funcionalidade é implementada no módulo GEOAPI através de validações e tipos de dados adequados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
