---
type: readme
status: rejected
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
updated: 2026-01-22
---

# API Reference - @carf/geoapi-client

## Overview

Referencia completa do cliente HTTP @carf/geoapi-client com todos os endpoints disponiveis organizados por dominio. Types TypeScript sincronizados com @carf/tscore.

## Endpoints Documentados

| API | Arquivo | Descricao |
|:----|:--------|:----------|
| Units | [01-units-api.md](./01-units-api.md) | Unidades Habitacionais - CRUD, holders, documents |
| Holders | [02-holders-api.md](./02-holders-api.md) | Posseiros/Titulares - CRUD, busca por CPF/CNPJ |
| Communities | [03-communities-api.md](./03-communities-api.md) | Comunidades/Nucleos - CRUD, estatisticas, geometria |
| Legitimation | [04-legitimation-api.md](./04-legitimation-api.md) | Processos de Legitimacao - workflow, historico |
| Documents | [05-documents-api.md](./05-documents-api.md) | Upload, download e gestao de documentos |
| Reports | [06-reports-api.md](./06-reports-api.md) | Geracao e download de relatorios |

## Configuracao do Cliente

```typescript
import { GeoApiClient } from '@carf/geoapi-client'

const api = new GeoApiClient({
  baseURL: process.env.GEOAPI_URL || 'https://api.carf.gov.br',
  auth: {
    getAccessToken: () => keycloak.token,
    refreshToken: () => keycloak.updateToken(30)
  },
  timeout: 30000,  // 30 segundos
  retry: {
    maxRetries: 3,
    retryDelay: 1000
  }
})

// Usar APIs
api.units.list()
api.holders.create(data)
api.communities.getStatistics(id)
api.legitimation.executeAction(id, action)
```

## Tratamento de Erros

```typescript
import { ApiError, NotFoundError, ValidationError, ConflictError } from '@carf/geoapi-client'

try {
  const unit = await api.units.getById('invalid-id')
} catch (error) {
  if (error instanceof NotFoundError) {
    // 404 - Recurso nao encontrado
  } else if (error instanceof ValidationError) {
    // 400 - Dados invalidos
    console.log(error.validationErrors)
  } else if (error instanceof ConflictError) {
    // 409 - Conflito de versao
  } else if (error instanceof ApiError) {
    // Outros erros HTTP
    console.log(error.status, error.message)
  }
}
```

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/API/01-units-api.md|Units API - Gerenciamento de Unidades Habitacionais]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/API/02-holders-api.md|Holders API - Gerenciamento de Posseiros/Titulares]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/API/03-communities-api.md|Communities API - Gerenciamento de Comunidades/Nucleos Urbanos]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/API/04-legitimation-api.md|Legitimation API - Processos de Legitimacao Fundiaria]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/API/05-documents-api.md|Documents API - Gerenciamento de Documentos]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/API/06-reports-api.md|Reports API - Geracao de Relatorios]]

<!-- CARF-INDEX-END -->
