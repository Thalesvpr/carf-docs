# API Reference @carf/tscore

Documentação completa da API pública.

## Validations

### CPF

```typescript
class CPF {
  constructor(cpf: string)
  static validate(cpf: string): boolean
  static normalize(cpf: string): string
  format(): string
  toString(): string
  toJSON(): string
  equals(other: CPF): boolean
}
```

**Métodos:**

- `constructor(cpf: string)` - Cria CPF validado. Throw ValidationError se inválido
- `validate(cpf: string): boolean` - Valida CPF sem instanciar
- `normalize(cpf: string): string` - Remove pontuação, retorna 11 dígitos
- `format(): string` - Retorna formatado `###.###.###-##`
- `toString(): string` - Retorna normalizado (11 dígitos)
- `toJSON(): string` - Serialização JSON (11 dígitos)
- `equals(other: CPF): boolean` - Compara igualdade

**Exemplos:**
```typescript
const cpf = new CPF('123.456.789-09')
cpf.format()    // "123.456.789-09"
cpf.toString()  // "12345678909"

CPF.validate('123.456.789-09') // true
CPF.normalize('123.456.789-09') // "12345678909"
```

### CNPJ

```typescript
class CNPJ {
  constructor(cnpj: string)
  static validate(cnpj: string): boolean
  static normalize(cnpj: string): string
  format(): string
  toString(): string
  toJSON(): string
  equals(other: CNPJ): boolean
}
```

**Métodos:**

- `constructor(cnpj: string)` - Cria CNPJ validado. Throw ValidationError se inválido
- `validate(cnpj: string): boolean` - Valida CNPJ sem instanciar
- `normalize(cnpj: string): string` - Remove pontuação, retorna 14 dígitos
- `format(): string` - Retorna formatado `##.###.###/####-##`
- `toString(): string` - Retorna normalizado (14 dígitos)
- `toJSON(): string` - Serialização JSON (14 dígitos)
- `equals(other: CNPJ): boolean` - Compara igualdade

**Exemplos:**
```typescript
const cnpj = new CNPJ('11.444.777/0001-61')
cnpj.format()    // "11.444.777/0001-61"
cnpj.toString()  // "11444777000161"
```

### Email

```typescript
class Email {
  constructor(email: string)
  static validate(email: string): boolean
  static normalize(email: string): string
  toString(): string
  toJSON(): string
  equals(other: Email): boolean
}
```

**Métodos:**

- `constructor(email: string)` - Cria Email validado. Throw ValidationError se inválido
- `validate(email: string): boolean` - Valida email sem instanciar
- `normalize(email: string): string` - Lowercase e trim
- `toString(): string` - Retorna email normalizado
- `toJSON(): string` - Serialização JSON
- `equals(other: Email): boolean` - Compara igualdade

**Regras Validação:**
- Formato: `local@domain.tld`
- Local part: alfanuméricos + `._%+-`
- Domain: alfanuméricos + `.-`
- Requer TLD (pelo menos um `.` no domain)

**Exemplos:**
```typescript
const email = new Email('User@Example.COM')
email.toString() // "user@example.com"

Email.validate('user@example.com') // true
Email.validate('invalid@') // false
```

### Phone

```typescript
class Phone {
  constructor(phone: string)
  static validate(phone: string): boolean
  static normalize(phone: string): string
  format(): string
  toString(): string
  toJSON(): string
  equals(other: Phone): boolean
}
```

**Métodos:**

- `constructor(phone: string)` - Cria Phone validado. Throw ValidationError se inválido
- `validate(phone: string): boolean` - Valida telefone sem instanciar
- `normalize(phone: string): string` - Remove pontuação, retorna dígitos
- `format(): string` - Retorna formatado `(##) #####-####` ou `(##) ####-####`
- `toString(): string` - Retorna normalizado (10 ou 11 dígitos)
- `toJSON(): string` - Serialização JSON
- `equals(other: Phone): boolean` - Compara igualdade

**Regras Validação:**
- DDD: 11-99
- Celular: 9 dígitos começando com 9
- Fixo: 8 dígitos começando com 2-5
- Formatos aceitos: `(XX) XXXXX-XXXX`, `(XX) XXXX-XXXX`, `XX XXXXX-XXXX`, `XXXXXXXXXXX`

**Exemplos:**
```typescript
const phone = new Phone('11987654321')
phone.format() // "(11) 98765-4321"

Phone.validate('(11) 98765-4321') // true
Phone.validate('(11) 3456-7890')  // true (fixo)
```

## Types

### Entities

#### Unit

```typescript
interface Unit {
  id: string
  code: string
  status: UnitStatus
  street: string
  number?: string | null
  complement?: string | null
  neighborhood?: string | null
  city: string
  state: string
  zipCode?: string | null
  geometry?: GeoJSON.Polygon | null
  area?: number | null
  builtArea?: number | null
  communityId: string
  customData?: Record<string, any> | null
  createdAt: Date
  updatedAt: Date
  version: number
}
```

#### Holder

```typescript
interface Holder {
  id: string
  type: EntityType
  name: string
  cpf?: string | null
  cnpj?: string | null
  rg?: string | null
  birthDate?: Date | null
  nationality?: string | null
  maritalStatus?: string | null
  occupation?: string | null
  email?: string | null
  phone?: string | null
  street?: string | null
  number?: string | null
  complement?: string | null
  neighborhood?: string | null
  city?: string | null
  state?: string | null
  zipCode?: string | null
  customData?: Record<string, any> | null
  createdAt: Date
  updatedAt: Date
  version: number
}
```

#### Community

```typescript
interface Community {
  id: string
  name: string
  code?: string | null
  type: CommunityType
  description?: string | null
  boundary?: GeoJSON.Polygon | null
  area?: number | null
  tenantId: string
  isActive: boolean
  customData?: Record<string, any> | null
  createdAt: Date
  updatedAt: Date
  version: number
}
```

Ver todas 36+ entities em código-fonte `src/types/entities/`

### Enums

#### UnitStatus

```typescript
enum UnitStatus {
  DRAFT = 'DRAFT'
  PENDING = 'PENDING'
  IN_REVIEW = 'IN_REVIEW'
  APPROVED = 'APPROVED'
  REJECTED = 'REJECTED'
  REQUIRES_CHANGES = 'REQUIRES_CHANGES'
}
```

#### Role

```typescript
enum Role {
  SUPER_ADMIN = 'SUPER_ADMIN'
  ADMIN = 'ADMIN'
  MANAGER = 'MANAGER'
  ANALYST = 'ANALYST'
  FIELD_AGENT = 'FIELD_AGENT'
}

const RoleHierarchy: Record<Role, number>

function hasRolePermission(userRole: Role, requiredRole: Role): boolean
```

**Funções:**

- `hasRolePermission(userRole, requiredRole)` - Verifica se userRole >= requiredRole

**Exemplos:**
```typescript
hasRolePermission(Role.MANAGER, Role.ANALYST) // true
hasRolePermission(Role.ANALYST, Role.MANAGER) // false
```

#### LegitimationStatus

```typescript
enum LegitimationStatus {
  DRAFT = 'DRAFT'
  SUBMITTED = 'SUBMITTED'
  UNDER_REVIEW = 'UNDER_REVIEW'
  AWAITING_DOCUMENTATION = 'AWAITING_DOCUMENTATION'
  PUBLIC_NOTICE = 'PUBLIC_NOTICE'
  CONTESTED = 'CONTESTED'
  ANALYZING_CONTESTATION = 'ANALYZING_CONTESTATION'
  APPROVED = 'APPROVED'
  REJECTED = 'REJECTED'
  CERTIFICATE_ISSUED = 'CERTIFICATE_ISSUED'
  ARCHIVED = 'ARCHIVED'
}
```

#### EntityType

```typescript
enum EntityType {
  PESSOA_FISICA = 'PESSOA_FISICA'
  PESSOA_JURIDICA = 'PESSOA_JURIDICA'
  GOVERNMENT = 'GOVERNMENT'
  NGO = 'NGO'
  OTHER = 'OTHER'
}
```

#### CommunityType

```typescript
enum CommunityType {
  URBAN_SLUM = 'URBAN_SLUM'
  RURAL_SETTLEMENT = 'RURAL_SETTLEMENT'
  INDIGENOUS_LAND = 'INDIGENOUS_LAND'
  QUILOMBOLA = 'QUILOMBOLA'
  FISHING_COMMUNITY = 'FISHING_COMMUNITY'
  OTHER = 'OTHER'
}
```

### DTOs

#### CreateUnitDto

```typescript
interface CreateUnitDto {
  code: string
  street: string
  city: string
  state: string
  communityId: string
  number?: string
  complement?: string
  neighborhood?: string
  zipCode?: string
  geometry?: GeoJSON.Polygon
  area?: number
  builtArea?: number
  customData?: Record<string, any>
}
```

#### UpdateUnitDto

```typescript
interface UpdateUnitDto {
  code?: string
  status?: UnitStatus
  street?: string
  number?: string
  complement?: string
  neighborhood?: string
  city?: string
  state?: string
  zipCode?: string
  geometry?: GeoJSON.Polygon
  area?: number
  builtArea?: number
  customData?: Record<string, any>
}
```

## Auth

### KeycloakClient

```typescript
class KeycloakClient {
  constructor(config: KeycloakConfig)
  async init(): Promise<void>
  login(redirectUri?: string): void
  async handleCallback(code: string, state: string): Promise<void>
  async logout(redirectUri?: string): Promise<void>
  async getToken(): Promise<string>
  getUser(): User | null
  hasRole(role: Role): boolean
  hasRolePermission(requiredRole: Role): boolean
  isAuthenticated(): boolean
}
```

**Tipos:**

```typescript
interface KeycloakConfig {
  url: string        // http://localhost:8080
  realm: string      // carf
  clientId: string   // geoweb, admin, etc
}

interface User {
  id: string
  username: string
  email?: string
  name?: string
  roles: Role[]
  tenantId?: string
  customClaims?: Record<string, any>
}

interface AuthTokens {
  accessToken: string
  refreshToken: string
  idToken: string
  expiresAt: number
}
```

**Métodos:**

- `init()` - Carrega tokens de localStorage
- `login(redirectUri?)` - Redireciona para Keycloak (Authorization Code + PKCE)
- `handleCallback(code, state)` - Processa callback OAuth2
- `logout(redirectUri?)` - Limpa sessão e redireciona para logout Keycloak
- `getToken()` - Retorna access token (refresh automático se expirado)
- `getUser()` - Retorna user atual ou null
- `hasRole(role)` - Verifica se user tem role específica
- `hasRolePermission(requiredRole)` - Verifica se user tem permissão hierárquica
- `isAuthenticated()` - Verifica se user está autenticado

### React Hooks

#### useAuth

```typescript
function useAuth(): AuthContextValue

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
```

**Uso:**
```typescript
const { user, isAuthenticated, hasRole } = useAuth()
```

#### AuthProvider

```typescript
function AuthProvider(props: AuthProviderProps): JSX.Element

interface AuthProviderProps {
  client: KeycloakClient
  children: React.ReactNode
}
```

**Uso:**
```typescript
<AuthProvider client={keycloakClient}>
  <App />
</AuthProvider>
```

#### ProtectedRoute

```typescript
function ProtectedRoute(props: ProtectedRouteProps): JSX.Element

interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRoles?: Role[]
  fallback?: React.ReactNode
}
```

**Uso:**
```typescript
<ProtectedRoute requiredRoles={[Role.ADMIN]}>
  <AdminPanel />
</ProtectedRoute>
```

### Vue Composables

#### useAuth

```typescript
function useAuth(): AuthComposable

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
```

**Uso:**
```vue
<script setup>
const { user, isAuthenticated, hasRole } = useAuth()
</script>
```

#### initAuth

```typescript
function initAuth(app: App, client: KeycloakClient): void
```

**Uso:**
```typescript
import { createApp } from 'vue'
import { initAuth } from '@carf/tscore/auth/vue'

const app = createApp(App)
initAuth(app, keycloakClient)
app.mount('#app')
```

## Errors

### ValidationError

```typescript
class ValidationError extends Error {
  constructor(message: string)
}
```

Lançado por value objects quando validação falha.

**Exemplo:**
```typescript
try {
  new CPF('000.000.000-00')
} catch (error) {
  if (error instanceof ValidationError) {
    console.error(error.message) // "CPF inválido"
  }
}
```

---

**Última atualização:** 2026-01-09
