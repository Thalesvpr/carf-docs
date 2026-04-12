---
type: leaf
status: active
updated: 2026-02-09
---

# Getting Started

Guia de inicio rapido para o @carf/geoapi-client.

## Instalacao

Instalar via bun:

```bash
bun add @carf/geoapi-client
```

Para usar hooks React Query (REURBWEB), tambem instalar:

```bash
bun add @tanstack/react-query
```

## Para Devs do Pacote: Geracao

O client e auto-gerado a partir do swagger.json da GEOAPI. Para regenerar apos mudancas na API:

```bash
# Baixar swagger atualizado (API deve estar rodando em localhost:5127)
bun run swagger:fetch

# Gerar tipos e hooks
bun run generate
```

## Configuracao

Criar o client passando baseURL e callbacks de auth:

```typescript
import { createApiClient } from '@carf/geoapi-client';

const api = createApiClient({
  baseURL: 'http://localhost:5127',
  getToken: async () => {
    // Sua logica de auth — ex: KeycloakClient, SecureStore, etc.
    return keycloakClient.getAccessToken();
  },
  getTenantId: () => {
    return currentUser.tenantId;
  },
});
```

## Uso com Hooks React Query (REURBWEB)

Os hooks sao gerados automaticamente pelo orval:

```typescript
import { useGetApiUnits, usePostApiUnits } from '@carf/geoapi-client';

function UnitsPage() {
  // GET /api/units
  const { data, isLoading } = useGetApiUnits({ communityId, page: 1, pageSize: 20 });

  // POST /api/units
  const createUnit = usePostApiUnits();

  const handleCreate = () => {
    createUnit.mutate({ data: { /* unit data */ } });
  };
}
```

## Uso com Funcoes Vanilla (qualquer app)

Para apps sem React Query:

```typescript
import { getApiUnits, postApiUnits } from '@carf/geoapi-client';

// GET /api/units
const units = await getApiUnits({ communityId, page: 1, pageSize: 20 });

// POST /api/units
const created = await postApiUnits({ /* unit data */ });
```

## Tratamento de Erros

Erros sao tipados automaticamente:

```typescript
import { ApiError, NotFoundError, ValidationError } from '@carf/geoapi-client';

try {
  await getApiUnitsId(unitId);
} catch (error) {
  if (error instanceof NotFoundError) {
    // Unidade nao encontrada
  } else if (error instanceof ValidationError) {
    // Dados invalidos — error.details contem campos
  } else if (error instanceof ApiError) {
    // Outro erro HTTP
  }
}
```
