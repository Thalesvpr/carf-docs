---
type: rf
status: review
updated: 2026-02-07
modules:
  - GEOAPI
  - GEOWEB
  - REURBCAD
  - GEOGIS
---

# RF-001: Integracao com Keycloak

## Descricao

O sistema deve integrar-se com Keycloak como identity provider centralizado implementando OAuth2 e OpenID Connect. Multi-tenancy opera em single realm CARF com isolamento via atributos de usuario (tenants, current_tenant) mapeados como claims no JWT, combinado com Row Level Security no PostgreSQL para isolamento de dados por tenant. A integracao suporta SSO permitindo que usuario autenticado em um modulo acesse outros sem re-autenticacao. Configuracao inclui client IDs, secrets (apenas geogis confidential), redirect URIs e escopos apropriados para cada aplicacao.

## Criterios de Aceitacao

1. Login via Keycloak funciona em GEOWEB, REURBCAD e GEOGIS
2. SSO permite navegacao entre modulos sem re-autenticacao
3. Configuracao de realm e clients documentada por ambiente
4. Tokens JWT incluem claims de tenant_id e roles
5. Logout em um modulo invalida sessao em todos

## Rastreabilidade

- Modulos: GEOAPI, GEOWEB, REURBCAD, GEOGIS
- Requisitos dependentes: RF-002, RF-003, RF-005
