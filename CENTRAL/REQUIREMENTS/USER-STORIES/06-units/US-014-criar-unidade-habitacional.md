---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-014: Criar Unidade Habitacional

Como analista cadastral, quero cadastrar nova unidade com geometria para que propriedades sejam registradas no sistema, onde o processo de criação permite documentar unidades habitacionais com suas características descritivas e representação espacial precisa através de polígonos georreferenciados, garantindo registro completo e rastreável de propriedades em comunidades. O cenário principal de uso inicia quando um analista cadastral acessa o formulário de criação de unidade e preenche campos obrigatórios incluindo código único identificador (code), tipo de unidade (type) e área em metros quadrados, permitindo também desenhar o polígono da geometria diretamente sobre o mapa interativo utilizando ferramentas de desenho onde cada vértice é capturado com coordenadas geográficas precisas. Os critérios de aceitação incluem formulário completo com campos validados para code (único no tenant), type (enumeração de tipos predefinidos) e área calculada automaticamente, ferramenta de desenho de polígono no mapa com capacidade de adicionar vértices clicando no mapa e editá-los antes de confirmar, validação automática de sobreposição com outras unidades existentes onde sobreposições menores que 1m² são aceitáveis mas maiores são bloqueadas, validação de SRID 4326 (WGS84) garantindo que todas as geometrias usam o mesmo sistema de referência espacial, e criação da unidade com status inicial DRAFT indicando que ainda precisa passar por aprovação. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint POST /api/units com validações de geometria usando PostGIS) e GEOWEB (formulário de unidade com mapa MapLibre integrado), garantindo rastreabilidade com RF-049 (Cadastro de Unidades Habitacionais) e UC-001 (Caso de Uso de Gestão de Unidades), onde cada unidade criada é automaticamente associada ao tenant do usuário e registrada em audit log para rastreabilidade completa, incluindo cálculo automático de área através de função ST_Area do PostGIS e validações de integridade geométrica.

---

**Última atualização:** 2025-12-30