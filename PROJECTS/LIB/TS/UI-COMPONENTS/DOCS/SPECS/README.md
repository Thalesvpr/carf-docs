---
title: "Especificacoes Tecnicas - @carf/ui"
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
status: rejected
updated: 2026-01-22
source: "interno"
---

# Especificacoes Tecnicas - @carf/ui

Documentacao tecnica detalhada das configuracoes de projeto necessarias para build, desenvolvimento e publicacao da biblioteca de componentes.

## Documentos

| ID | Titulo | Descricao |
|:---|:-------|:----------|
| 01-package-json | Package.json | Dependencias, exports e configuracao npm |
| 02-tailwind-config | Tailwind Config | Configuracao Tailwind com tema CARF |
| 03-globals-css | Globals CSS | CSS variables e tema base |
| 04-storybook-config | Storybook | Configuracao do Storybook |

## Visao Geral

O @carf/ui e configurado para:

- **Build**: Vite + TypeScript
- **Styling**: Tailwind CSS + CSS Variables
- **Componentes Base**: shadcn/ui + Radix UI
- **Documentacao**: Storybook
- **Publicacao**: GitHub Packages (@carf scope)

## Requisitos de Ambiente

```bash
# Versoes minimas
node >= 18.0.0
bun >= 1.0.0
```

## Comandos Principais

```bash
# Instalar dependencias
bun install

# Build da biblioteca
bun run build

# Storybook (desenvolvimento)
bun run storybook

# Testes
bun test

# Type check
tsc --noEmit
```

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/SPECS/01-package-json.md|Package.json - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/SPECS/02-tailwind-config.md|Tailwind Config - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/SPECS/03-globals-css.md|Globals CSS - @carf/ui]]
- ○ [[PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/SPECS/04-storybook-config.md|Storybook Config - @carf/ui]]

<!-- CARF-INDEX-END -->
