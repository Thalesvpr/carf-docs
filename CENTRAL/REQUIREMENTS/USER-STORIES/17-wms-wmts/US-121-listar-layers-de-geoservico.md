---
modules: [GEOAPI, GEOWEB]
epic: compatibility
---

# US-121: Listar Layers de Geoservico

Como Analista quero listar layers disponiveis no WMS para que possa selecionar camadas para exibir no sistema, onde o endpoint implementado em GEOAPI expoe a rota /api/geoservices/{id}/layers permitindo consultar as camadas cadastradas em um determinado geoservico WMS, garantindo validacao de permissoes baseada em roles e tratamento adequado de erros HTTP incluindo respostas 401 para usuarios nao autenticados, 403 para usuarios sem permissao e 404 para geoservicos inexistentes, permitindo que o frontend GEOWEB renderize a lista de layers disponiveis para selecao pelo usuario analista, incluindo metadados como nome da camada, tipo de geometria e sistema de referencia espacial, garantindo rastreabilidade ao requisito funcional RF-216 que especifica a necessidade de integracao com servicos WMS externos, onde a documentacao OpenAPI descreve os parametros de entrada incluindo o ID do geoservico e o schema de resposta contendo array de objetos Layer com propriedades id name type e srs, permitindo testes unitarios que validam o mapeamento correto entre a resposta do servico WMS e o modelo de dominio interno, garantindo testes de integracao que verificam a conectividade real com servidores WMS de teste incluindo GeoServer e MapServer, onde a implementacao utiliza HttpClient para realizar requisicoes GetCapabilities ao endpoint WMS configurado, incluindo tratamento de timeout e retry para garantir resiliencia, permitindo cache de respostas por periodo configuravel para reduzir latencia em consultas frequentes, garantindo que alteracoes no catalogo WMS sejam refletidas apos expiracao do cache ou invalidacao manual.

---

**Ultima atualizacao:** 2025-12-30
**Última atualização:** 2026-01-15
**Status do arquivo**: Review
