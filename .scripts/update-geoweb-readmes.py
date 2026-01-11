#!/usr/bin/env python3
"""
Update GEOWEB documentation READMEs to link individual files
"""

from pathlib import Path

# ARCHITECTURE/README.md
arch_content = """# ARCHITECTURE - GEOWEB

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
"""

# CONCEPTS/README.md
concepts_content = """# CONCEPTS - GEOWEB

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

---

**Última atualização:** 2026-01-10
"""

# HOW-TO/README.md
howto_content = """# HOW-TO - GEOWEB

Guias práticos para desenvolvimento e configuração do GEOWEB.

## Autenticação

- **[01-setup-keycloak.md](./01-setup-keycloak.md)** - Configurar Keycloak client, redirect URIs, CORS origins, roles
- **[02-login-logout.md](./02-login-logout.md)** - Implementar login/logout buttons, useAuth hook, AuthProvider setup
- **[03-refresh-tokens.md](./03-refresh-tokens.md)** - Token refresh automático, interceptor de 401, retry failed requests

## Desenvolvimento Local

**Setup inicial:**
1. Clone do repositório
2. `npm install` ou `bun install`
3. Configurar `.env.local` com VITE_KEYCLOAK_URL e VITE_GEOAPI_URL
4. `npm run dev` para servidor de desenvolvimento

**Build para produção:**
1. `npm run build`
2. Testa build com `npm run preview`
3. Deploy para Vercel via `vercel deploy`

---

**Última atualização:** 2026-01-10
"""

# LAYERS/README.md
layers_content = """# LAYERS - GEOWEB

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
"""

def main():
    print("Updating GEOWEB documentation READMEs...")

    updates = [
        ('PROJECTS/GEOWEB/DOCS/ARCHITECTURE/README.md', arch_content),
        ('PROJECTS/GEOWEB/DOCS/CONCEPTS/README.md', concepts_content),
        ('PROJECTS/GEOWEB/DOCS/HOW-TO/README.md', howto_content),
        ('PROJECTS/GEOWEB/DOCS/LAYERS/README.md', layers_content),
    ]

    for file_path, content in updates:
        path = Path(file_path)
        path.write_text(content, encoding='utf-8')
        print(f"  [OK] {file_path}")

    print(f"\nTotal: {len(updates)} files updated")

if __name__ == '__main__':
    main()
