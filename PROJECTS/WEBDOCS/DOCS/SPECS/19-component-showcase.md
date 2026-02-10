---
type: leaf
status: review
updated: 2026-02-07
---

# Component Showcase

Galeria de componentes @carf/ui em /dev/components/ para desenvolvedores (role dev). Inspirada em material.io/components e ui.shadcn.com.

## Categorias

| Categoria | Componentes |
|-----------|-------------|
| Acoes | Button, IconButton, FAB |
| Inputs | Input, Textarea, Select, Checkbox, Radio, Switch, Slider |
| Navegacao | Tabs, Breadcrumb, Pagination, DropdownMenu |
| Feedback | Toast, Alert, Progress, Skeleton, Spinner |
| Overlays | Dialog, Sheet, Popover, Tooltip |
| Layout | Card, Separator, Accordion, Collapsible |
| Data Display | Table, Badge, Avatar |

## Estrutura de Pagina

Cada componente segue estrutura: header com titulo e link fonte, demo interativa com toggle de variantes, installation com import, usage basico e com hidratacao Astro, variants em grid visual, props em tabela (Nome/Tipo/Default/Descricao), accessibility com ARIA e teclado, examples com uso real no CARF.

## Componentes de Documentacao

ComponentDemo em src/components/docs/ComponentDemo.astro com live preview, code display, copy button e variant switcher. PropsTable em src/components/docs/PropsTable.astro exibe tabela de props.

## Geracao e Tokens

Props extraidos automaticamente da @carf/ui (interfaces, JSDoc, defaults). Pagina /dev/components/tokens documenta cores, tipografia, spacing, borders, shadows e breakpoints.

## Source e Storybook

Source segue pattern PROJECTS/LIB/TS/UI/src/components/Component/index.tsx. Demos podem usar Storybook embeddado via iframe como alternativa a componentes Astro nativos.
