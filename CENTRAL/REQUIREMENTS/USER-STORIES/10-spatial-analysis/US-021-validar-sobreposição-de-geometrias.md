---
modules: [GEOAPI, REURBCAD]
epic: performance
---

# US-021: Validar Sobreposição de Geometrias

Como analista, quero que sistema valide sobreposições para que unidades não se sobreponham, onde o sistema executa verificações automáticas de topologia espacial durante criação e edição de unidades detectando e prevenindo sobreposições inválidas entre geometrias de diferentes unidades, garantindo integridade dos dados cadastrais e evitando conflitos territoriais. O cenário principal de uso ocorre automaticamente sempre que um analista desenha, edita ou importa geometria de unidade, onde o sistema executa query espacial em background usando funções PostGIS para identificar outras unidades cujas geometrias intersectam a geometria sendo submetida, permitindo que pequenas sobreposições dentro de tolerância configurável sejam aceitas enquanto sobreposições significativas são bloqueadas com feedback claro ao usuário. Os critérios de aceitação incluem execução de query PostGIS usando função ST_Overlaps para detectar sobreposições entre a geometria submetida e geometrias de unidades existentes no mesmo tenant, definição de tolerância onde sobreposições com área menor que 1m² são consideradas aceitáveis (devido a imprecisões de GPS ou digitalização) mas sobreposições maiores são rejeitadas, apresentação de alerta visual no mapa destacando em cor diferenciada as áreas de sobreposição detectadas permitindo que usuário identifique visualmente o problema, e bloqueio de operação de salvar quando sobreposição excede tolerância com mensagem de erro clara indicando com quais outras unidades há conflito e área da sobreposição. Esta funcionalidade é implementada pelos módulos GEOAPI (validação no endpoint de criação/edição de unidades usando queries espaciais PostGIS com índices GIST para performance) e GEOWEB (visualização de conflitos no mapa com layers de overlay destacando sobreposições), garantindo rastreabilidade com RF-069 (Validação de Sobreposições Geométricas) e UC-001 (Caso de Uso de Gestão de Unidades), onde validação considera apenas unidades ativas (não excluídas) do mesmo tenant, incluindo otimizações de performance usando bounding box para filtrar candidatos antes de calcular interseções precisas.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Pronto
