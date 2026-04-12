---
type: adr
status: accepted
updated: 2026-02-07
description: "Decisao de padronizar OAuth2 flows por tipo de cliente no ecossistema CARF."
---

# ADR-002: OAuth2 Flows por Tipo de Client

## Contexto

O ecossistema CARF possui tipos distintos de clientes: SPAs web como REURBWEB, ADMIN e WebDocs, aplicacao mobile REURBCAD, backend GEOAPI e desktop GEOGIS. SPAs nao podem armazenar secrets pois o codigo JavaScript e publico. Mobile apps possuem secure storage mas devem usar flows nativos. Backends podem usar client secret pois o codigo fica no servidor. Cada tipo de cliente exige o flow OAuth2 adequado ao seu modelo de ameacas.

## Decisao

SPAs e mobile usam Authorization Code com PKCE como clientes publicos conforme RFC 8252 e OAuth 2.1 draft. GEOAPI opera como bearer-only validando JWTs recebidos dos frontends sem executar flow proprio. GEOGIS usa Authorization Code com PKCE para fluxo interativo e Client Credentials para comunicacao machine-to-machine. Nenhuma SPA ou mobile app armazena client secret.

## Consequencias

Cada tipo de cliente usa o flow otimizado para suas restricoes de seguranca. A implementacao segue as RFCs 6749, 7636 e 8252 garantindo interoperabilidade com bibliotecas padrao como keycloak-js e oidc-client-ts. Nenhum secret fica exposto em codigo publico. Em contrapartida, desenvolvedores precisam entender o mecanismo de PKCE com code verifier e code challenge embora bibliotecas abstraiam a complexidade. GEOGIS requer gerenciamento de client secret com rotacao periodica.

## Alternativas Rejeitadas

Implicit Flow foi rejeitado por estar deprecado pelo OAuth Security BCP e expor tokens na URL do browser. Resource Owner Password Credentials foi rejeitado por expor credenciais do usuario diretamente para a aplicacao cliente, violando o principio de delegacao OAuth. Client secret em SPAs foi rejeitado porque o secret ficaria exposto no codigo fonte acessivel pelo navegador, permitindo impersonacao da aplicacao.
