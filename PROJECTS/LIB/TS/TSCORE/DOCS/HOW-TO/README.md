# How-To @carf/tscore

Guias práticos para usar @carf/tscore em cada projeto.

## Guias por Projeto

### GEOWEB (Frontend React)

#### Instalar e Configurar

```bash
cd PROJECTS/GEOWEB/SRC-CODE

# Configurar .npmrc
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/tscore
```

#### Setup Autenticação

```typescript
// src/main.tsx
import { AuthProvider } from '@carf/tscore/auth/react'
import { KeycloakClient } from '@carf/tscore/auth'

const keycloakClient = new KeycloakClient({
 url: import.meta.env.VITE_KEYCLOAK_URL,
 realm: 'carf',
 clientId: 'geoweb'
})

ReactDOM.createRoot(document.getElementById('root')!).render(
 <AuthProvider client={keycloakClient}>
 <App />
 </AuthProvider>
)
```

#### Usar Validações em Forms

```typescript
import { useForm } from 'react-hook-form'
import { CPF, CNPJ } from '@carf/tscore/validations'

function HolderForm() {
 const { register, handleSubmit, formState: { errors } } = useForm()

 const onSubmit = (data) => {
 try {
 const cpf = new CPF(data.cpf)
 // CPF válido, prosseguir
 } catch (error) {
 alert('CPF inválido')
 }
 }

 return (
 <form onSubmit={handleSubmit(onSubmit)}>
 <input
 {...register('cpf', {
 validate: (value) => CPF.validate(value) || 'CPF inválido'
 })}
 />
 {errors.cpf && <span>{errors.cpf.message}</span>}
 </form>
 )
}
```

#### Usar Types com TanStack Query

```typescript
import type { Unit } from '@carf/tscore/types'
import { useQuery } from '@tanstack/react-query'

function useUnits(communityId: string) {
 return useQuery({
 queryKey: ['units', communityId],
 queryFn: async (): Promise<Unit[]> => {
 const response = await fetch(`/api/units?communityId=${communityId}`)
 return response.json()
 }
 })
}
```

### REURBCAD (Mobile React Native)

#### Instalar e Configurar

```bash
cd PROJECTS/REURBCAD/SRC-CODE

# Configurar .npmrc
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/tscore
```

#### Validações Offline

```typescript
import { CPF, CNPJ, Email, Phone } from '@carf/tscore/validations'
import { Unit, Holder } from '@carf/tscore/types'
import { database } from './database' // WatermelonDB

async function createHolderOffline(data) {
 // Validar antes de salvar offline
 const cpf = new CPF(data.cpf) // Throw se inválido
 const phone = new Phone(data.phone)

 await database.write(async () => {
 await database.get('holders').create((holder) => {
 holder.cpf = cpf.toString()
 holder.phone = phone.toString()
 holder.name = data.name
 })
 })
}
```

#### Tipos com WatermelonDB

```typescript
import { Model } from '@nozbe/watermelondb'
import type { Unit } from '@carf/tscore/types'
import { UnitStatus } from '@carf/tscore/types'

export class UnitModel extends Model {
 static table = 'units'

 @field('code') code!: string
 @field('status') status!: UnitStatus
 @field('area') area!: number

 // Converter para type @carf/tscore
 toType(): Unit {
 return {
 id: this.id,
 code: this.code,
 status: this.status,
 // ... outros campos
 }
 }
}
```

### ADMIN (Console Next.js)

#### Instalar e Configurar

```bash
cd PROJECTS/ADMIN/SRC-CODE

# Configurar .npmrc
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/tscore
```

#### Setup Autenticação Next.js

```typescript
// app/providers.tsx
'use client'

import { AuthProvider } from '@carf/tscore/auth/react'
import { KeycloakClient } from '@carf/tscore/auth'

const keycloakClient = new KeycloakClient({
 url: process.env.NEXT_PUBLIC_KEYCLOAK_URL!,
 realm: 'carf',
 clientId: 'admin'
})

export function Providers({ children }: { children: React.ReactNode }) {
 return <AuthProvider client={keycloakClient}>{children}</AuthProvider>
}

// app/layout.tsx
import { Providers } from './providers'

export default function RootLayout({ children }) {
 return (
 <html>
 <body>
 <Providers>{children}</Providers>
 </body>
 </html>
 )
}
```

#### Protected Server Actions

```typescript
// app/actions/users.ts
'use server'

import { KeycloakClient } from '@carf/tscore/auth'
import { Role } from '@carf/tscore/types'
import { cookies } from 'next/headers'

export async function deleteUser(userId: string) {
 const token = cookies().get('access_token')?.value
 if (!token) throw new Error('Unauthorized')

 // Validar role no backend
 const keycloak = new KeycloakClient({...})
 const user = await keycloak.getUser()
 if (!user || !user.roles.includes(Role.ADMIN)) {
 throw new Error('Forbidden')
 }

 // Prosseguir com deleção
 await fetch(`/api/users/${userId}`, {
 method: 'DELETE',
 headers: { Authorization: `Bearer ${token}` }
 })
}
```

### WEBDOCS (Portal VitePress)

#### Instalar e Configurar

```bash
cd PROJECTS/WEBDOCS/SRC-CODE

# Configurar .npmrc
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/tscore
```

#### Setup Autenticação Vue 3

```typescript
// .vitepress/theme/index.ts
import DefaultTheme from 'vitepress/theme'
import { initAuth } from '@carf/tscore/auth/vue'
import { KeycloakClient } from '@carf/tscore/auth'

const keycloakClient = new KeycloakClient({
 url: import.meta.env.VITE_KEYCLOAK_URL,
 realm: 'carf',
 clientId: 'webdocs'
})

export default {
 extends: DefaultTheme,
 enhanceApp({ app }) {
 initAuth(app, keycloakClient)
 }
}
```

#### Componente Vue com Validações

```vue
<script setup lang="ts">
import { ref } from 'vue'
import { CPF, Email } from '@carf/tscore/validations'

const cpfInput = ref('')
const cpfError = ref<string | null>(null)

function validateCPF() {
 try {
 new CPF(cpfInput.value)
 cpfError.value = null
 } catch (error) {
 cpfError.value = 'CPF inválido'
 }
}
</script>

<template>
 <div>
 <input v-model="cpfInput" @blur="validateCPF" placeholder="CPF" />
 <span v-if="cpfError" class="error">{{ cpfError }}</span>
 </div>
</template>
```

## Recipes Comuns

### Validar Múltiplos Campos

```typescript
import { CPF, Email, Phone } from '@carf/tscore/validations'

function validateHolder(data: any) {
 const errors: Record<string, string> = {}

 try {
 new CPF(data.cpf)
 } catch {
 errors.cpf = 'CPF inválido'
 }

 try {
 new Email(data.email)
 } catch {
 errors.email = 'Email inválido'
 }

 try {
 new Phone(data.phone)
 } catch {
 errors.phone = 'Telefone inválido'
 }

 return Object.keys(errors).length > 0 ? errors : null
}
```

### Integrar com Zod

```typescript
import { z } from 'zod'
import { CPF, CNPJ, Email } from '@carf/tscore/validations'

const holderSchema = z.object({
 name: z.string().min(1),
 cpf: z.string().refine(
 (val) => CPF.validate(val),
 { message: 'CPF inválido' }
 ),
 email: z.string().refine(
 (val) => Email.validate(val),
 { message: 'Email inválido' }
 )
})

// Usar com React Hook Form
const { register, handleSubmit } = useForm({
 resolver: zodResolver(holderSchema)
})
```

### Type Guards

```typescript
import type { Unit, Holder } from '@carf/tscore/types'
import { EntityType } from '@carf/tscore/types'

function isUnit(entity: unknown): entity is Unit {
 return typeof entity === 'object' && entity !== null && 'code' in entity
}

function isPessoaFisica(holder: Holder): holder is Holder & { cpf: string } {
 return holder.type === EntityType.PESSOA_FISICA && !!holder.cpf
}
```

### Converter Types Backend → Frontend

```typescript
import type { Unit } from '@carf/tscore/types'

// Backend retorna dates como strings ISO
interface UnitDTO {
 id: string
 code: string
 createdAt: string // ISO string
 updatedAt: string // ISO string
}

function mapUnitDtoToUnit(dto: UnitDTO): Unit {
 return {
 ...dto,
 createdAt: new Date(dto.createdAt),
 updatedAt: new Date(dto.updatedAt)
 }
}
```

## Troubleshooting

### Erro: "Cannot find module '@carf/tscore'"

**Causa:** .npmrc não configurado ou GITHUB_TOKEN inválido

**Solução:**
```bash
# Verificar .npmrc
cat .npmrc

# Deve conter:
@carf:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}

# Configurar token
export GITHUB_TOKEN=ghp_...
bun install
```

### Erro: "CPF inválido" em CPF conhecido válido

**Causa:** Formato incorreto ou dígitos verificadores errados

**Solução:**
```typescript
// Testar passo a passo
const cpf = '123.456.789-09'
console.log(CPF.normalize(cpf)) // "12345678909"
console.log(CPF.validate(cpf)) // true ou false

// Gerar CPF válido para teste: https://www.4devs.com.br/gerador_de_cpf
```

### Erro: "User is not authenticated" após login

**Causa:** Tokens não persistindo ou callback não processado

**Solução:**
```typescript
// Verificar localStorage
console.log(localStorage.getItem('auth_tokens'))

// Verificar init foi chamado
await keycloakClient.init()
console.log(keycloakClient.isAuthenticated())

// Verificar callback URL está registrada no Keycloak
// Valid Redirect URIs: http://localhost:3000/auth/callback
```

### Types Desatualizados

**Causa:** Backend alterou model mas @carf/tscore não atualizado

**Solução:**
```bash
# Verificar versão instalada
bun pm ls @carf/tscore

# Atualizar para latest
bun update @carf/tscore

# Ver CHANGELOG
cat node_modules/@carf/tscore/CHANGELOG.md
```

---

**Última atualização:** 2026-01-09
