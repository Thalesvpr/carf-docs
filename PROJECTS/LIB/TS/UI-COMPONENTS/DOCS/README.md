---
status: review
updated: 2026-01-20
---

# @carf/ui - Documentacao

Biblioteca de componentes React reutilizaveis baseada em shadcn/ui e Tailwind CSS para o ecossistema CARF.

> **Status: Em Desenvolvimento**
>
> A documentacao abaixo descreve a arquitetura planejada. Apenas utilitarios base (`cn`, `carfColors`) estao implementados.

## Instalacao

```bash
bun add @carf/ui
```

## Uso Atual

```typescript
import { cn, carfColors } from '@carf/ui'

// Merge de classes condicionais
const className = cn('base', isActive && 'active')

// Cores CARF
const primaryColor = carfColors.primary.DEFAULT  // '#2C5F2D'
```

## Documentacao

| Secao | Descricao |
|:------|:----------|
| [ARCHITECTURE/](./ARCHITECTURE/README.md) | Arquitetura planejada, componentes e patterns |
| [CONCEPTS/](./CONCEPTS/README.md) | Design tokens, acessibilidade, composicao |
| [HOW-TO/](./HOW-TO/README.md) | Setup, build, customizacao, testes |

## Roadmap de Implementacao

### Fase 1: Base
- [x] Utilitario `cn()` para merge de classes
- [x] Paleta de cores `carfColors`
- [ ] CSS Variables globais (globals.css)

### Fase 2: Componentes Form
- [ ] Button
- [ ] Input
- [ ] Label
- [ ] Checkbox
- [ ] Switch
- [ ] Select
- [ ] Textarea

### Fase 3: Componentes Layout
- [ ] Card
- [ ] Separator
- [ ] Tabs
- [ ] Accordion

### Fase 4: Componentes Feedback
- [ ] Alert
- [ ] Toast
- [ ] Dialog
- [ ] Progress

### Fase 5: Componentes Data Display
- [ ] Avatar
- [ ] Badge
- [ ] Tooltip
- [ ] Table

### Fase 6: Componentes Dominio CARF
- [ ] UnitCard
- [ ] HolderCard
- [ ] CommunityCard
- [ ] StatusBadge

## Referencias

- [Design System CARF](../../../CENTRAL/DESIGN-SYSTEM/README.md)
- [shadcn/ui](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)
