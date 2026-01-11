# LAYERS - GEOWEB

Estrutura de camadas do código React do GEOWEB.

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

---

**Última atualização:** 2026-01-10
