# ARCHITECTURE - GEOWEB

Arquitetura do portal web GEOWEB React + Vite.

## Integrações

- **[01-keycloak-integration.md](./01-keycloak-integration.md)** - Integração OAuth2/OIDC com Keycloak, useAuth hook, AuthProvider, protected routes
- **[02-tscore-integration.md](./02-tscore-integration.md)** - Uso da biblioteca @carf/tscore para value objects (CPF, Email), types compartilhados, auth hooks

## Decisões Arquiteturais

Ver também [CENTRAL/ARCHITECTURE/ADRs](../../../../CENTRAL/ARCHITECTURE/ADRs/README.md) para decisões cross-project:
- [ADR-012](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-012-vite-bundler-frontend.md) - Vite bundler
- [ADR-014](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-014-shadcn-ui-component-library.md) - shadcn/ui components
- [ADR-015](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-015-tanstack-query-server-state.md) - TanStack Query
- [ADR-019](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-019-zustand-client-state.md) - Zustand state management

---

**Última atualização:** 2026-01-10
