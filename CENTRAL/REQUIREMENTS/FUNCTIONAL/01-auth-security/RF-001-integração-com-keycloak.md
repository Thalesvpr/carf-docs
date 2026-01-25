---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
  - GEOWEB
  - REURBCAD
  - GEOGIS
---

# RF-001: Integracao com Keycloak

## Descricao

O sistema deve integrar-se com Keycloak como identity provider centralizado implementando OAuth2 e OpenID Connect. Cada tenant possui realm ou configuracao isolada garantindo seguranca multi-tenant. A integracao suporta SSO permitindo que usuario autenticado em um modulo acesse outros sem re-autenticacao. Configuracao inclui client IDs, secrets, redirect URIs e escopos apropriados para cada aplicacao.

## Criterios de Aceitacao

1. Login via Keycloak funciona em GEOWEB, REURBCAD e GEOGIS
2. SSO permite navegacao entre modulos sem re-autenticacao
3. Configuracao de realm e clients documentada por ambiente
4. Tokens JWT incluem claims de tenant_id e roles
5. Logout em um modulo invalida sessao em todos

## Rastreabilidade

- Modulos: GEOAPI, GEOWEB, REURBCAD, GEOGIS
- Requisitos dependentes: RF-002, RF-003, RF-005
