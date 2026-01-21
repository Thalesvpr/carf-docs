---
title: "@carf/ui - Biblioteca de Componentes React"
description: "Componentes React baseados em shadcn/ui e Tailwind CSS para o ecossistema CARF"
status: review
updated: 2026-01-20
source: "CENTRAL/LIBRARIES/03-ui-components.md"
---

# @carf/ui

Biblioteca de componentes React reutilizaveis baseada em shadcn/ui e Tailwind CSS, customizada para o ecossistema CARF, garantindo consistencia visual e acessibilidade WCAG 2.1 AA.

> **Status: Especificado (Nao Implementado)**
>
> Esta documentacao especifica a API completa da biblioteca. A implementacao seguira estas especificacoes.

## Instalacao (quando publicado)

```bash
# Configurar registry
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/ui

# Instalar peer dependencies
bun add @radix-ui/react-dialog @radix-ui/react-dropdown-menu \
  @radix-ui/react-tabs lucide-react tailwindcss
```

## Uso

```tsx
import { Button, Card, Input, Badge, StatusBadge, UnitCard } from '@carf/ui'
import { cn, carfColors, formatCPF } from '@carf/ui'
import { useTheme, useMediaQuery, useDebounce } from '@carf/ui'
import '@carf/ui/globals.css'  // CSS variables globais
```

## Componentes Especificados

### Form (7 componentes)

| Componente | Variants | Descricao |
|:-----------|:---------|:----------|
| Button | default, destructive, outline, secondary, ghost, link | Botao com tamanhos sm, default, lg, icon |
| Input | - | Campo de texto com suporte a mascaras |
| Label | - | Label acessivel para inputs |
| Checkbox | - | Checkbox com Radix UI |
| Switch | - | Toggle on/off |
| Select | - | Dropdown com compound components |
| Textarea | - | Campo de texto multilinhas |

### Layout (4 componentes)

| Componente | Descricao |
|:-----------|:----------|
| Card | Container com Header, Content, Footer |
| Separator | Linha divisoria horizontal/vertical |
| Tabs | Navegacao em abas |
| Accordion | Conteudo expansivel |

### Feedback (5 componentes)

| Componente | Descricao |
|:-----------|:----------|
| Alert | Mensagem de alerta |
| Toast | Notificacao temporaria |
| Dialog | Modal acessivel |
| AlertDialog | Modal de confirmacao |
| Progress | Barra de progresso |

### Data Display (5 componentes)

| Componente | Descricao |
|:-----------|:----------|
| Avatar | Imagem circular com fallback |
| Badge | Label colorido |
| Tooltip | Hint contextual |
| Popover | Container flutuante |
| Table | Tabela com compound components |

### Navigation (1 componente)

| Componente | Descricao |
|:-----------|:----------|
| DropdownMenu | Menu suspenso com submenus |

### CARF Domain (4 componentes)

| Componente | Descricao |
|:-----------|:----------|
| StatusBadge | Badge de status REURB |
| UnitCard | Card de Unidade Habitacional |
| HolderCard | Card de Posseiro |
| CommunityCard | Card de Comunidade |

## Documentacao Tecnica

**[DOCS/](./DOCS/README.md)** - Documentacao completa, incluindo:
- SPECS/ - Especificacoes tecnicas (package.json, tailwind, globals.css)
- ARCHITECTURE/ - Arquitetura e patterns
- CONCEPTS/ - Conceitos fundamentais (atomic design, acessibilidade)
- API/ - Referencia de API por componente
- HOW-TO/ - Guias praticos

## Roadmap de Implementacao

| Fase | Componentes | Status |
|:-----|:------------|:-------|
| 1. Setup | package.json, tailwind.config, globals.css | Especificado |
| 2. Utils | cn(), formatters, validators | Especificado |
| 3. Form | Button, Input, Label, Checkbox, Switch, Select | Especificado |
| 4. Layout | Card, Separator, Tabs, Accordion | Especificado |
| 5. Feedback | Alert, Toast, Dialog, Progress | Especificado |
| 6. Data | Avatar, Badge, Tooltip, Table | Especificado |
| 7. Domain | StatusBadge, UnitCard, HolderCard | Especificado |
| 8. Storybook | Documentacao interativa | Especificado |

## Referencias

- CENTRAL/DESIGN-SYSTEM/README.md - Tokens e cores
- [shadcn/ui](https://ui.shadcn.com/) - Componentes base
- [Radix UI](https://www.radix-ui.com/) - Primitivos acessiveis

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/README|DOCS]]

<!-- CARF-INDEX-END -->
