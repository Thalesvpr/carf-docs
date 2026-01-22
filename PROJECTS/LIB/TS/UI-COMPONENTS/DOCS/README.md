---
title: "Documentacao @carf/ui"
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
status: rejected
updated: 2026-01-22
source: "interno"
---

# Documentacao @carf/ui

Documentacao tecnica da biblioteca de componentes React baseada em shadcn/ui e Tailwind CSS.

> **Status: Especificado (Nao Implementado)**
>
> Esta documentacao especifica a API completa. A implementacao seguira estas especificacoes.

## Secoes

| Secao | Descricao |
|:------|:----------|
| [SPECS/](./SPECS/README.md) | Especificacoes tecnicas (package.json, tailwind, CSS) |
| [ADRs/](./ADRs/README.md) | Decisoes arquiteturais |
| [ARCHITECTURE/](./ARCHITECTURE/README.md) | Arquitetura e patterns |
| [CONCEPTS/](./CONCEPTS/README.md) | Conceitos fundamentais |
| [API/](./API/README.md) | Referencia de API por componente |
| [HOW-TO/](./HOW-TO/README.md) | Guias praticos |

## Componentes Especificados

### Form (7)
Button, Input, Label, Checkbox, Switch, Select, Textarea

### Layout (4)
Card, Separator, Tabs, Accordion

### Feedback (5)
Alert, Toast, Dialog, AlertDialog, Progress

### Data Display (5)
Avatar, Badge, Tooltip, Popover, Table

### Navigation (1)
DropdownMenu

### CARF Domain (4)
StatusBadge, UnitCard, HolderCard, CommunityCard

## Hooks

| Hook | Descricao |
|:-----|:----------|
| useTheme | Gerenciamento de tema (light/dark/system) |
| useMediaQuery | Query responsiva |
| useDebounce | Debounce de valores |
| useLocalStorage | Persistencia local |
| useCopyToClipboard | Copiar para clipboard |

## Utils

| Funcao | Descricao |
|:-------|:----------|
| cn() | Merge de classes Tailwind |
| formatCPF() | Formata CPF |
| formatCNPJ() | Formata CNPJ |
| formatPhone() | Formata telefone |
| formatCurrency() | Formata moeda |
| formatDate() | Formata data |

## Status de Especificacao

| Secao | Arquivos | Status |
|:------|:---------|:-------|
| SPECS | 5 | Completo |
| ADRs | 1 | Completo |
| ARCHITECTURE | 5 | Existente |
| CONCEPTS | 4 | Completo |
| API | 9 | Completo |
| HOW-TO | 4 | Existente |

## Referencias

- [README principal](../README.md) - Visao geral da biblioteca
- CENTRAL/DESIGN-SYSTEM/README.md - Tokens e sistema de design
- [shadcn/ui](https://ui.shadcn.com/) - Componentes base

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/ARCHITECTURE/README|ARCHITECTURE]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/COMPONENTS/README|COMPONENTS]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/CONCEPTS/README|CONCEPTS]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/HOW-TO/README|HOW-TO]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/SPECS/README|SPECS]]

<!-- CARF-INDEX-END -->
