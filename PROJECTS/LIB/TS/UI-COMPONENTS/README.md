---
status: review
updated: 2026-01-20
---

# UI-COMPONENTS

Biblioteca de componentes React reutilizaveis baseada em shadcn/ui e Tailwind CSS, customizada para o ecossistema CARF, garantindo consistencia visual e acessibilidade WCAG 2.1 AA.

> **Status: Em Desenvolvimento**
>
> Esta biblioteca esta em fase inicial de implementacao. Apenas utilitarios base estao disponiveis.

## Implementado

| Modulo | Descricao |
|:-------|:----------|
| `cn()` | Funcao utilitaria para merge de classes Tailwind |
| `carfColors` | Objeto com paleta de cores oficial CARF |

```typescript
import { cn, carfColors } from '@carf/ui'

// Merge de classes condicionais
cn('base-class', isActive && 'active-class', variant === 'primary' && 'primary-class')

// Acesso a cores
carfColors.yellow  // '#FFCD07'
carfColors.primary.DEFAULT  // '#2C5F2D'
```

## Planejado (nao implementado)

### Componentes Form
- Button, Input, Label, Checkbox, Switch, Select, Textarea, Form

### Componentes Layout
- Card, Separator, Tabs, Accordion

### Componentes Feedback
- Alert, Toast, Dialog, AlertDialog, Progress

### Componentes Data Display
- Avatar, Badge, Tooltip, Popover, Table

### Componentes Navigation
- DropdownMenu, NavigationMenu

### Componentes Dominio CARF
- UnitCard, HolderCard, CommunityCard, StatusBadge

## Instalacao

```bash
bun add @carf/ui
```

## Documentacao

- **[DOCS/](./DOCS/README.md)** - Documentacao tecnica
- **[SRC-CODE/](./SRC-CODE/)** - Codigo fonte

## Roadmap

1. Implementar componentes base (shadcn/ui)
2. Criar tema CARF com CSS variables
3. Adicionar componentes de dominio
4. Configurar Storybook
5. Publicar no GitHub Packages

## Referencias

- [Design System CARF](../../CENTRAL/DESIGN-SYSTEM/README.md)
- [shadcn/ui](https://ui.shadcn.com/)

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/README|DOCS]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE/README|SRC-CODE]]

<!-- CARF-INDEX-END -->
