# Getting Started

Guia de início rápido para o GEOAPI Client TypeScript.

## Instalação

```bash
npm install @carf/geoapi-client
# ou
pnpm add @carf/geoapi-client
```

## Configuração

```typescript
import { GeoApiClient } from '@carf/geoapi-client';

const client = new GeoApiClient({
  baseUrl: 'https://api.carf.com.br',
  getAccessToken: async () => {
    // Retornar token JWT do seu auth provider
    return localStorage.getItem('access_token');
  },
  tenantId: 'seu-tenant-uuid'
});
```

## Uso Básico

### Listar Unidades

```typescript
const units = await client.units.list({
  page: 1,
  limit: 20,
  status: 'Aprovado'
});

console.log(units.data);
console.log(units.pagination.total);
```

### Criar Unidade

```typescript
const newUnit = await client.units.create({
  address: {
    street: 'Rua das Flores',
    number: '123',
    neighborhood: 'Centro',
    city: 'São Paulo',
    state: 'SP',
    zipCode: '01310-100'
  },
  geometry: {
    type: 'Polygon',
    coordinates: [[[-46.6388, -23.5489], ...]]
  }
});

console.log(newUnit.id, newUnit.code);
```

### Buscar por ID

```typescript
const unit = await client.units.getById('unit-uuid', {
  include: ['holders', 'community']
});

console.log(unit.holders);
```

### Tratamento de Erros

```typescript
import { ApiError } from '@carf/geoapi-client';

try {
  await client.units.create(data);
} catch (error) {
  if (error instanceof ApiError) {
    console.log(error.status); // 400, 401, 409, etc.
    console.log(error.code);   // 'GEOMETRY_OVERLAP'
    console.log(error.message);
  }
}
```

## Com React Query

```typescript
import { useQuery, useMutation } from '@tanstack/react-query';

function useUnits(filters: UnitFilters) {
  return useQuery({
    queryKey: ['units', filters],
    queryFn: () => client.units.list(filters)
  });
}

function useCreateUnit() {
  return useMutation({
    mutationFn: (data: CreateUnitRequest) => client.units.create(data),
    onSuccess: () => queryClient.invalidateQueries(['units'])
  });
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
