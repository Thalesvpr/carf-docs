---
type: readme
status: rejected
description: "Usa tabelas e diagrama ASCII ao inves de prosa densa - reescrever em paragrafos"
updated: 2026-01-22
---

# INTEGRATION

Documentacao de integracao das aplicacoes CARF com o Keycloak, cobrindo configuracao de clients OAuth2, gerenciamento de roles e permissoes, configuracao do realm, estrutura de tokens JWT e praticas de seguranca.

## Estrutura

| Pasta | Conteudo |
|:------|:---------|
| [CLIENTS](./CLIENTS/README.md) | Configuracao dos 6 clients OAuth2 (GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS, ADMIN) |
| [RBAC](./RBAC/README.md) | Hierarquia de roles e mapeamento de permissoes |
| [REALM](./REALM/README.md) | Configuracao do realm CARF, protocol mappers e temas |
| [TOKENS](./TOKENS/README.md) | Estrutura de access/refresh tokens JWT e validacao |
| [SECURITY](./SECURITY/README.md) | Boas praticas, protecao contra ataques e secrets |

## Fluxo de Autenticacao

```
Usuario → GEOWEB/REURBCAD/WEBDOCS/ADMIN
           ↓
      Keycloak (PKCE)
           ↓
      Access Token JWT
           ↓
      GEOAPI (Bearer Validation)
           ↓
      PostgreSQL (RLS by tenant_id)
```

## Relacao com ADRs

Decisoes arquiteturais que fundamentam esta integracao:

- [ADR-025: Single-Realm Multi-Tenancy](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-025-single-realm-multi-tenancy.md) - Por que usamos realm unico
- [ADR-026: Hierarquia de Roles](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-026-roles-hierarchy.md) - Por que 5+1 roles
- [ADR-027: OAuth2 Flows](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-027-oauth2-flows-by-client.md) - Por que PKCE para SPAs
- [ADR-028: Token Lifetimes](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-028-token-lifetimes.md) - Por que 5min access token
- [ADR-029: Security Strategy](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-029-security-strategy.md) - Por que essas configuracoes

## Ver Tambem

- [CONCEPTS](../CONCEPTS/README.md) - Conceitos teoricos de Keycloak, OAuth2, OIDC
- [RUNBOOKS](../RUNBOOKS/README.md) - Procedimentos operacionais
- [CONFIG](../CONFIG/README.md) - Arquivos de configuracao

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/KEYCLOAK/DOCS/INTEGRATION/CLIENTS/README|CLIENTS]]
- [[PROJECTS/KEYCLOAK/DOCS/INTEGRATION/RBAC/README|RBAC]]
- [[PROJECTS/KEYCLOAK/DOCS/INTEGRATION/REALM/README|REALM]]
- [[PROJECTS/KEYCLOAK/DOCS/INTEGRATION/SECURITY/README|SECURITY]]
- [[PROJECTS/KEYCLOAK/DOCS/INTEGRATION/TOKENS/README|TOKENS]]

<!-- CARF-INDEX-END -->
