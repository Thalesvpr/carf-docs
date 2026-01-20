---
status: review
updated: 2026-01-15
---

# INTEGRATION

Documentação de integrações com serviços externos essenciais para o funcionamento do sistema CARF.

O [Keycloak](./KEYCLOAK/README.md) é o provedor de autenticação centralizada OAuth2/OIDC, oferecendo Single Sign-On para todas as aplicações do ecossistema com suporte a multi-tenancy via atributos de usuário mapeados em claims JWT.

O [banco de dados](./DATABASE/README.md) usa PostgreSQL 16 com extensão PostGIS 3.4 para dados geoespaciais e Row-Level Security para isolamento automático de dados entre tenants.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (28 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Database](./DATABASE/README.md) | 2 |
|  | [Keycloak](./KEYCLOAK/README.md) | 26 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/INTEGRATION/DATABASE/README|DATABASE]]
- [[CENTRAL/INTEGRATION/KEYCLOAK/README|KEYCLOAK]]

<!-- CARF-INDEX-END -->
