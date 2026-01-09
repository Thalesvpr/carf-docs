# @carf/tscore

TypeScript shared library for CARF ecosystem providing authentication, validations, and domain types.

## 📦 Installation

```bash
# Configure GitHub Packages registry
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Install with Bun
bun add @carf/tscore

# Or with npm
npm install @carf/tscore
```

## 🚀 Usage

### Validations

```typescript
import { CPF, CNPJ, Email, Phone } from '@carf/tscore/validations'

// CPF validation
const cpf = new CPF('123.456.789-09')
console.log(cpf.format()) // "123.456.789-09"
console.log(cpf.toString()) // "12345678909"

// CNPJ validation
const cnpj = new CNPJ('12.345.678/0001-99')

// Email validation (RFC 5322)
const email = new Email('user@example.com')

// Phone validation (BR format)
const phone = new Phone('(11) 98765-4321')
```

### Types

```typescript
import type { Unit, Holder, Community, UnitStatus, Role } from '@carf/tscore/types'

const unit: Unit = {
  id: '123',
  code: 'U-001',
  status: 'APPROVED',
  // ...
}
```

### Auth (React)

```typescript
import { useAuth, ProtectedRoute } from '@carf/tscore/auth/react'

function App() {
  const { user, login, logout, hasRole } = useAuth()

  return (
    <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
      <Dashboard />
    </ProtectedRoute>
  )
}
```

### Auth (Vue 3)

```typescript
import { useAuth } from '@carf/tscore/auth/vue'

export default {
  setup() {
    const { user, login, logout, hasRole } = useAuth()
    return { user, login, logout, hasRole }
  }
}
```

## 📚 Modules

- **`@carf/tscore/validations`** - Value Objects with validation (CPF, CNPJ, Email, Phone, etc.)
- **`@carf/tscore/types`** - TypeScript interfaces and enums for domain entities
- **`@carf/tscore/auth/react`** - Keycloak authentication hooks for React
- **`@carf/tscore/auth/vue`** - Keycloak authentication composables for Vue 3

## 🔧 Development

```bash
# Clone
git clone https://github.com/Thalesvpr/carf-tscore.git
cd carf-tscore

# Install
bun install

# Develop
bun run dev

# Test
bun test

# Build
bun run build:all
```

## 📝 License

Copyright © 2024-2026 CARF Team. All rights reserved.

---

This project was created using `bun init` with Bun v1.3.4.
