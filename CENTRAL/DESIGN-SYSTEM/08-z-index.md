---
status: approved
updated: 2026-01-20
---

# Z-Index Scale

Sistema de z-index para gerenciamento de camadas visuais, evitando conflitos e garantindo hierarquia correta de elementos sobrepostos.

## Escala de Z-Index

| Token | Valor | Uso |
|:------|:------|:----|
| `base` | 0 | Conteudo normal, fluxo do documento |
| `dropdown` | 10 | Dropdowns, selects, menus contextuais |
| `sticky` | 20 | Headers fixos, sidebars sticky |
| `modal` | 30 | Modals, dialogs, sheets |
| `popover` | 40 | Tooltips, popovers, hints |
| `toast` | 50 | Notificacoes, toasts, snackbars |

## Aplicacao por Componente

| Componente | Token | Valor |
|:-----------|:------|:------|
| Conteudo pagina | `base` | 0 |
| Dropdown menu | `dropdown` | 10 |
| Select options | `dropdown` | 10 |
| Autocomplete | `dropdown` | 10 |
| Header fixo | `sticky` | 20 |
| Sidebar | `sticky` | 20 |
| Modal | `modal` | 30 |
| Dialog | `modal` | 30 |
| Drawer/Sheet | `modal` | 30 |
| Tooltip | `popover` | 40 |
| Popover | `popover` | 40 |
| Command palette | `popover` | 40 |
| Toast | `toast` | 50 |
| Notification | `toast` | 50 |

## CSS Variables

```css
:root {
  --z-base: 0;
  --z-dropdown: 10;
  --z-sticky: 20;
  --z-modal: 30;
  --z-popover: 40;
  --z-toast: 50;
}
```

## Tailwind Config

```javascript
// tailwind.config.js
zIndex: {
  base: '0',
  dropdown: '10',
  sticky: '20',
  modal: '30',
  popover: '40',
  toast: '50',
}
```

## Exemplos de Uso

```tsx
// Header fixo
<header className="fixed top-0 z-sticky">...</header>

// Dropdown
<ul className="absolute z-dropdown">...</ul>

// Modal com backdrop
<div className="fixed inset-0 z-modal bg-black/50">
  <dialog className="z-modal">...</dialog>
</div>

// Toast container
<div className="fixed bottom-4 right-4 z-toast">...</div>
```

## Regras de Empilhamento

1. **Nunca usar valores arbitrarios** - Sempre usar tokens
2. **Backdrop** - Mesmo z-index do elemento que cobre
3. **Aninhamento** - Elementos filhos herdam contexto do pai
4. **Conflitos** - Resolver via stacking context isolado

## Stacking Context

Criar novo contexto de empilhamento quando necessario:

```css
.isolated-stack {
  isolation: isolate;
}
```

## Hierarquia Visual

```
z-50: Toast/Notifications (sempre visiveis)
  │
z-40: Popover/Tooltip (sobre modais se necessario)
  │
z-30: Modal/Dialog (bloqueia interacao)
  │
z-20: Sticky/Fixed (navegacao)
  │
z-10: Dropdown (menus contextuais)
  │
z-0:  Base content (fluxo normal)
```

## Anti-Patterns

```tsx
// ERRADO - valor arbitrario
<div className="z-[9999]">...</div>

// ERRADO - conflito de camadas
<header className="z-50">  // Toast level para header?
<dialog className="z-10">  // Dropdown level para modal?

// CORRETO
<header className="z-sticky">
<dialog className="z-modal">
```
