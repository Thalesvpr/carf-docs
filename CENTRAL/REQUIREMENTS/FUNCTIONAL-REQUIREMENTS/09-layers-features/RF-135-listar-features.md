---
modules: [GEOAPI, GEOWEB, REURBCAD]
epic: other
---

# RF-135: Listar Features

Este requisito estabelece que o sistema deve fornecer endpoint e interface para listar features de uma camada específica permitindo navegação e gerenciamento dos elementos geográficos cadastrados, onde listagem apresenta features com suas geometrias e atributos de forma estruturada. A interface deve implementar filtro por camada como parâmetro obrigatório ou contexto de navegação garantindo que apenas features da layer selecionada sejam exibidas, evitando mistura de dados de diferentes camadas com schemas potencialmente distintos. O sistema deve implementar paginação robusta para camadas com grande volume de features onde resultados são divididos em páginas de tamanho configurável tipicamente 20 a 100 registros, incluindo metadados de paginação como total de registros página atual e total de páginas, permitindo navegação eficiente sem carregar dataset completo. A funcionalidade deve incluir busca por atributos permitindo filtrar features baseado em valores de propriedades customizadas, onde usuário pode especificar campo e valor ou termo de busca e sistema retorna apenas features que correspondem ao critério, implementado através de queries JSON sobre campo properties. A listagem pode incluir representação simplificada da geometria como centroide ou bbox para features complexas. A funcionalidade deve estar disponível nos módulos GEOWEB através de tabelas ou listas de features e GEOAPI via endpoint GET com suporte a query parameters.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
