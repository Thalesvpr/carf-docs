# Package Structure

Arquitetura do pacote @carf/tscore.

## Visão Geral

O @carf/tscore é a biblioteca compartilhada de tipos e utilitários TypeScript para projetos CARF, garantindo consistência entre frontend (GEOWEB), mobile (REURBCAD) e cliente API.

## Estrutura

```
src/
├── types/           # Tipos e interfaces compartilhados
│   ├── domain/      # Entidades de domínio
│   │   ├── unit.ts
│   │   ├── holder.ts
│   │   └── community.ts
│   ├── api/         # Tipos de request/response
│   │   ├── requests.ts
│   │   └── responses.ts
│   └── common/      # Tipos utilitários
│       ├── pagination.ts
│       └── result.ts
├── utils/           # Funções utilitárias
│   ├── validation/
│   │   ├── cpf.ts
│   │   └── geometry.ts
│   ├── formatting/
│   │   ├── address.ts
│   │   └── currency.ts
│   └── date/
│       └── formatters.ts
├── constants/       # Constantes compartilhadas
│   ├── status.ts
│   └── roles.ts
└── index.ts         # Exports públicos
```

## Exports

```typescript
// index.ts
// Types
export * from './types/domain';
export * from './types/api';
export * from './types/common';

// Utils
export * from './utils/validation';
export * from './utils/formatting';
export * from './utils/date';

// Constants
export * from './constants';
```

## Exemplo de Tipo

```typescript
// types/domain/unit.ts
export interface Unit {
  id: string;
  code: string;
  status: UnitStatus;
  address: Address;
  geometry: GeoJsonPolygon;
  areaM2: number;
  centroid: Centroid;
  tenantId: string;
  createdAt: string;
  updatedAt: string;
}

export type UnitStatus = 'Rascunho' | 'Pendente' | 'Aprovado' | 'Rejeitado';

export interface Address {
  street: string;
  number: string;
  complement?: string;
  neighborhood: string;
  city: string;
  state: string;
  zipCode: string;
}
```

## Build

```bash
# Desenvolvimento
pnpm dev

# Build produção
pnpm build

# Type check
pnpm typecheck
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
