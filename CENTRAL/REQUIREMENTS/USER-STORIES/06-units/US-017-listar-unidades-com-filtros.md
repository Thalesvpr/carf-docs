---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: performance
---

# US-017: Listar Unidades com Filtros

Como analista, quero filtrar unidades por status, tipo, comunidade para que eu encontre registros rapidamente, onde o sistema fornece interface de busca e filtros avançados permitindo localizar unidades específicas em meio a grandes volumes de dados, garantindo produtividade e eficiência nas operações diárias. O cenário principal de uso ocorre quando um analista precisa trabalhar com conjunto específico de unidades e utiliza os controles de filtro para refinar a listagem aplicando critérios como status da unidade (DRAFT, PENDING, APPROVED), tipo de unidade, community_id específica, ou busca textual por código, permitindo combinação de múltiplos filtros simultaneamente e visualização de resultados paginados com performance consistente. Os critérios de aceitação incluem filtros funcionais para status (DRAFT PENDING APPROVED), type (tipos de unidade predefinidos), community_id (ID da comunidade), e search que busca por código da unidade parcial ou completo, implementação de paginação com parâmetros page (número da página) e pageSize (quantidade de registros por página) com valores padrão configuráveis, funcionalidade de ordenação através de parâmetros sort (campo para ordenar como created_at ou code) e order (ASC ou DESC), e garantia de performance onde response time é inferior a 500ms mesmo para datasets com 10.000 unidades através de índices otimizados no banco de dados. Esta funcionalidade é implementada pelos módulos GEOAPI (endpoint GET /api/units com query parameters para filtros, paginação e ordenação, usando índices PostgreSQL para performance) e GEOWEB (componente de listagem com controles de filtro, tabela paginada e indicadores de loading), garantindo rastreabilidade com RF-052 (Listagem e Busca de Unidades) e UC-001 (Caso de Uso de Gestão de Unidades), onde resultados refletem permissões do usuário mostrando apenas unidades do tenant apropriado, incluindo exportação de resultados filtrados e salvamento de filtros favoritos para uso recorrente.

---

**Última atualização:** 2025-12-30**Status do arquivo**: Review
