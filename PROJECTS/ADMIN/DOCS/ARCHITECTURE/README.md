# Arquitetura ADMIN

Documentação arquitetural do console administrativo.

## Stack

- **Next.js 14** - App Router, React Server Components, Server Actions
- **@carf/tscore** - Auth, validations, types compartilhados
- **shadcn/ui** - Component library baseado em Radix UI
- **TanStack Query** - Client-side data fetching
- **Tailwind CSS** - Utility-first CSS framework
- **Bun** - Runtime e package manager

## App Router

Next.js 14 App Router com Server e Client Components:

```
app/
├── layout.tsx            # Root layout com AuthProvider
├── page.tsx              # Dashboard principal
├── tenants/
│   ├── page.tsx          # Lista tenants (RSC)
│   ├── [id]/
│   │   ├── page.tsx      # Detalhes tenant (RSC)
│   │   └── edit/
│   │       └── page.tsx  # Editar tenant (Client)
│   └── new/
│       └── page.tsx      # Criar tenant (Client)
├── users/
│   ├── page.tsx          # Lista usuários
│   └── [id]/
│       └── page.tsx      # Detalhes usuário
└── api/
    └── [...]/            # API routes (raramente usado)
```

## Server Components

Usar RSC para data fetching inicial:

```typescript
// app/tenants/page.tsx (Server Component)
import type { Tenant } from '@carf/tscore/types'

async function getTenants(): Promise<Tenant[]> {
  const response = await fetch('http://api/tenants', { cache: 'no-store' })
  return response.json()
}

export default async function TenantsPage() {
  const tenants = await getTenants()

  return (
    <div>
      {tenants.map((tenant) => (
        <TenantCard key={tenant.id} tenant={tenant} />
      ))}
    </div>
  )
}
```

## Client Components

Usar Client Components para interatividade:

```typescript
// app/tenants/new/page.tsx
'use client'

import { useForm } from 'react-hook-form'
import { Email } from '@carf/tscore/validations'
import type { CreateTenantDto } from '@carf/tscore/types'

export default function NewTenantPage() {
  const { register, handleSubmit } = useForm<CreateTenantDto>()

  const onSubmit = async (data: CreateTenantDto) => {
    await fetch('/api/tenants', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* form fields */}
    </form>
  )
}
```

## Server Actions

Server Actions para mutations:

```typescript
// app/actions/tenants.ts
'use server'

import type { CreateTenantDto } from '@carf/tscore/types'
import { revalidatePath } from 'next/cache'

export async function createTenant(data: CreateTenantDto) {
  const response = await fetch('http://api/tenants', {
    method: 'POST',
    body: JSON.stringify(data)
  })

  if (!response.ok) {
    throw new Error('Failed to create tenant')
  }

  revalidatePath('/tenants')
  return response.json()
}
```

## Autenticação

@carf/tscore/auth/react integrado:

```typescript
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

// app/providers.tsx
'use client'

import { AuthProvider } from '@carf/tscore/auth/react'
import { KeycloakClient } from '@carf/tscore/auth'

const keycloakClient = new KeycloakClient({
  url: process.env.NEXT_PUBLIC_KEYCLOAK_URL!,
  realm: 'carf',
  clientId: 'admin'
})

export function Providers({ children }) {
  return <AuthProvider client={keycloakClient}>{children}</AuthProvider>
}
```

## shadcn/ui

Component library baseado em Radix UI:

```typescript
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'

function CreateTenantDialog() {
  return (
    <Dialog>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Criar Tenant</DialogTitle>
        </DialogHeader>
        <form>
          <Label htmlFor="name">Nome</Label>
          <Input id="name" />
          <Button type="submit">Criar</Button>
        </form>
      </DialogContent>
    </Dialog>
  )
}
```

## API Client

```typescript
// lib/api.ts
import { useAuth } from '@carf/tscore/auth/react'

export async function apiClient(endpoint: string, options: RequestInit = {}) {
  const { getToken } = useAuth()
  const token = await getToken()

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...options.headers
    }
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`)
  }

  return response.json()
}
```

## Deployment

Next.js app deployado via Docker:

```dockerfile
FROM oven/bun:1 as builder
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

FROM oven/bun:1
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
CMD ["bun", "start"]
```

---

**Última atualização:** 2026-01-09
