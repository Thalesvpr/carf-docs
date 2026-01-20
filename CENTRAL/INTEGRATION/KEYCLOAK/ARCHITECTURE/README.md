---
status: review
updated: 2026-01-17
---

# ARCHITECTURE

Arquitetura de autenticação e autorização do Keycloak no ecossistema CARF, cobrindo padrões OAuth2/OIDC, fluxos de autenticação e estratégia de multi-tenancy.

A [visão geral](./01-overview.md) apresenta o Keycloak como provedor centralizado de identidade para as seis aplicações do sistema com Single Sign-On unificado. Os [fluxos OAuth2/OIDC](./02-oauth2-oidc.md) detalham Authorization Code com PKCE para SPAs e mobile, Client Credentials para server-to-server, e Bearer Token validation no backend. A estratégia de [multi-tenancy](./03-multi-tenancy.md) explica como um único realm suporta múltiplos municípios usando atributos de usuário e Row Level Security no PostgreSQL.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-overview](./01-overview.md) | Visão Geral da Arquitetura |
| [02-oauth2-oidc](./02-oauth2-oidc.md) | Fluxos OAuth2 e OpenID Connect |
| [03-multi-tenancy](./03-multi-tenancy.md) | Multi-Tenancy Dinâmico |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/INTEGRATION/KEYCLOAK/ARCHITECTURE/01-overview.md|Visão Geral da Arquitetura]]
- ○ [[CENTRAL/INTEGRATION/KEYCLOAK/ARCHITECTURE/02-oauth2-oidc.md|Fluxos OAuth2 e OpenID Connect]]
- ○ [[CENTRAL/INTEGRATION/KEYCLOAK/ARCHITECTURE/03-multi-tenancy.md|Multi-Tenancy Dinâmico]]

<!-- CARF-INDEX-END -->
