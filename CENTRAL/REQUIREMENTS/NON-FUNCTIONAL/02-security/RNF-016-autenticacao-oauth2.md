---
id: RNF-016
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-016: Autenticacao OAuth2

## Descricao

Toda autenticacao no sistema GEOMAP5 deve utilizar OAuth2 via Keycloak. Mecanismo padronizado e centralizado para controle de acesso aos modulos GEOAPI, GEOWEB, REURBCAD e GEOGIS.

## Metricas

- Protocolo: OAuth2 conforme RFC 6749
- Servidor de identidade: Keycloak
- Algoritmo de assinatura JWT: RS256

## Criterios de Aceitacao

1. GEOWEB e REURBCAD implementam Authorization Code com PKCE (RFC 7636)
2. GEOGIS implementa Client Credentials para integracao maquina-a-maquina
3. Todos os tokens JWT assinados com RS256
