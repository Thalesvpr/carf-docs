---
modules: [GEOAPI, GEOWEB]
epic: reliability
---

# US-057: Filtrar Unidades no Mapa

Como analista, quero filtrar as unidades visíveis no mapa por diferentes critérios para que a análise seja focada apenas em subconjuntos relevantes de dados, onde a funcionalidade deve fornecer painel de filtros acessível permitindo seleção de múltiplos critérios como status tipo e comunidade, garantindo aplicação em tempo real dos filtros sem necessidade de recarregar página, permitindo exibição de contador mostrando quantidade de unidades visíveis após aplicação dos filtros ativos. Esta funcionalidade é implementada pelo módulo GEOWEB com UI de filtros dinâmicos consumindo GEOAPI através do endpoint GET /api/units com query parameters como status type e community, integrada à visualização de mapa para análise focada. Os critérios de aceitação incluem disponibilidade de painel de filtros facilmente acessível lateral ou superior à visualização do mapa, filtros disponíveis minimamente por status (DRAFT PENDING APPROVED REJECTED) tipo de unidade (RESIDENTIAL COMMERCIAL MIXED) e comunidade, suporte a seleção múltipla dentro de cada categoria de filtro permitindo combinações complexas, aplicação instantânea de filtros em tempo real conforme usuário marca ou desmarca opções sem necessidade de botão "aplicar", atualização automática da visualização do mapa mostrando apenas unidades que atendem critérios selecionados, exibição de contador dinâmico "X unidades visíveis de Y total" refletindo impacto dos filtros ativos, botão "Limpar filtros" permitindo resetar todos filtros de uma vez retornando visualização completa, e persistência de filtros ativos na sessão do usuário mantendo seleção ao navegar entre telas e retornar ao mapa. A rastreabilidade conecta esta user story ao endpoint GET /api/units com suporte a filtragem por query parameters, garantindo flexibilidade analítica e foco em subconjuntos relevantes de dados.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
