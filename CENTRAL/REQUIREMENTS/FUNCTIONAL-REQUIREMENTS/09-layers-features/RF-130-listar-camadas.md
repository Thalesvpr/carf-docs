---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: performance
---

# RF-130: Listar Camadas

Este requisito especifica que o sistema deve fornecer endpoint e interface para listar camadas GIS disponíveis no contexto atual do usuário permitindo navegação e gerenciamento do conjunto de layers configurados, onde listagem apresenta informações essenciais de cada camada de forma organizada. A interface deve implementar filtro por comunidade permitindo que usuários visualizem apenas camadas específicas de comunidade selecionada quando aplicável, útil em ambientes multi-comunidade onde cada localidade possui conjunto próprio de camadas temáticas. A listagem deve apresentar camadas ordenadas por campo display_order garantindo que sequência de apresentação no painel de camadas e no mapa respeite ordenação configurada pelos administradores, onde ordem tipicamente reflete Z-index de renderização com camadas base primeiro e overlays temáticos depois. Cada item da lista deve exibir total de features contidas na camada fornecendo indicador visual de densidade de dados, onde usuários podem rapidamente identificar camadas vazias versus populadas e avaliar volume de informação disponível. A listagem deve incluir informações adicionais como nome tipo de geometria visibilidade atual e ícone/cor representativa. O endpoint da API deve suportar paginação para tenants com muitas camadas e permitir filtros adicionais por tipo de geometria ou status. A funcionalidade deve estar disponível nos módulos GEOWEB para popular painel de controle de camadas e GEOAPI via endpoint GET.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
