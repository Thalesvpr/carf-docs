---
status: approved
updated: 2026-01-20
---

# API Reference - @carf/ui

Complete reference for components, hooks and utilities.

## Catalogo por Aplicacao

Mapeamento de quais componentes cada aplicacao do ecossistema CARF utiliza. Componentes marcados como **Essencial** sao necessarios desde o MVP; **Opcional** podem ser adicionados incrementalmente.

### GEOWEB (Portal de Analistas)

| Componente | Prioridade | Uso Principal |
|:-----------|:-----------|:--------------|
| Button | Essencial | Acoes em formularios, toolbar |
| Input | Essencial | Cadastro de unidades/posseiros |
| Select | Essencial | Filtros, selecao de comunidade |
| Table | Essencial | Listagem de unidades, posseiros |
| Card | Essencial | Detalhes de entidades |
| Dialog | Essencial | Edicao, confirmacoes |
| Toast | Essencial | Feedback de acoes |
| Badge | Essencial | Status de legitimacao |
| Tabs | Essencial | Navegacao em detalhes |
| UnitCard | Essencial | Cards na listagem de unidades |
| HolderCard | Essencial | Cards na listagem de posseiros |
| StatusBadge | Essencial | Status de processos REURB |
| DropdownMenu | Opcional | Acoes contextuais |
| Tooltip | Opcional | Hints de campos |
| Avatar | Opcional | Foto de posseiros |
| Accordion | Opcional | Historico de alteracoes |

### ADMIN (Console Administrativo)

| Componente | Prioridade | Uso Principal |
|:-----------|:-----------|:--------------|
| Button | Essencial | Todas as acoes |
| Input | Essencial | Configuracoes, cadastros |
| Table | Essencial | Usuarios, comunidades, logs |
| Card | Essencial | Metricas, dashboards |
| Dialog | Essencial | CRUD de entidades |
| Select | Essencial | Filtros, permissoes |
| Checkbox | Essencial | Permissoes de roles |
| Switch | Essencial | Toggles de features |
| Tabs | Essencial | Configuracoes organizadas |
| Toast | Essencial | Feedback de acoes |
| Badge | Essencial | Status de usuarios |
| CommunityCard | Essencial | Gestao de comunidades |
| DropdownMenu | Opcional | Acoes em tabelas |
| Progress | Opcional | Upload de dados |
| AlertDialog | Opcional | Confirmacao de exclusao |

### REURBCAD Mobile (Aplicativo de Campo)

> Nota: REURBCAD usa React Native, mas componentes de dominio compartilham types.

| Componente | Prioridade | Adaptacao Mobile |
|:-----------|:-----------|:-----------------|
| StatusBadge | Essencial | Adaptar para RN StyleSheet |
| UnitCard | Essencial | Versao RN com TouchableOpacity |
| HolderCard | Essencial | Versao RN simplificada |
| CommunityCard | Essencial | Versao RN |
| carfColors | Essencial | Usar diretamente |
| formatCPF/CNPJ | Essencial | Utils funcionam em RN |

### WebDocs (Portal de Documentacao)

| Componente | Prioridade | Uso Principal |
|:-----------|:-----------|:--------------|
| Button | Opcional | Navegacao, copiar codigo |
| Card | Opcional | Boxes de destaque |
| Tabs | Opcional | Exemplos multi-linguagem |
| Badge | Opcional | Tags de status |
| Accordion | Opcional | FAQ sections |

### Keycloak Theme (Autenticacao)

| Componente | Prioridade | Uso Principal |
|:-----------|:-----------|:--------------|
| Button | Essencial | Submit de login |
| Input | Essencial | Usuario, senha |
| Label | Essencial | Labels de campos |
| Checkbox | Essencial | "Lembrar-me" |
| Card | Essencial | Container do formulario |
| Alert | Essencial | Mensagens de erro |

## Documentacao por Categoria

| Categoria | Arquivo | Componentes |
|:----------|:--------|:------------|
| Form | 01-form-components | Button, Input, Label, Checkbox, Switch, Select, Textarea |
| Layout | 02-layout-components | Card, Separator, Tabs, Accordion, ScrollArea |
| Feedback | 03-feedback-components | Alert, Toast, Dialog, AlertDialog, Progress, Skeleton |
| Data Display | 04-data-components | Avatar, Badge, Tooltip, Popover, Table, HoverCard |
| Navigation | 05-navigation-components | DropdownMenu, Command, Breadcrumb, NavigationMenu, Pagination |
| CARF Domain | 06-domain-components | StatusBadge, UnitCard, HolderCard, CommunityCard |
| Hooks | 07-hooks | useTheme, useMediaQuery, useDebounce, useLocalStorage, useCopyToClipboard |
| Utils | 08-utils | cn, cva, formatters, validators, helpers |

## Dependencias

```
@carf/ui
├── @radix-ui/* (primitivos acessiveis)
├── class-variance-authority (variants)
├── clsx + tailwind-merge (cn utility)
├── tailwindcss (estilos)
└── @carf/tscore (types para domain components) [opcional]
```

A dependencia de `@carf/tscore` e **opcional**: componentes de dominio (UnitCard, HolderCard, etc) definem seus proprios types localmente, mas podem aceitar types de tscore via generics para integracao completa.

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/01-form-components.md|Form Components]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/02-layout-components.md|Layout Components - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/03-feedback-components.md|Feedback Components - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/04-data-components.md|Data Components - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/05-navigation-components.md|Navigation Components - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/06-domain-components.md|Domain Components]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/07-hooks.md|Hooks - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/08-utils.md|Utils - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/API/09-screen-mapping.md|Mapeamento Tela-Componentes]]

<!-- CARF-INDEX-END -->
