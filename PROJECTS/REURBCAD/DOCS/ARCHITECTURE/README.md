---
type: readme
status: review
description: "README usa listas/tabelas ao inves de prosa densa com links inline."
updated: 2026-02-08
---

# ARCHITECTURE - REURBCAD

Arquitetura do aplicativo mobile REURBCAD React Native + Expo.

## Integracao e Configuracao

- **[01-keycloak-integration.md](./01-keycloak-integration.md)** - OAuth2/OIDC em React Native, deep linking, PKCE flow, token storage seguro
- **[02-lib-integration.md](./02-lib-integration.md)** - Integracao com @carf/tscore, @carf/geoapi-client, @carf/ui-native

## Estrutura e Padroes

- **[03-navigation-structure.md](./03-navigation-structure.md)** - Expo Router file-based navigation, tabs, stacks, deep linking
- **[04-state-management.md](./04-state-management.md)** - Zustand + TanStack Query, persistencia, offline state
- **[05-error-handling.md](./05-error-handling.md)** - Error boundaries, retry logic, error reporting (Sentry)
- **[06-project-structure.md](./06-project-structure.md)** - Organizacao de diretorios, convencoes de nomenclatura

**Mobile-specific challenges:**
- Deep linking para callback OAuth
- Secure storage via expo-secure-store
- Offline token refresh
- Biometric authentication

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisao

- ○ [[PROJECTS/REURBCAD/DOCS/ARCHITECTURE/01-keycloak-integration.md|01-keycloak-integration]]
- ○ [[PROJECTS/REURBCAD/DOCS/ARCHITECTURE/02-lib-integration.md|02-lib-integration]]

### Planejados

- ○ [[PROJECTS/REURBCAD/DOCS/ARCHITECTURE/03-navigation-structure.md|03-navigation-structure]]
- ○ [[PROJECTS/REURBCAD/DOCS/ARCHITECTURE/04-state-management.md|04-state-management]]
- ○ [[PROJECTS/REURBCAD/DOCS/ARCHITECTURE/05-error-handling.md|05-error-handling]]
- ○ [[PROJECTS/REURBCAD/DOCS/ARCHITECTURE/06-project-structure.md|06-project-structure]]

<!-- CARF-INDEX-END -->
