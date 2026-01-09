# ADMIN - Console Administrativo Next.js

Documentação do console administrativo CARF.

## Visão Geral

ADMIN é console administrativo Next.js 14 para gestão de tenants, usuários, equipes e configurações sistema CARF.

### Características

- **Next.js 14** - App Router com React Server Components
- **TypeScript** - Type safety completo
- **@carf/tscore** - Biblioteca compartilhada (auth, validations, types)
- **shadcn/ui** - Component library
- **TanStack Query** - Data fetching e cache
- **Tailwind CSS** - Styling utility-first
- **Keycloak** - Autenticação OAuth2/OIDC

## Tecnologias

- Next.js 14 App Router
- React 18
- TypeScript 5
- @carf/tscore ^0.1.0
- shadcn/ui components
- TanStack Query v5
- Tailwind CSS
- Bun runtime

## Setup Local

```bash
# Clonar
git clone https://github.com/Thalesvpr/carf-admin.git PROJECTS/ADMIN/SRC-CODE
cd PROJECTS/ADMIN/SRC-CODE

# Instalar dependências
bun install

# Configurar .env.local
cp .env.example .env.local
# Editar NEXT_PUBLIC_KEYCLOAK_URL, NEXT_PUBLIC_API_URL

# Dev server
bun dev

# Build production
bun build

# Start production
bun start
```

## Estrutura

```
PROJECTS/ADMIN/
├── DOCS/              # Documentação (esta pasta)
│   ├── README.md      # Este arquivo
│   ├── ARCHITECTURE/  # Arquitetura específica
│   ├── CONCEPTS/      # Conceitos técnicos
│   └── HOW-TO/        # Guias práticos
└── SRC-CODE/          # Código-fonte Next.js (carf-admin repo)
    ├── app/           # Next.js App Router
    ├── components/    # React components
    ├── lib/           # Utilities, API client
    └── types/         # Types suplementares locais
```

## Integração @carf/tscore

ADMIN usa @carf/tscore para:

### Autenticação

```typescript
// app/providers.tsx
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

### Validações

```typescript
// app/users/new/page.tsx
import { useForm } from 'react-hook-form'
import { CPF, Email } from '@carf/tscore/validations'

function NewUserPage() {
  const { register } = useForm()

  return (
    <form>
      <input
        {...register('cpf', {
          validate: (val) => CPF.validate(val) || 'CPF inválido'
        })}
      />
    </form>
  )
}
```

### Types

```typescript
import type { Tenant, Account, Team } from '@carf/tscore/types'
import { Role } from '@carf/tscore/types'

async function fetchTenants(): Promise<Tenant[]> {
  const response = await fetch('/api/tenants')
  return response.json()
}
```

## Responsabilidades

ADMIN gerencia:

- **Tenants** - Criar, editar, desativar prefeituras
- **Accounts** - Criar usuários, atribuir roles, gerenciar permissões
- **Teams** - Criar equipes, vincular usuários
- **Configurações** - Parâmetros sistema, integrations
- **Auditoria** - Logs de ações administrativas

## Documentação

- [Arquitetura](./ARCHITECTURE/README.md) - Decisões técnicas específicas do ADMIN
- [Conceitos](./CONCEPTS/README.md) - Conceitos técnicos Next.js, RSC
- [How-To](./HOW-TO/README.md) - Guias práticos de desenvolvimento

## Links

- **Repositório:** https://github.com/Thalesvpr/carf-admin
- **@carf/tscore:** [Biblioteca compartilhada](../../TSCORE/DOCS/README.md)
- **ADR-011:** [Decisão shared library](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-011-shared-library-tscore.md)

---

**Última atualização:** 2026-01-09
