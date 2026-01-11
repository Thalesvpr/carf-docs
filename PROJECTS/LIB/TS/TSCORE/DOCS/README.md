# @carf/tscore - Biblioteca TypeScript Compartilhada

Biblioteca TypeScript compartilhada para projetos CARF, eliminando duplicação de código entre GEOWEB, REURBCAD, ADMIN e WEBDOCS.

## Visão Geral

@carf/tscore é um NPM package publicado no GitHub Packages contendo:

- **Autenticação Keycloak** - OAuth2/OIDC client, token management, role checking
- **Value Objects** - CPF, CNPJ, Email, Phone com validações brasileiras
- **Types TypeScript** - Entities, Enums, DTOs sincronizados com backend .NET
- **Hooks React** - useAuth, useKeycloak, ProtectedRoute
- **Composables Vue** - useAuth, initAuth para Vue 3

## Instalação

### Configurar GitHub Packages

Crie `.npmrc` na raiz do projeto:

```
@carf:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

### Instalar Package

```bash
# Com Bun (recomendado)
bun add @carf/tscore

# Com npm
npm install @carf/tscore
```

## Uso Básico

### Validações

```typescript
import { CPF, CNPJ, Email, Phone } from '@carf/tscore/validations'

// CPF validation
const cpf = new CPF('123.456.789-09')
console.log(cpf.format()) // "123.456.789-09"
console.log(cpf.toString()) // "12345678909"

// CNPJ validation
const cnpj = new CNPJ('11.444.777/0001-61')
console.log(cnpj.format()) // "11.444.777/0001-61"

// Email validation
const email = new Email('user@example.com')

// Phone validation (Brazilian format)
const phone = new Phone('(11) 98765-4321')
```

### Types

```typescript
import type { Unit, Holder, Community } from '@carf/tscore/types'
import { UnitStatus, Role } from '@carf/tscore/types'

const unit: Unit = {
  id: 'uuid',
  code: 'UN-001',
  status: UnitStatus.APPROVED,
  // ... outros campos
}

const hasPermission = (userRole: Role) => {
  return userRole === Role.ADMIN || userRole === Role.SUPER_ADMIN
}
```

### Autenticação (React)

```typescript
import { AuthProvider, useAuth, ProtectedRoute } from '@carf/tscore/auth/react'
import { KeycloakClient } from '@carf/tscore/auth'
import { Role } from '@carf/tscore/types'

// Setup no App.tsx
const keycloakClient = new KeycloakClient({
  url: 'http://localhost:8080',
  realm: 'carf',
  clientId: 'geoweb'
})

function App() {
  return (
    <AuthProvider client={keycloakClient}>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/admin"
            element={
              <ProtectedRoute requiredRoles={[Role.ADMIN]}>
                <AdminPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

// Uso em componentes
function UserProfile() {
  const { user, hasRole, logout } = useAuth()

  return (
    <div>
      <p>Olá, {user?.name}</p>
      {hasRole(Role.ADMIN) && <AdminPanel />}
      <button onClick={logout}>Sair</button>
    </div>
  )
}
```

### Autenticação (Vue 3)

```typescript
import { createApp } from 'vue'
import { initAuth } from '@carf/tscore/auth/vue'
import { KeycloakClient } from '@carf/tscore/auth'
import App from './App.vue'

const keycloakClient = new KeycloakClient({
  url: 'http://localhost:8080',
  realm: 'carf',
  clientId: 'webdocs'
})

const app = createApp(App)
initAuth(app, keycloakClient)
app.mount('#app')

// Uso em components
<script setup lang="ts">
import { useAuth } from '@carf/tscore/auth/vue'
import { Role } from '@carf/tscore/types'

const { user, hasRole, logout } = useAuth()
</script>

<template>
  <div>
    <p>Olá, {{ user?.name }}</p>
    <AdminPanel v-if="hasRole(Role.ADMIN)" />
    <button @click="logout">Sair</button>
  </div>
</template>
```

## Documentação

- [Arquitetura](./ARCHITECTURE/README.md) - Decisões de design da biblioteca
- [Conceitos](./CONCEPTS/README.md) - Value Objects, Validations, Auth
- [How-To](./HOW-TO/README.md) - Guias práticos de uso
- [API Reference](./API/README.md) - Documentação completa da API

## Versionamento

@carf/tscore segue **Semantic Versioning**:

- **MAJOR** - Breaking changes (alterar signatures, remover métodos)
- **MINOR** - Novas features backward-compatible
- **PATCH** - Bug fixes

Ver **CHANGELOG** para histórico completo.

## Desenvolvimento

Para contribuir com a biblioteca:

```bash
# Clonar repositório
git clone https://github.com/Thalesvpr/carf-tscore.git PROJECTS/TSCORE/SRC-CODE
cd PROJECTS/TSCORE/SRC-CODE

# Instalar dependências
bun install

# Rodar testes
bun test

# Build
bun run build

# Testar localmente em outro projeto
npm link
cd ../../../GEOWEB/SRC-CODE
npm link @carf/tscore
```

## Links

- [Source Code README](../SRC-CODE/carf-tscore/README.md) - Repositório e setup local
- [CHANGELOG.md](../SRC-CODE/carf-tscore/CHANGELOG.md) - Histórico completo de versões e mudanças
- **Repositório:** https://github.com/Thalesvpr/carf-tscore
- **NPM Package:** https://github.com/Thalesvpr/carf-tscore/packages
- **ADR-011:** **Decisão de criar biblioteca compartilhada**

---

**Última atualização:** 2026-01-09
