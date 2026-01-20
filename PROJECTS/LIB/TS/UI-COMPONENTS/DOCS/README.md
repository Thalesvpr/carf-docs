---
status: approved
updated: 2026-01-20
---

# @carf/ui

Biblioteca de componentes React baseada em shadcn/ui e Tailwind CSS implementando o Design System CARF. Fornece componentes reutilizaveis para GEOWEB, ADMIN e futuras aplicacoes web do ecossistema.

## Instalacao

```bash
bun add @carf/ui
```

## Uso

```tsx
import { Button, Card, Input, Badge, StatusBadge, UnitCard } from '@carf/ui'
import { cn, carfColors, formatCPF } from '@carf/ui'
import { useTheme, useMediaQuery, useDebounce } from '@carf/ui'
import '@carf/ui/styles'  // CSS variables globais
```

## Componentes Disponiveis

### Form (7 componentes)

| Componente | Variants | Descricao |
|:-----------|:---------|:----------|
| Button | default, destructive, outline, secondary, ghost, link, success, warning | Botao com 4 tamanhos (sm, default, lg, icon) |
| Input | - | Campo de texto com suporte a mascaras |
| Label | - | Label acessivel para inputs |
| Checkbox | - | Checkbox com Radix UI |
| Switch | - | Toggle on/off |
| Select | - | Dropdown com compound components |
| Textarea | - | Campo de texto multilinhas |

### Layout (4 componentes)

| Componente | Variants | Descricao |
|:-----------|:---------|:----------|
| Card | - | Container com Header, Content, Footer |
| Separator | horizontal, vertical | Linha divisoria |
| Tabs | - | Navegacao em abas |
| Accordion | - | Conteudo expansivel |

### Feedback (5 componentes)

| Componente | Variants | Descricao |
|:-----------|:---------|:----------|
| Alert | default, destructive | Mensagem de alerta |
| Toast | - | Notificacao temporaria |
| Dialog | - | Modal acessivel |
| AlertDialog | - | Modal de confirmacao |
| Progress | - | Barra de progresso |

### Data Display (5 componentes)

| Componente | Variants | Descricao |
|:-----------|:---------|:----------|
| Avatar | - | Imagem circular com fallback |
| Badge | default, secondary, destructive, outline | Label colorido |
| Tooltip | - | Hint contextual |
| Popover | - | Container flutuante |
| Table | - | Tabela com compound components |

### Navigation (1 componente)

| Componente | Variants | Descricao |
|:-----------|:---------|:----------|
| DropdownMenu | - | Menu suspenso com submenus |

### CARF Domain (4 componentes)

| Componente | Variants | Descricao |
|:-----------|:---------|:----------|
| StatusBadge | pending, progress, approved, rejected, cancelled | Badge de status REURB |
| UnitCard | - | Card de Unidade Habitacional |
| HolderCard | - | Card de Posseiro |
| CommunityCard | - | Card de Comunidade |

## Hooks

| Hook | Descricao |
|:-----|:----------|
| useTheme | Gerenciamento de tema (light/dark/system) |
| useMediaQuery | Query responsiva |
| useDebounce | Debounce de valores |

## Utils

| Funcao | Descricao |
|:-------|:----------|
| cn() | Merge de classes Tailwind (clsx + twMerge) |
| carfColors | Paleta de cores CARF |
| formatCPF() | Formata CPF (000.000.000-00) |
| formatCNPJ() | Formata CNPJ (00.000.000/0000-00) |
| formatPhone() | Formata telefone |

## Documentacao

| Secao | Descricao |
|:------|:----------|
| [ARCHITECTURE/](./ARCHITECTURE/README.md) | Arquitetura, patterns, integracao |
| [CONCEPTS/](./CONCEPTS/README.md) | Design tokens, acessibilidade |
| [HOW-TO/](./HOW-TO/README.md) | Setup, build, customizacao, testes |
| [API/](./API/README.md) | Referencia detalhada por componente |

## Status de Implementacao

| Fase | Status | Componentes |
|:-----|:-------|:------------|
| 1. Base | Completo | cn, carfColors, globals.css |
| 2. Form | Completo | Button, Input, Label, Checkbox, Switch, Select, Textarea |
| 3. Layout | Completo | Card, Separator, Tabs, Accordion |
| 4. Feedback | Completo | Alert, Toast, Dialog, AlertDialog, Progress |
| 5. Data Display | Completo | Avatar, Badge, Tooltip, Popover, Table |
| 6. Navigation | Completo | DropdownMenu |
| 7. CARF Domain | Completo | StatusBadge, UnitCard, HolderCard, CommunityCard |

## Referencias

- [Design System CARF](../../../CENTRAL/DESIGN-SYSTEM/README.md) - Tokens e especificacoes
- [shadcn/ui](https://ui.shadcn.com/) - Componentes base
- [Tailwind CSS](https://tailwindcss.com/) - Sistema de estilos
- [Radix UI](https://www.radix-ui.com/) - Primitivos acessiveis

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/ARCHITECTURE/README|ARCHITECTURE]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/CONCEPTS/README|CONCEPTS]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/HOW-TO/README|HOW-TO]]

<!-- CARF-INDEX-END -->
