# Layers - ADMIN

## Camadas

ADMIN SPA tem 5 layers: **(1) Presentation Layer** - React components em `src/pages/` e `src/components/` renderizando UI com shadcn/ui, **(2) State Management Layer** - TanStack Query gerenciando server state (cache, refetch, mutations) e Zustand gerenciando client state (UI flags, modals, selected items), **(3) API Client Layer** - `@carf/geoapi-client` fazendo requests HTTP para GEOAPI `/api/admin/*` com JWT injection automático via interceptor, **(4) Routing Layer** - React Router v6 com protected routes validando role antes de renderizar páginas admin, **(5) Auth Layer** - `@carf/tscore` KeycloakClient gerenciando login, logout, token refresh com PKCE flow sem client_secret no frontend.

## Diagrama

```
┌─────────────────────────────────────┐
│     Presentation Layer (React)      │
│  - UserManagementPage.tsx           │
│  - TenantManagementPage.tsx         │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│    State Management Layer           │
│  - TanStack Query (server state)    │
│  - Zustand (client state)           │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│       API Client Layer              │
│  - @carf/geoapi-client              │
│  - Interceptors (auth, retry)       │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│         Routing Layer               │
│  - React Router v6                  │
│  - Protected routes                 │
└──────────┬──────────────────────────┘
           │
┌──────────▼──────────────────────────┐
│          Auth Layer                 │
│  - @carf/tscore KeycloakClient      │
│  - PKCE flow (no secret)            │
└─────────────────────────────────────┘
```

