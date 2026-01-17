---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# US-128: Listar Lotes de Quadra

Como Analista quero listar lotes dentro de uma quadra para que possa visualizar subdivisoes da quadra e gerenciar lotes individuais de forma organizada, onde o endpoint implementado em GEOAPI expoe a rota /api/blocks/{id}/plots retornando lista paginada de lotes pertencentes a quadra especificada, garantindo validacao de permissoes baseada em roles onde usuarios com role Analyst ou superior podem listar lotes de quadras do seu tenant, incluindo tratamento de erro 404 Not Found quando ID da quadra nao existe e validacao de ownership garantindo que usuario nao acesse lotes de quadras de outros tenants, permitindo filtragem da listagem atraves de query parameters incluindo status para filtrar por DRAFT PENDING APPROVED, search para busca textual em codigo ou nome do lote e sortBy para ordenacao por code area createdAt, onde a resposta inclui paginacao com parametros page size totalCount previousPage nextPage e array items contendo objetos Plot com propriedades id code name area status blockId blockCode createdAt updatedAt, garantindo rastreabilidade ao requisito funcional RF-078 que especifica gerenciamento de lotes, incluindo relacionamento com entidade Block onde cada lote pertence a exatamente uma quadra e relacionamento com entidade Unit onde cada lote pode conter multiplas unidades habitacionais, permitindo que o frontend GEOWEB exiba tabela paginada de lotes com colunas configuradas codigo nome area status e acoes incluindo botoes para editar visualizar no mapa e excluir, onde a implementacao em GEOAPI utiliza specification pattern para construir queries dinamicas baseadas nos filtros aplicados garantindo SQL eficiente sem concatenacao de strings, garantindo que geometrias dos lotes nao sejam incluidas na listagem para reduzir payload sendo carregadas apenas em endpoints especificos de geometria, incluindo campo computado unitCount na resposta indicando quantidade de unidades habitacionais cadastradas em cada lote, permitindo export da listagem em formatos CSV e Excel para analise offline e geracao de relatorios gerenciais, onde testes unitarios validam logica de filtragem paginacao e ordenacao com datasets mock simulando diferentes cenarios de uso, garantindo testes de integracao que verificam recuperacao correta de lotes de uma quadra especifica com isolamento multi-tenant e validacao de indices de performance no banco de dados para queries com filtros complexos, incluindo suporte a range queries para filtrar lotes por faixa de area minima e maxima em metros quadrados facilitando identificacao de lotes fora de padroes estabelecidos.

---

**Ultima atualizacao:** 2025-12-30
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
