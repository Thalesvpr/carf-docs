---
title: "@carf/tscore - Biblioteca Core"
description: "Value objects, validacoes e tipos TypeScript compartilhados"
status: review
updated: 2026-01-20
source: "CENTRAL/LIBRARIES/01-tscore.md"
---

# @carf/tscore

Biblioteca TypeScript core com value objects (CPF, CNPJ, Email, Phone), validacoes e tipos compartilhados entre todas as aplicacoes do ecossistema CARF.

## Instalacao

```bash
# Configurar registry
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/tscore
```

## Uso

```typescript
// Value Objects e Validacoes
import { CPF, CNPJ, Email, PhoneNumber } from '@carf/tscore/validations'

const cpf = new CPF('123.456.789-00')
console.log(cpf.isValid())  // true
console.log(cpf.formatted)  // "123.456.789-00"

// Tipos
import type { Unit, Holder, Community, UnitStatus } from '@carf/tscore/types'

// Autenticacao (Keycloak)
import { useAuth, ProtectedRoute } from '@carf/tscore/auth/react'
```

## Modulos

| Modulo | Descricao |
|:-------|:----------|
| `/validations` | Value objects com validacao (CPF, CNPJ, Email, Phone) |
| `/types` | Interfaces e enums compartilhados |
| `/auth/react` | Hooks React para Keycloak |
| `/auth/vue` | Composables Vue para Keycloak |

## Documentacao

**[DOCS/](./DOCS/README.md)** - Documentacao tecnica completa, incluindo:
- SPECS/ - Especificacoes tecnicas (package.json, tsconfig)
- API/ - Referencia de API
- CONCEPTS/ - Value objects e tipos
- HOW-TO/ - Guias praticos

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/TSCORE/DOCS/README|DOCS]]

<!-- CARF-INDEX-END -->
