---
title: "ADRs - @carf/ui"
description: "Decisoes arquiteturais da biblioteca de componentes React"
status: review
updated: 2026-01-20
source: "interno"
---

# ADRs - @carf/ui

Decisoes arquiteturais que guiam o desenvolvimento da biblioteca de componentes.

## Decisoes Principais

### ADR-001: shadcn/ui como Base

**Status**: Aprovado

**Contexto**: Precisamos de componentes React acessiveis e customizaveis para o ecossistema CARF.

**Decisao**: Usar shadcn/ui como base dos componentes.

**Justificativa**:
- Componentes sao copiados para o projeto (ownership total)
- Baseado em Radix UI (acessibilidade garantida)
- Tailwind CSS para styling (consistente com stack)
- Altamente customizavel
- Sem lock-in de versao

**Consequencias**:
- (+) Controle total sobre o codigo
- (+) Facil customizacao para tema CARF
- (+) Atualizacoes sob demanda
- (-) Responsabilidade de manter componentes atualizados

---

### ADR-002: Radix UI para Primitivos

**Status**: Aprovado

**Contexto**: Componentes interativos precisam ser acessiveis (WCAG 2.1 AA).

**Decisao**: Usar Radix UI como base para todos os componentes interativos.

**Justificativa**:
- Acessibilidade built-in (WAI-ARIA)
- Headless (sem estilos impostos)
- Composable API
- Bem testado e mantido

**Componentes Radix utilizados**:
- Dialog, AlertDialog
- DropdownMenu, Select
- Tabs, Accordion
- Checkbox, Switch
- Toast, Tooltip
- Popover, Avatar
- Progress, Separator

---

### ADR-003: Tailwind CSS para Styling

**Status**: Aprovado

**Contexto**: Precisamos de um sistema de styling consistente e performatico.

**Decisao**: Usar Tailwind CSS com CSS variables para temas.

**Justificativa**:
- Utility-first acelera desenvolvimento
- CSS variables permitem dark mode nativo
- Tree-shaking automatico (bundle pequeno)
- Consistente com WEBDOCS e outros projetos

**Implementacao**:
- CSS variables em `:root` e `.dark`
- `tailwind-merge` para resolver conflitos
- `class-variance-authority` para variantes
- `clsx` para classes condicionais

---

### ADR-004: Storybook para Documentacao

**Status**: Aprovado

**Contexto**: Componentes precisam de documentacao visual interativa.

**Decisao**: Usar Storybook para documentar e testar componentes visualmente.

**Justificativa**:
- Documentacao interativa
- Testes visuais
- Addon de acessibilidade (a11y)
- Deploy estatico facil

---

### ADR-005: Vite para Build

**Status**: Aprovado

**Contexto**: Precisamos de um build rapido e moderno para biblioteca.

**Decisao**: Usar Vite para desenvolvimento e build.

**Justificativa**:
- HMR instantaneo
- ESM nativo
- Build otimizado com Rollup
- Integracao nativa com Storybook

---

## Referencias

- CENTRAL/ADRs/011-ui-component-library.md - Decisao de criar biblioteca de componentes
- CENTRAL/DESIGN-SYSTEM/README.md - Sistema de design CARF

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
