---
modules: [GEOWEB]
epic: performance
---

# RF-052: Listar Unidades

Usuários podem listar unidades com paginação e filtros avançados onde paginação implementada retornando subconjunto configurável (20 50 100 registros por página) com metadados de total de registros página atual e navegação eficiente, filtros disponíveis incluem status de workflow (DRAFT PENDING APPROVED REJECTED CHANGES_REQUESTED) comunidade vinculada tipo de unidade (Residencial Comercial Mista) período de criação ou última atualização permitindo segmentação precisa de resultados, busca textual por endereço completo ou parcial código identificador único CPF/nome de titular com matching case-insensitive e highlighting de termos encontrados facilitando localização rápida em grandes volumes de dados, ordenação personalizável por múltiplos critérios incluindo data de criação (padrão: mais recentes primeiro) código endereço área status ou data de última modificação com direção ascendente/descendente configurável e persistência de preferências de ordenação entre sessões, implementação em módulos GEOWEB e GEOAPI com interface responsiva (tabela ou cards) controles de filtro interativos busca com debounce para performance ações rápidas (editar visualizar no mapa aprovar) e exportação de resultados filtrados para Excel CSV.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
