---
modules: [GEOAPI, GEOWEB]
epic: security
---

# US-122: Acessar Geoservico via Proxy

Como Sistema quero fazer proxy de requisicoes WMS para que possa evitar problemas de CORS Cross-Origin Resource Sharing e autenticar requests de forma transparente, onde o endpoint implementado em GEOAPI expoe a rota /api/geoservices/{id}/proxy funcionando como intermediario entre o cliente frontend GEOWEB e os servidores WMS externos, garantindo que todas as requisicoes WMS GetMap GetFeatureInfo e GetCapabilities sejam encaminhadas atraves do backend eliminando restricoes de CORS impostas pelos navegadores, permitindo injecao automatica de credenciais de autenticacao configuradas no cadastro do geoservico incluindo HTTP Basic Auth Bearer tokens e certificados mTLS, incluindo validacao de permissoes baseada em roles onde apenas usuarios autenticados com role Analyst ou superior podem acessar o proxy, garantindo tratamento adequado de erros HTTP incluindo timeout ao servidor WMS upstream, erros de DNS, falhas de SSL/TLS e respostas 5xx do servidor remoto, onde a implementacao em GEOAPI utiliza HttpClient configurado com politicas de retry e circuit breaker para garantir resiliencia, permitindo logging detalhado de todas as requisicoes proxied incluindo origem destino latencia e status code para auditoria e troubleshooting, garantindo rastreabilidade ao requisito funcional RF-218 que especifica a necessidade de proxy reverso para geoservicos, incluindo headers de cache-control apropriados para tiles WMS permitindo cache no navegador e CDN, onde a documentacao OpenAPI descreve os parametros de query que sao repassados ao servidor WMS upstream incluindo LAYERS BBOX WIDTH HEIGHT FORMAT e SRS, garantindo testes de integracao que validam o fluxo completo de proxy com servidores WMS reais verificando integridade das imagens retornadas e metadados GetFeatureInfo.

---

**Ultima atualizacao:** 2025-12-30
**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
