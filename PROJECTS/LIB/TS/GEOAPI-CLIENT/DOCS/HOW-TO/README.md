---
title: "How-To Guides - @carf/geoapi-client"
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
status: rejected
updated: 2026-01-22
source: "interno"
---

# How-To Guides - @carf/geoapi-client

Guias praticos para uso da biblioteca @carf/geoapi-client.

## Guias Disponiveis

| Guia | Descricao |
|:-----|:----------|
| 01-getting-started | Instalacao, configuracao e uso basico |
| 02-error-handling | Tratamento de erros da API |
| 03-file-upload | Upload de arquivos com progresso |

## Quick Start

```bash
# Instalar
bun add @carf/geoapi-client @carf/tscore

# Configurar .npmrc
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc
```

```typescript
import { createGeoApiClient } from '@carf/geoapi-client'

const api = createGeoApiClient({
  baseUrl: process.env.API_URL,
  auth: { type: 'keycloak', realm: 'carf' },
})

// Usar
const units = await api.units.list()
const holder = await api.holders.getById(id)
```

## Topicos Abordados

- Instalacao e configuracao inicial
- Autenticacao com Keycloak
- Tratamento de erros HTTP
- Retry automatico e circuit breaker
- Upload de arquivos com progresso
- Integracao com React Query

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/HOW-TO/01-getting-started.md|Getting Started]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/HOW-TO/02-error-handling.md|Error Handling - Guia Pratico]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/HOW-TO/03-file-upload.md|File Upload - Guia Pratico]]

<!-- CARF-INDEX-END -->
