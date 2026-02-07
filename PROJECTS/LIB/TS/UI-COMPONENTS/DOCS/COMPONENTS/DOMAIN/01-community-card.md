---
type: leaf
status: approved
updated: 2026-02-07
---

# CommunityCard

Componente card para exibicao de comunidades/assentamentos no sistema CARF.

## Props

| Prop | Tipo | Obrigatorio | Descricao |
|------|------|-------------|-----------|
| community | Community | Sim | Dados da comunidade |
| onEdit | () => void | Nao | Callback ao clicar em Editar |
| onViewDetails | () => void | Nao | Callback ao clicar em Detalhes |
| onViewUnits | () => void | Nao | Callback ao clicar em Unidades |
| showActions | boolean | Nao | Exibir botoes de acao (default: true) |

## Interface Community

```typescript
interface Community {
  id: string
  name: string
  description?: string
  status?: 'active' | 'inactive' | 'archived'
  unitCount?: number
  holderCount?: number
  city?: string
  state?: string
}
```

## Uso

```tsx
import { CommunityCard } from '@carf/ui'

<CommunityCard
  community={{
    id: '1',
    name: 'Vila Esperanca',
    city: 'Sao Paulo',
    state: 'SP',
    status: 'active',
    unitCount: 150,
    holderCount: 320
  }}
  onViewDetails={() => navigate(`/communities/1`)}
  onViewUnits={() => navigate(`/communities/1/units`)}
/>
```

## Exibicao

- Titulo: nome da comunidade
- Subtitulo: cidade, estado
- Badge: status (ativo, inativo, arquivado)
- Metricas: quantidade de unidades e titulares
- Descricao: texto truncado em 2 linhas

## Acessibilidade

- Card usa semantica article
- Botoes com labels descritivos
- Contraste adequado para texto
