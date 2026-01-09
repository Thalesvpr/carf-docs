# Integração @carf/tscore no GEOWEB

Documentação de como GEOWEB utiliza @carf/tscore para autenticação, validações e types compartilhados.

## Instalação

@carf/tscore é instalado como dependência NPM via GitHub Packages:

```json
{
  "dependencies": {
    "@carf/tscore": "^0.1.0"
  }
}
```

**Atualização:**
```bash
bun update @carf/tscore
```

## Autenticação Keycloak

GEOWEB usa @carf/tscore/auth/react para integração Keycloak.

### Setup (src/main.tsx)

```typescript
import { AuthProvider } from '@carf/tscore/auth/react'
import { KeycloakClient } from '@carf/tscore/auth'
import App from './App'

const keycloakClient = new KeycloakClient({
  url: import.meta.env.VITE_KEYCLOAK_URL,
  realm: 'carf',
  clientId: 'geoweb'
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <AuthProvider client={keycloakClient}>
      <App />
    </AuthProvider>
  </React.StrictMode>
)
```

### Uso em Componentes

```typescript
import { useAuth } from '@carf/tscore/auth/react'
import { Role } from '@carf/tscore/types'

function NavBar() {
  const { user, hasRole, logout } = useAuth()

  return (
    <nav>
      <span>Olá, {user?.name}</span>
      {hasRole(Role.ADMIN) && (
        <Link to="/admin">Admin Panel</Link>
      )}
      <button onClick={logout}>Sair</button>
    </nav>
  )
}
```

### Rotas Protegidas

```typescript
import { ProtectedRoute } from '@carf/tscore/auth/react'
import { Role } from '@carf/tscore/types'

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      {/* Rota requer autenticação */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />

      {/* Rota requer role ADMIN */}
      <Route
        path="/admin"
        element={
          <ProtectedRoute requiredRoles={[Role.ADMIN, Role.SUPER_ADMIN]}>
            <AdminPanel />
          </ProtectedRoute>
        }
      />
    </Routes>
  )
}
```

## Validações

GEOWEB usa value objects @carf/tscore/validations em formulários.

### React Hook Form

```typescript
import { useForm } from 'react-hook-form'
import { CPF, CNPJ, Email, Phone } from '@carf/tscore/validations'

function HolderForm() {
  const { register, handleSubmit, formState: { errors } } = useForm()

  const onSubmit = async (data) => {
    try {
      const cpf = new CPF(data.cpf)
      const email = new Email(data.email)
      const phone = new Phone(data.phone)

      await api.createHolder({
        cpf: cpf.toString(),
        email: email.toString(),
        phone: phone.toString(),
        name: data.name
      })
    } catch (error) {
      console.error('Validation failed:', error)
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('cpf', {
          validate: (value) => CPF.validate(value) || 'CPF inválido'
        })}
        placeholder="CPF"
      />
      {errors.cpf && <span>{errors.cpf.message}</span>}

      <input
        {...register('email', {
          validate: (value) => Email.validate(value) || 'Email inválido'
        })}
        placeholder="Email"
      />
      {errors.email && <span>{errors.email.message}</span>}

      <button type="submit">Salvar</button>
    </form>
  )
}
```

### Zod Schema

```typescript
import { z } from 'zod'
import { CPF, Email, Phone } from '@carf/tscore/validations'
import { zodResolver } from '@hookform/resolvers/zod'

const holderSchema = z.object({
  name: z.string().min(1, 'Nome obrigatório'),
  cpf: z.string().refine(
    (val) => CPF.validate(val),
    { message: 'CPF inválido' }
  ),
  email: z.string().refine(
    (val) => Email.validate(val),
    { message: 'Email inválido' }
  ),
  phone: z.string().refine(
    (val) => Phone.validate(val),
    { message: 'Telefone inválido' }
  )
})

function HolderForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(holderSchema)
  })

  // ... rest of component
}
```

## Types TypeScript

GEOWEB importa types domain de @carf/tscore garantindo sincronia com backend.

### TanStack Query

```typescript
import type { Unit, Holder, Community } from '@carf/tscore/types'
import { UnitStatus } from '@carf/tscore/types'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

// Query units
function useUnits(communityId: string) {
  return useQuery({
    queryKey: ['units', communityId],
    queryFn: async (): Promise<Unit[]> => {
      const response = await fetch(`/api/units?communityId=${communityId}`)
      return response.json()
    }
  })
}

// Create unit mutation
function useCreateUnit() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (data: CreateUnitDto): Promise<Unit> => {
      const response = await fetch('/api/units', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      })
      return response.json()
    },
    onSuccess: (newUnit) => {
      queryClient.invalidateQueries({ queryKey: ['units', newUnit.communityId] })
    }
  })
}

// Uso em componente
function UnitsPage({ communityId }: { communityId: string }) {
  const { data: units, isLoading } = useUnits(communityId)
  const createMutation = useCreateUnit()

  if (isLoading) return <Loading />

  return (
    <div>
      {units?.map((unit) => (
        <UnitCard key={unit.id} unit={unit} />
      ))}
      <button onClick={() => createMutation.mutate({...})}>
        Nova Unidade
      </button>
    </div>
  )
}
```

### Type Guards

```typescript
import type { Unit, Holder } from '@carf/tscore/types'
import { EntityType, UnitStatus } from '@carf/tscore/types'

function isApprovedUnit(unit: Unit): boolean {
  return unit.status === UnitStatus.APPROVED
}

function isPessoaFisica(holder: Holder): holder is Holder & { cpf: string } {
  return holder.type === EntityType.PESSOA_FISICA && !!holder.cpf
}

// Uso
if (isPessoaFisica(holder)) {
  // TypeScript sabe que holder.cpf existe
  console.log('CPF:', holder.cpf)
}
```

## API Client

GEOWEB configura Axios interceptors usando @carf/tscore auth:

```typescript
// src/lib/api.ts
import axios from 'axios'
import { useAuth } from '@carf/tscore/auth/react'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
})

// Request interceptor - adiciona token
api.interceptors.request.use(async (config) => {
  const { getToken } = useAuth()
  const token = await getToken()

  config.headers.Authorization = `Bearer ${token}`
  return config
})

// Response interceptor - trata erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

## Formatação UI

Value objects facilitam formatação consistente:

```typescript
import { CPF, CNPJ, Phone } from '@carf/tscore/validations'

function HolderDetails({ holder }) {
  // holder.cpf vem do backend como string normalizada
  const cpf = holder.cpf ? new CPF(holder.cpf) : null
  const phone = holder.phone ? new Phone(holder.phone) : null

  return (
    <div>
      <p>Nome: {holder.name}</p>
      <p>CPF: {cpf?.format() ?? '-'}</p>
      <p>Telefone: {phone?.format() ?? '-'}</p>
    </div>
  )
}
```

## Benefícios

### Type Safety

TypeScript detecta erros em compile-time:

```typescript
import type { Unit } from '@carf/tscore/types'

const unit: Unit = {
  id: '123',
  code: 'UN-001',
  status: 'INVALID_STATUS', // ❌ Error: Type '"INVALID_STATUS"' is not assignable to type 'UnitStatus'
  // ...
}
```

### Validações Consistentes

Mesmas regras CPF/CNPJ em toda aplicação:

```typescript
// Formulário de cadastro
const cpf = new CPF(input) // Valida

// Listagem de titulares
const cpf = new CPF(holder.cpf) // Mesma validação

// Edição de titular
const cpf = new CPF(updatedData.cpf) // Mesma validação
```

### Redução de Bugs

Types sincronizados eliminam mismatches:

```typescript
// Backend adiciona campo novo `builtArea?: number`
// @carf/tscore atualiza Unit interface
// TypeScript alerta GEOWEB que type mudou
// Developer adiciona campo no UI
```

## Atualizações

Quando @carf/tscore atualiza:

### MINOR (backward-compatible)

```bash
# Atualizar automaticamente
bun update @carf/tscore

# Restart dev server
bun dev
```

### MAJOR (breaking changes)

1. Ler CHANGELOG: `node_modules/@carf/tscore/CHANGELOG.md`
2. Verificar migration guide
3. Atualizar código consumidor
4. Testar manualmente
5. Rodar CI/CD
6. Deploy

**Exemplo breaking change:**
```typescript
// v1.0.0 - CPF.validate() retorna boolean
if (CPF.validate(input)) { ... }

// v2.0.0 - CPF.validate() throw ValidationError
try {
  CPF.validate(input)
} catch (error) {
  // handle error
}
```

## Troubleshooting

### Types Desatualizados

**Sintoma:** Backend retorna campo que TypeScript não conhece

**Solução:**
```bash
# Atualizar @carf/tscore
bun update @carf/tscore

# Restart TypeScript server (VS Code)
Ctrl+Shift+P → "TypeScript: Restart TS Server"
```

### Validação Rejeitando Input Válido

**Sintoma:** CPF conhecido válido é rejeitado

**Solução:**
```typescript
// Debug passo a passo
const input = '123.456.789-09'
console.log('Normalized:', CPF.normalize(input))
console.log('Valid:', CPF.validate(input))

// Verificar se não é sequência conhecida
// 000.000.000-00 até 999.999.999-99 são rejeitados
```

### Bundle Size

@carf/tscore adiciona ~50KB ao bundle. Otimizações:

```typescript
// ❌ Importa tudo
import { CPF, CNPJ, Email, Phone, ... } from '@carf/tscore/validations'

// ✅ Import específico (tree-shaking)
import { CPF } from '@carf/tscore/validations'
```

---

**Última atualização:** 2026-01-09
