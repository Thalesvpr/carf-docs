---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-058: Busca Espacial

Como analista, quero buscar unidades desenhando uma área de interesse diretamente no mapa para que a seleção geográfica de unidades seja fácil e intuitiva, onde a funcionalidade deve permitir desenhar retângulo ou polígono livre sobre o mapa para definir área de busca, garantindo execução de query espacial PostGIS ST_Within no backend para identificar unidades contidas na geometria desenhada, permitindo que resultados sejam filtrados automaticamente no mapa e em listagens mostrando apenas unidades dentro da área selecionada. Esta funcionalidade é implementada pelo módulo GEOWEB com ferramentas de desenho de geometrias consumindo GEOAPI através do endpoint POST /api/units/spatial-search que processa query espacial, integrada ao RF-065 (Busca Espacial de Unidades) para seleção geográfica avançada. Os critérios de aceitação incluem disponibilidade de ferramenta de desenho de retângulo permitindo clicar e arrastar para definir área retangular de busca, ferramenta alternativa de polígono livre permitindo desenhar área irregular através de cliques sequenciais definindo vértices, execução automática de busca ao completar desenho da geometria enviando GeoJSON ao endpoint de spatial search, processamento no backend utilizando PostGIS ST_Within ou ST_Intersects conforme configuração para identificar unidades contidas ou intersectando área, retorno e renderização imediata no mapa apenas de unidades que atendem critério espacial, exibição de contador mostrando "X unidades encontradas na área selecionada", opção de exportar lista de unidades encontradas para CSV ou outro formato, e capacidade de limpar seleção espacial retornando visualização completa com botão "Limpar área". A rastreabilidade conecta esta user story ao RF-065 (Busca Espacial) e ao endpoint POST /api/units/spatial-search, garantindo capacidade de seleção geográfica intuitiva para análises espaciais complexas.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
