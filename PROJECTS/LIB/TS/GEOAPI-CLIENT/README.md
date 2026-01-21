---
title: "@carf/geoapi-client - HTTP Client"
description: "Cliente HTTP type-safe para comunicacao com GEOAPI"
status: review
updated: 2026-01-20
source: "CENTRAL/LIBRARIES/02-geoapi-client.md"
---

# @carf/geoapi-client

Cliente HTTP type-safe para comunicacao com a API GEOAPI. Fornece metodos tipados para todas as operacoes da API com tratamento de erros, retry automatico e circuit breaker.

## Instalacao

```bash
# Configurar registry
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/geoapi-client @carf/tscore
```

## Uso

```typescript
import { createGeoApiClient } from '@carf/geoapi-client'

const client = createGeoApiClient({
  baseUrl: 'https://api.carf.gov.br',
  auth: { type: 'keycloak', realm: 'carf' },
})

// Listar unidades
const units = await client.units.list({ status: 'APPROVED' })

// Criar unidade
const unit = await client.units.create({
  code: 'UN-001',
  communityId: '...',
  street: 'Rua das Flores',
  city: 'Sao Paulo',
  state: 'SP',
})
```

## APIs Disponiveis

| API | Descricao |
|:----|:----------|
| `units` | Unidades habitacionais |
| `holders` | Posseiros |
| `communities` | Comunidades |
| `legitimation` | Processos de legitimacao |
| `documents` | Upload e download de documentos |
| `reports` | Geracao de relatorios |

## Documentacao

**[DOCS/](./DOCS/README.md)** - Documentacao tecnica completa, incluindo:
- SPECS/ - Especificacoes tecnicas (package.json, client config)
- API/ - Referencia de APIs (units, holders, etc.)
- ARCHITECTURE/ - Arquitetura do cliente
- HOW-TO/ - Guias praticos

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/README|DOCS]]

<!-- CARF-INDEX-END -->
