# Conceitos - ADMIN

## Documentos Disponíveis

- [01-key-concepts.md](./01-key-concepts.md) - SPA, TanStack Query, RBAC, proxy seguro
- [02-terminology.md](./02-terminology.md) - Glossário React/TanStack Query
- [03-design-principles.md](./03-design-principles.md) - Security-first, least privilege

## Conceitos Fundamentais

ADMIN aplica **React SPA** para máxima segurança mantendo secrets no backend, **TanStack Query** para server state management com cache automático, **RBAC** com roles ADMIN/SUPER_ADMIN validadas no backend, e **Proxy Seguro** onde GEOAPI faz intermediação com Keycloak Admin API mantendo client_secret confidencial.
