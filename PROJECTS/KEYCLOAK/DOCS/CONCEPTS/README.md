---
type: readme
status: review
updated: 2026-02-07
---

# CONCEPTS

Conceitos fundamentais do Keycloak e customizacoes CARF explicando a base teorica que fundamenta as decisoes de implementacao. Cobre desde temas visuais ate estrategia de multi-tenancy.

O doc [keycloak-themes](./01-keycloak-themes.md) explica Keycloakify como padrao CARF para temas React/TypeScript. O [keycloak-spis](./02-keycloak-spis.md) cobre extensoes Java como Authenticators e Event Listeners. A [realm-customization](./03-realm-customization.md) detalha configuracao de clients, roles com hierarquia em arvore e password policy length(8). O [oauth2-oidc-flows](./04-oauth2-oidc-flows.md) documenta grant types e endpoints OIDC. A [multi-tenancy-strategy](./05-multi-tenancy-strategy.md) explica isolamento via user attributes (current_tenant, tenants, community_ids) mapeados para JWT pelo scope carf-tenant e RLS no PostgreSQL.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (5)

| Documento | Status |
|-----------|--------|
| [Keycloak Themes](./01-keycloak-themes.md) | ⚠ |
| [02-keycloak-spis](./02-keycloak-spis.md) | ⚠ |
| [03-realm-customization](./03-realm-customization.md) | ⚠ |
| [04-oauth2-oidc-flows](./04-oauth2-oidc-flows.md) | ⚠ |
| [05-multi-tenancy-strategy](./05-multi-tenancy-strategy.md) | ⚠ |

<!-- CARF-INDEX-END -->
