---
type: readme
status: review
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
updated: 2026-01-22
---

# LAYERS - REURBWEB

Estrutura de camadas do código React do REURBWEB.

## Camadas da Aplicação

### Auth Context

- **[01-auth-context.md](./01-auth-context.md)** - AuthContext, AuthProvider, useAuth hook, token storage, refresh logic

**Responsabilidades:**
- Gerenciar estado de autenticação (user, isLoading, isAuthenticated)
- Prover métodos login(), logout(), getToken()
- Refresh automático de tokens antes de expirar
- hasRole() e hasPermission() helpers

### API Layer

**@carf/geoapi-client:**
- HTTP client com interceptors
- Request/response transformations
- Error handling centralizado
- Retry logic para network failures

### UI Components

**shadcn/ui + custom components:**
- Layout components (Navbar, Sidebar, Footer)
- Form components (Input, Select, DatePicker)
- Domain components (UnitCard, HolderCard, MapView)
- Shared utilities (@carf/ui library)

### State Management

**TanStack Query:**
- useQuery para fetch data
- useMutation para create/update/delete
- Cache invalidation strategies
- Optimistic updates

**Zustand:**
- Auth store
- Tenant context store
- UI preferences

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (1)

| Documento | Status |
|-----------|--------|
| [01-auth-context](./01-auth-context.md) | ⚠ |

<!-- CARF-INDEX-END -->
