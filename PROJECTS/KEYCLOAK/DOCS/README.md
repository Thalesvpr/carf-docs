---
status: review
updated: 2026-01-21
---

# KEYCLOAK - Documentacao Completa

Documentacao completa do Keycloak no ecossistema CARF, cobrindo desde conceitos teoricos ate procedimentos operacionais. Este e o ponto central para toda documentacao de autenticacao e autorizacao do sistema.

**Tecnologia de Temas**: O padrao CARF e **Keycloakify** (React/TypeScript), permitindo reutilizacao de componentes @carf/ui. Ver [CONCEPTS/01-keycloak-themes.md](./CONCEPTS/01-keycloak-themes.md) e [HOW-TO/01-develop-themes.md](./HOW-TO/01-develop-themes.md).

## Estrutura

### Conceitos e Arquitetura

| Pasta | Conteudo |
|:------|:---------|
| [ARCHITECTURE/](./ARCHITECTURE/README.md) | Estrategia de customizacao, temas e extensoes |
| [CONCEPTS/](./CONCEPTS/README.md) | Temas, SPIs, OAuth2, OIDC, multi-tenancy |

### Implementacao

| Pasta | Conteudo |
|:------|:---------|
| [INTEGRATION/](./INTEGRATION/README.md) | Clients, RBAC, Realm, Tokens, Security |
| [FEATURES/](./FEATURES/README.md) | Features CARF: validacao CPF, temas, multi-tenancy |
| [CONFIG/](./CONFIG/README.md) | docker-compose, realm-export, .env |

### Operacao

| Pasta | Conteudo |
|:------|:---------|
| [HOW-TO/](./HOW-TO/README.md) | Guias de desenvolvimento, deploy, producao |
| [RUNBOOKS/](./RUNBOOKS/README.md) | Criar usuarios, tenants, troubleshooting |
| [REFERENCE/](./REFERENCE/README.md) | Admin API, OIDC endpoints, theme properties |

## ADRs Relacionados

Decisoes arquiteturais que fundamentam a implementacao:

| ADR | Decisao |
|:----|:--------|
| [ADR-024](../../CENTRAL/ARCHITECTURE/ADRs/ADR-024-keycloakify-adoption.md) | Keycloakify para temas React |
| [ADR-025](../../CENTRAL/ARCHITECTURE/ADRs/ADR-025-single-realm-multi-tenancy.md) | Single-realm multi-tenancy |
| [ADR-026](../../CENTRAL/ARCHITECTURE/ADRs/ADR-026-roles-hierarchy.md) | Hierarquia de 5+1 roles |
| [ADR-027](../../CENTRAL/ARCHITECTURE/ADRs/ADR-027-oauth2-flows-by-client.md) | OAuth2 flows por tipo de client |
| [ADR-028](../../CENTRAL/ARCHITECTURE/ADRs/ADR-028-token-lifetimes.md) | Token lifetimes e session config |
| [ADR-029](../../CENTRAL/ARCHITECTURE/ADRs/ADR-029-security-strategy.md) | Estrategia de seguranca |

## Quick Start

```bash
# 1. Configurar ambiente
cp DOCS/CONFIG/.env.example DOCS/CONFIG/.env

# 2. Subir Keycloak local
cd DOCS/CONFIG && docker-compose up -d

# 3. Acessar Admin Console
open http://localhost:8080/admin
# Usuario: admin / Senha: ver .env
```

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/KEYCLOAK/DOCS/ARCHITECTURE/README|ARCHITECTURE]]
- [[PROJECTS/KEYCLOAK/DOCS/CONCEPTS/README|CONCEPTS]]
- [[PROJECTS/KEYCLOAK/DOCS/CONFIG/README|CONFIG]]
- [[PROJECTS/KEYCLOAK/DOCS/FEATURES/README|FEATURES]]
- [[PROJECTS/KEYCLOAK/DOCS/HOW-TO/README|HOW-TO]]
- [[PROJECTS/KEYCLOAK/DOCS/INTEGRATION/README|INTEGRATION]]
- [[PROJECTS/KEYCLOAK/DOCS/REFERENCE/README|REFERENCE]]
- [[PROJECTS/KEYCLOAK/DOCS/RUNBOOKS/README|RUNBOOKS]]

<!-- CARF-INDEX-END -->
