---
status: review
updated: 2026-01-21
---

# Domain Components

Componentes especificos do dominio CARF/REURB que encapsulam logica de apresentacao de entidades do sistema.

## StatusBadge

Badge colorido para status de processos REURB e entidades.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| status | `'pending' \| 'in_progress' \| 'approved' \| 'rejected' \| 'active' \| 'inactive' \| 'draft' \| 'archived'` | `'pending'` | Status a exibir |
| label | `string` | - | Label customizado (sobrescreve default) |
| className | `string` | - | Classes adicionais |

### Status Colors

| Status | Cor | Label Default |
|:-------|:----|:--------------|
| pending | Amarelo (#FFCD07) | Pendente |
| in_progress | Azul (#3872C6) | Em Andamento |
| approved | Verde (#15981C) | Aprovado |
| rejected | Vermelho (#E63946) | Rejeitado |
| active | Verde (#15981C) | Ativo |
| inactive | Cinza | Inativo |
| draft | Cinza claro | Rascunho |
| archived | Cinza escuro | Arquivado |

### Examples

```tsx
import { StatusBadge } from '@carf/ui'

// Status REURB
<StatusBadge status="pending" />      // Pendente (amarelo)
<StatusBadge status="in_progress" />  // Em Andamento (azul)
<StatusBadge status="approved" />     // Aprovado (verde)
<StatusBadge status="rejected" />     // Rejeitado (vermelho)

// Status generico
<StatusBadge status="active" />       // Ativo
<StatusBadge status="inactive" />     // Inativo

// Label customizado
<StatusBadge status="pending" label="Aguardando Analise" />
```

## UnitCard

Card para exibicao de Unidade Habitacional com acoes opcionais.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| unit | `Unit` | **required** | Dados da unidade |
| onEdit | `() => void` | - | Callback ao clicar em Editar |
| onDelete | `() => void` | - | Callback ao clicar em Excluir |
| onViewMap | `() => void` | - | Callback ao clicar em Ver Mapa |
| showActions | `boolean` | `true` | Exibir botoes de acao |
| className | `string` | - | Classes adicionais |

### Unit Type

```typescript
interface Unit {
  id: string
  code: string           // Ex: "UN-001"
  address?: string       // Endereco completo
  area?: number          // Area em m²
  status?: 'pending' | 'in_progress' | 'approved' | 'rejected'
  holderCount?: number   // Quantidade de posseiros
}
```

### Examples

```tsx
import { UnitCard } from '@carf/ui'

const unit = {
  id: '123',
  code: 'UN-001',
  address: 'Rua das Flores, 123',
  area: 250,
  status: 'approved',
  holderCount: 2,
}

// Completo com acoes
<UnitCard
  unit={unit}
  onEdit={() => navigate(`/units/${unit.id}/edit`)}
  onDelete={() => confirmDelete(unit.id)}
  onViewMap={() => openMapModal(unit)}
/>

// Sem acoes (somente leitura)
<UnitCard unit={unit} showActions={false} />

// Em listagem
{units.map(unit => (
  <UnitCard
    key={unit.id}
    unit={unit}
    onEdit={() => setEditingUnit(unit)}
  />
))}
```

### Renders

O componente renderiza:
- **Header:** Codigo da unidade + StatusBadge (se status presente)
- **Description:** Endereco (se presente)
- **Content:** Area em m² e quantidade de posseiros
- **Footer:** Botoes Ver Mapa, Editar, Excluir (conforme callbacks passados)

## HolderCard

Card para exibicao de Posseiro/Titular.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| holder | `Holder` | **required** | Dados do posseiro |
| onEdit | `() => void` | - | Callback ao clicar em Editar |
| showUnits | `boolean` | `false` | Exibir unidades associadas |
| className | `string` | - | Classes adicionais |

### Holder Type

```typescript
interface Holder {
  id: string
  name: string
  cpf?: string           // Sera mascarado (***.***.***-XX)
  cnpj?: string          // Sera mascarado
  email?: string
  phone?: string
  unitCount?: number     // Quantidade de unidades
}
```

### Examples

```tsx
import { HolderCard } from '@carf/ui'

const holder = {
  id: '456',
  name: 'Maria Silva',
  cpf: '12345678901',
  email: 'maria@email.com',
  phone: '11999999999',
  unitCount: 1,
}

<HolderCard
  holder={holder}
  onEdit={() => navigate(`/holders/${holder.id}/edit`)}
/>
```

## CommunityCard

Card para exibicao de Comunidade/Nucleo Urbano.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| community | `Community` | **required** | Dados da comunidade |
| onEdit | `() => void` | - | Callback ao clicar em Editar |
| onSelect | `() => void` | - | Callback ao selecionar |
| className | `string` | - | Classes adicionais |

### Community Type

```typescript
interface Community {
  id: string
  name: string
  city?: string
  state?: string
  unitCount?: number
  status?: 'active' | 'inactive' | 'archived'
}
```

### Examples

```tsx
import { CommunityCard } from '@carf/ui'

const community = {
  id: '789',
  name: 'Vila das Flores',
  city: 'Sao Paulo',
  state: 'SP',
  unitCount: 150,
  status: 'active',
}

<CommunityCard
  community={community}
  onEdit={() => navigate(`/communities/${community.id}/edit`)}
  onSelect={() => setCurrentCommunity(community)}
/>
```

## Integracao com @carf/tscore

Os types locais (`Unit`, `Holder`, `Community`) sao compatíveis com os types exportados por `@carf/tscore`. Para integracao completa:

```tsx
import { UnitCard } from '@carf/ui'
import type { Unit } from '@carf/tscore'

// Unit de tscore tem mais campos, mas UnitCard aceita subset
const unit: Unit = await geoApiClient.units.getById('123')
<UnitCard unit={unit} />
```

## Composicao Avancada

Para customizacao além das props disponíveis, use os componentes base:

```tsx
import { Card, CardHeader, CardContent, StatusBadge, Button } from '@carf/ui'

// UnitCard customizado
function CustomUnitCard({ unit, children }) {
  return (
    <Card>
      <CardHeader>
        <div className="flex justify-between">
          <span>{unit.code}</span>
          <StatusBadge status={unit.status} />
        </div>
      </CardHeader>
      <CardContent>
        {children} {/* Conteudo customizado */}
      </CardContent>
    </Card>
  )
}
```
