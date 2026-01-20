---
status: approved
updated: 2026-01-20
---

# API Reference - @carf/ui

Referencia completa de componentes, hooks e utilitarios da biblioteca.

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
| Form | [01-form-components.md](01-form-components.md) | Button, Input, Label, Checkbox, Switch, Select, Textarea |
| Layout | [02-layout-components.md](02-layout-components.md) | Card, Separator, Tabs, Accordion |
| Feedback | [03-feedback-components.md](03-feedback-components.md) | Alert, Toast, Dialog, AlertDialog, Progress |
| Data Display | [04-data-display-components.md](04-data-display-components.md) | Avatar, Badge, Tooltip, Popover, Table |
| Navigation | [05-navigation-components.md](05-navigation-components.md) | DropdownMenu |
| CARF Domain | [06-domain-components.md](06-domain-components.md) | StatusBadge, UnitCard, HolderCard, CommunityCard |
| Hooks | [07-hooks.md](07-hooks.md) | useTheme, useMediaQuery, useDebounce |
| Utils | [08-utils.md](08-utils.md) | cn, carfColors, format functions |

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
