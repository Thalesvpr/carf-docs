---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# RF-065: Buscar Unidade por Localização

O sistema deve oferecer endpoint de busca espacial de unidades através de coordenadas geográficas e raio de distância, onde a API GEOAPI recebe parâmetros lat (latitude), lon (longitude) e radius (raio em metros) retornando todas as unidades dentro da área circular especificada. A implementação utiliza índices espaciais do PostGIS garantindo performance otimizada mesmo com grandes volumes de dados, onde operadores geométricos nativos do PostgreSQL calculam distâncias e interseções espaciais de forma eficiente. Os resultados são automaticamente ordenados por distância crescente do ponto de consulta, apresentando as unidades mais próximas primeiro e facilitando identificação de imóveis nas imediações de uma localização específica. Este recurso é essencial para aplicativos móveis de campo onde agentes podem localizar rapidamente unidades próximas à sua posição atual, para análises de vizinhança e impacto territorial, e para relatórios baseados em proximidade a equipamentos públicos, áreas de risco ou pontos de interesse, permitindo consultas espaciais complexas através de interface simples e intuitiva baseada em coordenadas e raio de busca.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
