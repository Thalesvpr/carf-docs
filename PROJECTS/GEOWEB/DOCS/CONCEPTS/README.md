---
type: readme
status: review
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
updated: 2026-01-22
---

# CONCEPTS - GEOWEB

Conceitos fundamentais do portal GEOWEB React.

## Autenticação e Autorização

- **[01-authentication.md](./01-authentication.md)** - OAuth2/OIDC flow, useAuth hook, token management, refresh logic
- **[02-protected-routes.md](./02-protected-routes.md)** - ProtectedRoute component, role-based routing, unauthorized redirects
- **[03-tenant-switcher.md](./03-tenant-switcher.md)** - Switch entre tenants permitidos, atualização de contexto, re-fetch de dados

## Padrões React

**Component Architecture** - Composição de componentes reutilizáveis, separação de UI e lógica, custom hooks

**State Management:**
- **Server State** - TanStack Query para cache de dados da API, invalidation, refetch
- **Client State** - Zustand para auth state, tenant context, UI preferences

**Form Handling** - React Hook Form + Zod validation, field-level errors, submit optimistic updates

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (3)

| Documento | Status |
|-----------|--------|
| [01-authentication](./01-authentication.md) | ⚠ |
| [02-protected-routes](./02-protected-routes.md) | ⚠ |
| [03-tenant-switcher](./03-tenant-switcher.md) | ⚠ |

<!-- CARF-INDEX-END -->
