---
type: leaf
title: "Exports Map - @carf/tscore"
status: review
updated: 2026-01-21
source: "interno"
---

# Exports Map - @carf/tscore

Sistema de subpath exports que permite importacao modular com tree-shaking automatico.

## Configuracao

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./validations": {
      "types": "./dist/validations/index.d.ts",
      "import": "./dist/validations/index.js"
    },
    "./types": {
      "types": "./dist/types/index.d.ts",
      "import": "./dist/types/index.js"
    },
    "./auth": {
      "types": "./dist/auth/index.d.ts",
      "import": "./dist/auth/index.js"
    },
    "./auth/react": {
      "types": "./dist/auth/react/index.d.ts",
      "import": "./dist/auth/react/index.js"
    },
    "./auth/vue": {
      "types": "./dist/auth/vue/index.d.ts",
      "import": "./dist/auth/vue/index.js"
    }
  }
}
```

## Subpaths Disponiveis

### `@carf/tscore`

Entry point principal com re-exports de todos os modulos:

```typescript
import { CPF, CNPJ, Email, Phone, Unit, Holder, KeycloakClient } from '@carf/tscore'
```

**Exporta:**
- Todos os Value Objects de validacao
- Todos os tipos TypeScript
- Cliente Keycloak base

### `@carf/tscore/validations`

Apenas Value Objects de validacao:

```typescript
import { CPF, CNPJ, Email, Phone, ValidationError } from '@carf/tscore/validations'
```

**Exporta:**
- `CPF` - Validacao de CPF brasileiro
- `CNPJ` - Validacao de CNPJ
- `Email` - Validacao de email
- `Phone` - Validacao de telefone brasileiro
- `ValidationError` - Classe de erro

**Usar quando:** Precisar apenas de validacoes, sem tipos ou auth.

### `@carf/tscore/types`

Tipos TypeScript do dominio:

```typescript
import type { Unit, Holder, Community, UnitStatus } from '@carf/tscore/types'
```

**Exporta:**
- Interfaces de entidades (Unit, Holder, Community, etc.)
- Enums (UnitStatus, Role, EntityType, etc.)
- DTOs (CreateUnitDto, UpdateHolderDto, etc.)

**Usar quando:** Precisar apenas de type definitions.

### `@carf/tscore/auth`

Cliente Keycloak base (framework-agnostico):

```typescript
import { KeycloakClient, AuthTokens, User } from '@carf/tscore/auth'
```

**Exporta:**
- `KeycloakClient` - Classe principal de autenticacao
- `AuthTokens` - Interface de tokens
- `User` - Interface de usuario autenticado
- `KeycloakConfig` - Interface de configuracao

**Usar quando:** Integrar com framework customizado ou SSR.

### `@carf/tscore/auth/react`

React hooks e componentes:

```typescript
import { useAuth, useUser, AuthProvider, ProtectedRoute } from '@carf/tscore/auth/react'
```

**Exporta:**
- `useAuth()` - Hook de estado de autenticacao
- `useUser()` - Hook de dados do usuario
- `usePermissions()` - Hook de verificacao de roles
- `useToken()` - Hook de acesso ao JWT
- `AuthProvider` - Context provider
- `ProtectedRoute` - Componente de rota protegida

**Requer:** `react` como peer dependency

### `@carf/tscore/auth/vue`

Vue 3 composables:

```typescript
import { useAuth, useUser, initAuth } from '@carf/tscore/auth/vue'
```

**Exporta:**
- `useAuth()` - Composable de autenticacao
- `useUser()` - Composable de usuario
- `usePermissions()` - Composable de roles
- `initAuth()` - Plugin de inicializacao

**Requer:** `vue` como peer dependency

## Tree-Shaking

O sistema de exports permite que bundlers eliminem codigo nao utilizado:

```typescript
// Importa APENAS validacoes - auth e types nao sao incluidos no bundle
import { CPF, CNPJ } from '@carf/tscore/validations'
```

### Exemplo de Reducao de Bundle

| Import | Bundle Size (estimado) |
|:-------|:-----------------------|
| `@carf/tscore` (tudo) | ~45KB |
| `@carf/tscore/validations` | ~8KB |
| `@carf/tscore/types` | ~0KB (types only) |
| `@carf/tscore/auth/react` | ~15KB |

## Estrutura de Arquivos

```
src/
├── index.ts              # Re-exports tudo
├── validations/
│   ├── index.ts          # Export de validacoes
│   ├── cpf.ts
│   ├── cnpj.ts
│   ├── email.ts
│   ├── phone.ts
│   └── error.ts
├── types/
│   ├── index.ts          # Export de types
│   ├── entities/
│   │   ├── unit.ts
│   │   ├── holder.ts
│   │   └── community.ts
│   ├── enums/
│   │   ├── unit-status.ts
│   │   └── role.ts
│   └── dtos/
│       ├── create-unit.ts
│       └── update-holder.ts
└── auth/
    ├── index.ts          # Export base auth
    ├── keycloak-client.ts
    ├── types.ts
    ├── react/
    │   ├── index.ts      # Export React hooks
    │   ├── provider.tsx
    │   ├── hooks.ts
    │   └── protected-route.tsx
    └── vue/
        ├── index.ts      # Export Vue composables
        ├── plugin.ts
        └── composables.ts
```

## Compatibilidade

### Bundlers Suportados

| Bundler | Suporte | Notas |
|:--------|:--------|:------|
| Vite | Completo | moduleResolution: bundler |
| esbuild | Completo | Usado pelo Bun |
| Webpack 5 | Completo | exports field support |
| Rollup | Completo | Via plugin |

### Node.js

Requer Node.js 18+ com suporte a ES Modules e exports field.

```bash
# Verificar versao
node --version  # >= 18.0.0
```
