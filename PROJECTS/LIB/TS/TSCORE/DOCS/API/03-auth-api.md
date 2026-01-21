---
title: "Auth API - @carf/tscore"
status: review
updated: 2026-01-21
source: "CENTRAL/LIBRARIES/01-tscore.md"
---

# Auth API - @carf/tscore

Referencia completa da API de autenticacao com Keycloak.

## Modulos

| Modulo | Import | Uso |
|:-------|:-------|:----|
| Base | `@carf/tscore/auth` | Cliente Keycloak framework-agnostico |
| React | `@carf/tscore/auth/react` | Hooks e componentes React |
| Vue | `@carf/tscore/auth/vue` | Composables Vue 3 |

## @carf/tscore/auth

### KeycloakClient

Cliente principal de autenticacao.

```typescript
class KeycloakClient {
  constructor(config: KeycloakConfig)

  // Inicializacao
  async init(): Promise<void>

  // Login/Logout
  login(redirectUri?: string): void
  async handleCallback(code: string, state: string): Promise<void>
  async logout(redirectUri?: string): Promise<void>

  // Token
  async getToken(): Promise<string>
  async refreshToken(): Promise<string>

  // Usuario
  getUser(): User | null
  isAuthenticated(): boolean

  // Permissoes
  hasRole(role: Role): boolean
  hasRolePermission(requiredRole: Role): boolean
  getRoles(): Role[]
}
```

### KeycloakConfig

```typescript
interface KeycloakConfig {
  url: string        // URL do Keycloak (ex: https://keycloak.carf.gov.br)
  realm: string      // Realm (ex: carf)
  clientId: string   // Client ID (ex: geoweb-client, admin-client)
}
```

### User

```typescript
interface User {
  id: string
  username: string
  email?: string
  name?: string
  firstName?: string
  lastName?: string
  roles: Role[]
  tenantId?: string
  customClaims?: Record<string, unknown>
}
```

### AuthTokens

```typescript
interface AuthTokens {
  accessToken: string
  refreshToken: string
  idToken: string
  expiresAt: number  // Timestamp em milliseconds
}
```

### Exemplo de Uso

```typescript
import { KeycloakClient } from '@carf/tscore/auth'

const keycloak = new KeycloakClient({
  url: 'https://keycloak.carf.gov.br',
  realm: 'carf',
  clientId: 'geoweb-client'
})

// Inicializar (carrega tokens do localStorage)
await keycloak.init()

// Verificar autenticacao
if (!keycloak.isAuthenticated()) {
  // Redireciona para Keycloak
  keycloak.login()
}

// Obter token para requisicoes
const token = await keycloak.getToken()
// Token e renovado automaticamente se expirado

// Verificar permissao
if (keycloak.hasRole(Role.ADMIN)) {
  // Usuario e admin
}

// Logout
await keycloak.logout()
```

## @carf/tscore/auth/react

### AuthProvider

Context provider para autenticacao.

```typescript
interface AuthProviderProps {
  client: KeycloakClient
  children: React.ReactNode
  loadingComponent?: React.ReactNode
}

function AuthProvider(props: AuthProviderProps): JSX.Element
```

**Uso:**

```tsx
import { KeycloakClient } from '@carf/tscore/auth'
import { AuthProvider } from '@carf/tscore/auth/react'

const keycloak = new KeycloakClient({ /* config */ })

function App() {
  return (
    <AuthProvider client={keycloak}>
      <Router />
    </AuthProvider>
  )
}
```

### useAuth

Hook de estado de autenticacao.

```typescript
interface AuthContextValue {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: () => void
  logout: () => Promise<void>
  hasRole: (role: Role) => boolean
  hasPermission: (requiredRole: Role) => boolean
  getToken: () => Promise<string>
}

function useAuth(): AuthContextValue
```

**Uso:**

```tsx
import { useAuth } from '@carf/tscore/auth/react'

function UserMenu() {
  const { user, isAuthenticated, logout } = useAuth()

  if (!isAuthenticated) {
    return <LoginButton />
  }

  return (
    <div>
      <span>Ola, {user?.name}</span>
      <button onClick={logout}>Sair</button>
    </div>
  )
}
```

### useUser

Hook de dados do usuario.

```typescript
function useUser(): User | null
```

**Uso:**

```tsx
import { useUser } from '@carf/tscore/auth/react'

function Profile() {
  const user = useUser()

  if (!user) return null

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  )
}
```

### usePermissions

Hook de verificacao de roles.

```typescript
interface PermissionsHook {
  hasRole: (role: Role) => boolean
  hasPermission: (requiredRole: Role) => boolean
  roles: Role[]
  isAdmin: boolean
  isManager: boolean
}

function usePermissions(): PermissionsHook
```

**Uso:**

```tsx
import { usePermissions, Role } from '@carf/tscore/auth/react'

function AdminPanel() {
  const { hasRole, isAdmin } = usePermissions()

  if (!isAdmin) {
    return <AccessDenied />
  }

  return <AdminDashboard />
}
```

### useToken

Hook de acesso ao JWT.

```typescript
function useToken(): {
  getToken: () => Promise<string>
  isExpired: boolean
}
```

**Uso:**

```tsx
import { useToken } from '@carf/tscore/auth/react'

function ApiClient() {
  const { getToken } = useToken()

  async function fetchData() {
    const token = await getToken()
    const response = await fetch('/api/data', {
      headers: { Authorization: `Bearer ${token}` }
    })
  }
}
```

### ProtectedRoute

Componente de rota protegida.

```typescript
interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRoles?: Role[]
  fallback?: React.ReactNode
  redirectTo?: string
}

function ProtectedRoute(props: ProtectedRouteProps): JSX.Element
```

**Uso:**

```tsx
import { ProtectedRoute, Role } from '@carf/tscore/auth/react'

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      {/* Rota protegida - qualquer usuario autenticado */}
      <Route path="/dashboard" element={
        <ProtectedRoute>
          <Dashboard />
        </ProtectedRoute>
      } />

      {/* Rota protegida - apenas admin */}
      <Route path="/admin" element={
        <ProtectedRoute requiredRoles={[Role.ADMIN]}>
          <AdminPanel />
        </ProtectedRoute>
      } />

      {/* Com fallback customizado */}
      <Route path="/reports" element={
        <ProtectedRoute
          requiredRoles={[Role.MANAGER, Role.ADMIN]}
          fallback={<AccessDenied />}
        >
          <Reports />
        </ProtectedRoute>
      } />
    </Routes>
  )
}
```

## @carf/tscore/auth/vue

### initAuth

Plugin de inicializacao para Vue 3.

```typescript
function initAuth(app: App, client: KeycloakClient): void
```

**Uso:**

```typescript
import { createApp } from 'vue'
import { KeycloakClient } from '@carf/tscore/auth'
import { initAuth } from '@carf/tscore/auth/vue'

const keycloak = new KeycloakClient({ /* config */ })
const app = createApp(App)

initAuth(app, keycloak)
app.mount('#app')
```

### useAuth (Vue)

Composable de autenticacao.

```typescript
interface AuthComposable {
  user: Ref<User | null>
  isLoading: Ref<boolean>
  isAuthenticated: Ref<boolean>
  login: () => void
  logout: () => Promise<void>
  hasRole: (role: Role) => boolean
  hasPermission: (requiredRole: Role) => boolean
  getToken: () => Promise<string>
}

function useAuth(): AuthComposable
```

**Uso:**

```vue
<script setup lang="ts">
import { useAuth } from '@carf/tscore/auth/vue'

const { user, isAuthenticated, logout } = useAuth()
</script>

<template>
  <div v-if="isAuthenticated">
    <span>Ola, {{ user?.name }}</span>
    <button @click="logout">Sair</button>
  </div>
</template>
```

### useUser (Vue)

Composable de dados do usuario.

```typescript
function useUser(): Ref<User | null>
```

### usePermissions (Vue)

Composable de verificacao de roles.

```typescript
interface PermissionsComposable {
  hasRole: (role: Role) => boolean
  hasPermission: (requiredRole: Role) => boolean
  roles: Ref<Role[]>
  isAdmin: Ref<boolean>
  isManager: Ref<boolean>
}

function usePermissions(): PermissionsComposable
```
