---
status: review
updated: 2026-01-21
---

# Authentication - Autenticação com Keycloak

## Visão Geral

O módulo de autenticação do @carf/tscore fornece integração com Keycloak OAuth2/OIDC para Single Sign-On (SSO) em todos os projetos CARF conforme. Implementa autenticação baseada em tokens JWT com suporte a roles, multi-tenancy e refresh automático, sendo consumido por geoapi-client para autenticação automática em requisições HTTP.

## Arquitetura de Autenticacao

O CARF utiliza autenticação federada via Keycloak com o seguinte fluxo:

```
┌─────────────┐ ┌──────────────┐ ┌─────────────┐ ┌──────────┐
│ Cliente │ │ Keycloak │ │ GEOAPI │ │ Database │
│ (GEOWEB/APP)│ │ (Auth) │ │ (Backend) │ │ (RLS) │
└──────┬──────┘ └──────┬───────┘ └──────┬──────┘ └────┬─────┘
 │ │ │ │
 │ 1. Login Request │ │ │
 ├───────────────────>│ │ │
 │ │ │ │
 │ 2. User Credentials │ │
 ├───────────────────>│ │ │
 │ │ │ │
 │ 3. JWT Token │ │ │
 │<───────────────────┤ │ │
 │ │ │ │
 │ 4. API Request (JWT in Bearer header) │ │
 ├──────────────────────────────────────────>│ │
 │ │ │ │
 │ │ 5. Validate Token │ │
 │ │<────────────────────┤ │
 │ │ │ │
 │ │ 6. Token Valid │ │
 │ ├────────────────────>│ │
 │ │ │ │
 │ │ │ 7. Query with RLS│
 │ │ ├──────────────────>│
 │ │ │ │
 │ 8. Response │ │ │
 │<───────────────────────────────────────────┤ │
```

### 1. Authorization Code Flow with PKCE

Aplicações frontend (SPA) usam **PKCE (Proof Key for Code Exchange)** para segurança adicional:

1. Cliente gera `code_verifier` aleatório
2. Cliente calcula `code_challenge = SHA256(code_verifier)`
3. Cliente redireciona para Keycloak com `code_challenge`
4. Usuário faz login no Keycloak
5. Keycloak redireciona de volta com `authorization_code`
6. Cliente troca `code` + `code_verifier` por `access_token`

### 2. JWT Token Structure

Token JWT contém claims customizados para multi-tenancy:

```json
{
 "sub": "550e8400-e29b-41d4-a716-446655440000",
 "email": "usuario@example.com",
 "name": "João da Silva",
 "preferred_username": "joao.silva",
 "realm_access": {
 "roles": ["analyst", "field-collector"]
 },
 "tenant_id": "tenant-sp-prefeitura",
 "allowed_tenants": ["tenant-sp-prefeitura", "tenant-rj-iterj"],
 "current_tenant": "tenant-sp-prefeitura",
 "exp": 1704931200,
 "iat": 1704844800
}
```

## Roles do Sistema

O CARF define 5 niveis de autorizacao (RBAC):

| Role | Descricao | Permissoes |
|:-----|:----------|:-----------|
| `super-admin` | Super administrador global | Acesso total, gerencia tenants |
| `admin` | Administrador do tenant | Gerencia usuarios e configuracoes |
| `manager` | Gestor de processos | Aprova legitimacoes, gera relatorios |
| `analyst` | Analista tecnico | Valida unidades, corrige geometrias |
| `field-collector` | Coletor de campo | Apenas coleta dados mobile |

## API do Modulo de Autenticacao

### KeycloakClient

Classe principal que gerencia autenticação com Keycloak.

```typescript
import { KeycloakClient } from '@carf/tscore/auth'

const client = new KeycloakClient({
 url: 'https://keycloak.carf.gov.br',
 realm: 'carf',
 clientId: 'geoweb-client'
})

// Inicializar autenticação
await client.init()

// Verificar se usuário está autenticado
if (client.isAuthenticated()) {
 const token = client.getToken()
 const user = client.getUser()
 const roles = client.getRoles()
}

// Fazer login
await client.login()

// Fazer logout
await client.logout()

// Refresh token automático
client.onTokenExpired(() => {
 client.refreshToken()
})
```

#### Configuração por Projeto

Cada projeto CARF tem configuração específica:

| Projeto | Client ID | Flow | Redirect URI | Docs |
|---------|-----------|------|--------------|------|
| GEOWEB | `geoweb-client` | PKCE | `http://localhost:3000/callback` | |
| REURBCAD | `reurbcad-mobile` | PKCE | `reurbcad://callback` | |
| ADMIN | `admin-console` | PKCE | `http://localhost:5173/callback` | |
| WEBDOCS | `webdocs` | PKCE | `http://localhost:5174/callback` | |
| GEOGIS | `geogis-plugin` | Client Credentials | N/A | |
| GEOAPI | `geoapi-backend` | Client Credentials | N/A | |

### React Hooks

#### useAuth()

Hook principal para acesso a dados de autenticação.

```typescript
import { useAuth } from '@carf/tscore/auth/react'

function UserProfile() {
 const {
 user, // Dados do usuário autenticado
 isAuthenticated, // Boolean: está autenticado?
 isLoading, // Boolean: carregando?
 token, // JWT access token
 roles, // Array de roles do usuário
 hasRole, // Função: verifica se tem role
 hasAnyRole, // Função: verifica se tem ao menos uma role
 hasAllRoles, // Função: verifica se tem todas as roles
 login, // Função: fazer login
 logout, // Função: fazer logout
 refreshToken, // Função: renovar token
 tenant, // Tenant atual do usuário
 switchTenant, // Função: trocar tenant
 } = useAuth()

 if (isLoading) return <Spinner />
 if (!isAuthenticated) return <LoginPage />

 return (
 <div>
 <h1>Olá, {user?.name}</h1>
 <p>Email: {user?.email}</p>
 <p>Tenant: {tenant?.name}</p>

 {hasRole('admin') && <AdminPanel />}
 {hasAnyRole(['analyst', 'manager']) && <AnalysisTools />}

 <button onClick={logout}>Sair</button>
 </div>
 )
}
```

#### ProtectedRoute

Componente para proteger rotas por role.

```typescript
import { ProtectedRoute } from '@carf/tscore/auth/react'
import { Role } from '@carf/tscore/types'

function App() {
 return (
 <Router>
 <Routes>
 {/* Rota pública */}
 <Route path="/login" element={<LoginPage />} />

 {/* Rota protegida - qualquer usuário autenticado */}
 <Route
 path="/dashboard"
 element={
 <ProtectedRoute>
 <Dashboard />
 </ProtectedRoute>
 }
 />

 {/* Rota protegida - requer role específica */}
 <Route
 path="/admin"
 element={
 <ProtectedRoute requiredRoles={[Role.ADMIN, Role.SUPER_ADMIN]}>
 <AdminPage />
 </ProtectedRoute>
 }
 />

 {/* Rota protegida - requer todas as roles */}
 <Route
 path="/advanced"
 element={
 <ProtectedRoute
 requiredRoles={[Role.ANALYST, Role.MANAGER]}
 requireAll={true}
 >
 <AdvancedPage />
 </ProtectedRoute>
 }
 />

 {/* Rota de fallback */}
 <Route path="/unauthorized" element={<UnauthorizedPage />} />
 </Routes>
 </Router>
 )
}
```

#### AuthProvider

Provider React Context para gerenciar estado de autenticação.

```typescript
import { AuthProvider } from '@carf/tscore/auth/react'
import { KeycloakClient } from '@carf/tscore/auth'

const keycloakClient = new KeycloakClient({
 url: import.meta.env.VITE_KEYCLOAK_URL,
 realm: 'carf',
 clientId: 'geoweb-client'
})

function App() {
 return (
 <AuthProvider
 client={keycloakClient}
 onTokenExpired={(client) => client.refreshToken()}
 onTokenRefreshError={(error) => console.error(error)}
 >
 <Router>
 {/* Suas rotas aqui */}
 </Router>
 </AuthProvider>
 )
}
```

### Vue 3 Composables

#### useAuth()

Composable para Vue 3 com reatividade.

```typescript
import { useAuth } from '@carf/tscore/auth/vue'
import { computed } from 'vue'

export default {
 setup() {
 const {
 user,
 isAuthenticated,
 isLoading,
 hasRole,
 login,
 logout
 } = useAuth()

 const canManage = computed(() =>
 hasRole('manager') || hasRole('admin')
 )

 return {
 user,
 isAuthenticated,
 isLoading,
 canManage,
 login,
 logout
 }
 }
}
```

#### initAuth()

Função para inicializar autenticação no Vue app.

```typescript
import { createApp } from 'vue'
import { initAuth } from '@carf/tscore/auth/vue'
import { KeycloakClient } from '@carf/tscore/auth'
import App from './App.vue'

const keycloakClient = new KeycloakClient({
 url: import.meta.env.VITE_KEYCLOAK_URL,
 realm: 'carf',
 clientId: 'webdocs'
})

const app = createApp(App)
initAuth(app, keycloakClient)
app.mount('#app')
```

## Multi-Tenancy

### Conceito

Multi-tenancy permite que múltiplas instituições (prefeituras, ITERJ, etc.) compartilhem a mesma infraestrutura CARF com isolamento completo de dados conforme arquitetura documentada em CENTRAL/ARCHITECTURE/MULTI-TENANCY usando entidade para representar cada instituição.

### Isolamento de Dados

O isolamento ocorre em 3 camadas:

1. **Keycloak:** User attributes `tenants: []` e `current_tenant`
2. **JWT Claims:** Token inclui `tenant_id` e `allowed_tenants`
3. **Database RLS:** PostgreSQL Row-Level Security filtra por tenant

```sql
-- Exemplo de RLS Policy
CREATE POLICY tenant_isolation ON units
 USING (tenant_id = current_setting('app.current_tenant_id')::uuid);
```

### Trocar Tenant

Usuários com acesso a múltiplos tenants podem alternar:

```typescript
import { useAuth } from '@carf/tscore/auth/react'

function TenantSwitcher() {
 const { tenant, allowedTenants, switchTenant } = useAuth()

 return (
 <select
 value={tenant?.id}
 onChange={(e) => switchTenant(e.target.value)}
 >
 {allowedTenants.map(t => (
 <option key={t.id} value={t.id}>{t.name}</option>
 ))}
 </select>
 )
}
```

### Backend API

```typescript
// POST /api/auth/switch-tenant
// Body: { tenantId: "tenant-sp-prefeitura" }
// Response: { token: "novo-jwt-com-tenant-atualizado" }
```

## Segurança

### Token Storage

- **Web (GEOWEB, ADMIN):** `httpOnly` cookie (protege contra XSS)
- **Mobile (REURBCAD):** Keychain/Keystore nativo (criptografado)

### Token Refresh

Tokens são renovados automaticamente antes de expirar:

```typescript
const client = new KeycloakClient({
 url: '...',
 realm: 'carf',
 clientId: 'geoweb-client',
 refreshTokenMinValidity: 300 // Renova 5min antes de expirar
})

// Refresh automático
client.onTokenExpired(async () => {
 try {
 await client.refreshToken()
 } catch (error) {
 // Token refresh falhou - redirecionar para login
 await client.login()
 }
})
```

### PKCE (Proof Key for Code Exchange)

Aplicações SPA usam PKCE para proteger o Authorization Code Flow:

```typescript
// Interno - KeycloakClient gerencia automaticamente
const codeVerifier = generateRandomString(128)
const codeChallenge = await sha256(codeVerifier)

// 1. Redireciona para Keycloak com code_challenge
window.location.href = `${keycloakUrl}/auth?code_challenge=${codeChallenge}`

// 2. Após redirect, troca code + code_verifier por token
const token = await exchangeCode(code, codeVerifier)
```

## Testes

### Mocking Autenticação

```typescript
import { KeycloakClient } from '@carf/tscore/auth'
import { vi } from 'vitest'

// Mock Keycloak client
vi.mock('@carf/tscore/auth', () => ({
 KeycloakClient: vi.fn().mockImplementation(() => ({
 init: vi.fn().mockResolvedValue(true),
 isAuthenticated: vi.fn().mockReturnValue(true),
 getToken: vi.fn().mockReturnValue('mock-jwt-token'),
 getUser: vi.fn().mockReturnValue({
 id: '123',
 name: 'Test User',
 email: 'test@example.com'
 }),
 getRoles: vi.fn().mockReturnValue(['analyst']),
 login: vi.fn(),
 logout: vi.fn()
 }))
}))
```

### Testando ProtectedRoute

```typescript
import { render, screen } from '@testing-library/react'
import { ProtectedRoute } from '@carf/tscore/auth/react'
import { AuthProvider } from '@carf/tscore/auth/react'

test('redirects to login if not authenticated', () => {
 const mockClient = createMockClient({ isAuthenticated: false })

 render(
 <AuthProvider client={mockClient}>
 <ProtectedRoute>
 <div>Protected Content</div>
 </ProtectedRoute>
 </AuthProvider>
 )

 expect(screen.queryByText('Protected Content')).not.toBeInTheDocument()
})
```
