---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-031: Listar Titulares com Filtros

Como analista, quero filtrar titulares por nome, CPF, tipo para que eu encontre registros rapidamente, onde o sistema fornece interface de busca e filtros permitindo localizar titulares específicos em meio a grandes volumes de cadastros, garantindo produtividade nas operações diárias de consulta e vinculação de titulares. O cenário principal de uso ocorre quando analista precisa encontrar titular específico ou conjunto de titulares com características comuns e utiliza controles de filtro e busca para refinar listagem aplicando critérios como nome parcial, CPF/CNPJ, ou tipo de pessoa, permitindo combinação de filtros e visualização de resultados paginados com performance consistente. Os critérios de aceitação incluem filtro de search que aceita busca textual por nome parcial ou CPF/CNPJ completo ou parcial realizando matching case-insensitive e permitindo localização rápida, filtro de type que permite selecionar entre Pessoa Física ou Pessoa Jurídica refinando resultados por categoria de titular, implementação de paginação com navegação entre páginas e controle de quantidade de registros exibidos por página evitando carregamento de datasets grandes, e ordenação por nome em ordem alfabética ascendente facilitando localização visual de titulares na lista. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/holders com query parameters para search, type, page e pageSize usando índices para performance) e GEOWEB (componente de listagem de titulares com controles de filtro, busca e tabela paginada), garantindo rastreabilidade com RF-087 (Listagem e Busca de Titulares), onde resultados respeitam isolamento de tenant mostrando apenas titulares do tenant do usuário, incluindo indicadores visuais de tipo de pessoa e estatísticas de quantidade total de resultados encontrados.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
