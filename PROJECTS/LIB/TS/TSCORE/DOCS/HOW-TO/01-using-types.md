# Using Types

Como utilizar os tipos do @carf/tscore em seus projetos.

## Instalação

```bash
npm install @carf/tscore
# ou
pnpm add @carf/tscore
```

## Importando Tipos

```typescript
import type {
  Unit,
  Holder,
  Community,
  UnitStatus,
  Address,
  PagedResult,
  Result
} from '@carf/tscore';
```

## Usando em Componentes React

```typescript
import type { Unit, UnitStatus } from '@carf/tscore';

interface UnitCardProps {
  unit: Unit;
  onStatusChange?: (status: UnitStatus) => void;
}

function UnitCard({ unit, onStatusChange }: UnitCardProps) {
  return (
    <div>
      <h3>{unit.code}</h3>
      <p>{unit.address.street}, {unit.address.number}</p>
      <span className={`status-${unit.status.toLowerCase()}`}>
        {unit.status}
      </span>
    </div>
  );
}
```

## Usando Utilitários de Validação

```typescript
import { validateCPF, formatCPF, maskCPF } from '@carf/tscore';

// Validar
const isValid = validateCPF('12345678909'); // true
const isInvalid = validateCPF('12345678900'); // false

// Formatar
const formatted = formatCPF('12345678909'); // '123.456.789-09'

// Mascarar
const masked = maskCPF('12345678909'); // '***.***.***-09'
```

## Usando Formatadores

```typescript
import { formatAddress, formatCurrency, formatDate } from '@carf/tscore';

// Endereço
const address = formatAddress({
  street: 'Rua das Flores',
  number: '123',
  neighborhood: 'Centro',
  city: 'São Paulo',
  state: 'SP',
  zipCode: '01310-100'
});
// "Rua das Flores, 123 - Centro, São Paulo/SP"

// Moeda
const price = formatCurrency(1500.50); // "R$ 1.500,50"

// Data
const date = formatDate('2026-01-16T10:30:00Z'); // "16/01/2026 10:30"
```

## Tipos de API

```typescript
import type {
  CreateUnitRequest,
  UpdateUnitRequest,
  UnitResponse,
  PagedResult,
  ApiError
} from '@carf/tscore';

async function createUnit(data: CreateUnitRequest): Promise<UnitResponse> {
  const response = await fetch('/api/units', {
    method: 'POST',
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    const error: ApiError = await response.json();
    throw new Error(error.message);
  }

  return response.json();
}
```

## Constantes

```typescript
import { UNIT_STATUS, USER_ROLES, REURB_MODALITIES } from '@carf/tscore';

// Usar em selects
const statusOptions = Object.values(UNIT_STATUS);
// ['Rascunho', 'Pendente', 'Aprovado', 'Rejeitado']

// Verificar roles
if (user.roles.includes(USER_ROLES.APROVADOR)) {
  // Mostrar botão de aprovar
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
