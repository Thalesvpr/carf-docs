---
modules: [GEOAPI, GEOWEB, GEOGIS]
epic: performance
---

# US-127: Obter Geometria de Quadra

Como Analista quero obter poligono geoespacial da quadra para que possa exibir limites da quadra no mapa de forma otimizada sem carregar metadados desnecessarios, onde o endpoint implementado em GEOAPI expoe a rota /api/blocks/{id}/geometry retornando exclusivamente a geometria GeoJSON da quadra para uso em camadas vetoriais de mapas web, garantindo validacao de permissoes baseada em roles onde usuarios autenticados podem acessar geometrias de quadras do seu tenant, incluindo tratamento de erro 404 Not Found quando ID da quadra nao existe e 403 Forbidden quando usuario tenta acessar quadra de outro tenant, permitindo resposta leve otimizada para rendering em mapas contendo apenas objeto GeoJSON com type coordinates e crs sem metadados adicionais, onde o sistema de referencia espacial CRS retornado e EPSG:4326 WGS84 compativel com bibliotecas de mapa web Leaflet OpenLayers e Mapbox GL, garantindo rastreabilidade ao requisito funcional RF-075 que especifica visualizacao de elementos territoriais, incluindo suporte a content negotiation onde cliente pode requisitar geometry em formatos alternativos incluindo WKT Well-Known Text e WKB Well-Known Binary atraves de header Accept, permitindo que o frontend GEOWEB utilize este endpoint para carregar geometrias sob demanda quando usuario seleciona quadra no mapa reduzindo payload inicial da aplicacao, onde a implementacao em GEOAPI projeta query de banco de dados para selecionar apenas coluna geometry evitando overhead de carregar todas as propriedades da entidade Block, garantindo cache de geometrias no lado servidor com invalidacao automatica quando geometria da quadra for atualizada, incluindo compressao gzip da resposta para reduzir trafego de rede especialmente importante para poligonos complexos com muitos vertices, permitindo parametro de query simplify com valor numerico de tolerancia em metros para simplificacao topologica do poligono usando algoritmo Douglas-Peucker reduzindo quantidade de vertices para melhorar performance de rendering, garantindo testes unitarios que validam serializacao correta de geometrias incluindo MultiPolygon para quadras com geometria descontinua, incluindo testes de integracao que verificam corretude da geometria retornada comparando com geometria armazenada no banco PostGIS e validando que simplificacao nao gera poligonos invalidos.

---

**Ultima atualizacao:** 2025-12-30
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
