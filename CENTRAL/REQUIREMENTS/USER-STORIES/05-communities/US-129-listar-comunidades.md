---
modules: [GEOAPI, GEOWEB]
epic: performance
---

# US-129: Listar Comunidades

Como Analista quero listar todas as comunidades do meu tenant para que possa navegar entre assentamentos e gerenciar unidades habitacionais de forma contextualizada por comunidade, onde o endpoint implementado em GEOAPI expoe a rota /api/communities retornando lista paginada de comunidades com suporte a filtragem busca e ordenacao, garantindo validacao de permissoes baseada em roles onde usuarios autenticados podem listar apenas comunidades do tenant ao qual pertencem garantindo isolamento multi-tenant, incluindo filtragem automatica por tenantId extraido do token JWT sem permitir que parametro seja manipulado pelo cliente, permitindo query parameters para filtragem incluindo status para filtrar por ACTIVE INACTIVE, search para busca textual em nome ou descricao da comunidade e sortBy para ordenacao por name createdAt updatedAt, onde a resposta inclui paginacao com page size totalCount hasNextPage hasPreviousPage e array items contendo objetos Community com propriedades id name description address city state status totalUnits totalBlocks totalPlots createdAt updatedAt, garantindo rastreabilidade ao requisito funcional RF-034 que especifica gerenciamento de comunidades, incluindo campos computados totalUnits totalBlocks totalPlots calculados atraves de agregacao para exibir estatisticas resumidas sem necessidade de requisicoes adicionais, permitindo que o frontend GEOWEB exiba grid de cards ou tabela com informacoes das comunidades incluindo foto de capa localizacao e metricas principais, onde a implementacao em GEOAPI utiliza projection para selecionar apenas campos necessarios na listagem otimizando performance de queries ao banco PostgreSQL, garantindo cache de listagem com invalidacao quando comunidade for criada atualizada ou excluida utilizando estrategia de cache distribuido Redis para ambientes com multiplas instancias da API, incluindo suporte a geolocation filtering onde cliente pode enviar coordenadas latitude longitude e raio para listar comunidades proximas ordenadas por distancia, permitindo paginacao cursor-based como alternativa a offset-based para melhor performance em datasets grandes onde cursor e baseado em ID sequencial, onde testes unitarios validam logica de filtragem ordenacao e calculo de campos computados com mocks de repositorio, garantindo testes de integracao que verificam isolamento multi-tenant validando que usuario de tenant A nao visualiza comunidades de tenant B mesmo manipulando parametros da requisicao, incluindo testes de performance que validam tempo de resposta inferior a 200ms para listagem de 1000 comunidades com agregacoes.

---

**Ultima atualizacao:** 2025-12-30
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
