---
status: approved
updated: 2026-01-20
---

# Borders

Especificacao de border-radius para consistencia visual em todos os componentes do ecossistema CARF, desde inputs ate modais.

## Border Radius

| Token | Valor | Uso |
|:------|:------|:----|
| `none` | 0 | Elementos quadrados |
| `sm` | 4px | Inputs, badges, chips |
| `DEFAULT` | 8px | Botoes, cards, containers |
| `md` | 12px | Modals, dropdowns, menus |
| `lg` | 16px | Cards destacados, panels |
| `full` | 9999px | Avatares, pills, toggles |

## Aplicacao por Componente

| Componente | Token |
|:-----------|:------|
| Button | `DEFAULT` (8px) |
| Input | `sm` (4px) |
| Card | `DEFAULT` (8px) |
| Modal/Dialog | `md` (12px) |
| Dropdown | `md` (12px) |
| Badge | `sm` (4px) |
| Avatar | `full` |
| Pill/Tag | `full` |
| Tooltip | `sm` (4px) |
| Alert | `DEFAULT` (8px) |

## CSS Variables

```css
:root {
  --radius-none: 0;
  --radius-sm: 4px;
  --radius: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 9999px;
}
```

## Tailwind Config

```javascript
// tailwind.config.js
borderRadius: {
  none: '0',
  sm: 'var(--radius-sm)',      // 4px
  DEFAULT: 'var(--radius)',    // 8px
  md: 'var(--radius-md)',      // 12px
  lg: 'var(--radius-lg)',      // 16px
  full: 'var(--radius-full)',  // 9999px
}
```

## Exemplos de Uso

```tsx
// Botao padrao
<button className="rounded">Submit</button>

// Input com bordas sutis
<input className="rounded-sm" />

// Card
<div className="rounded">...</div>

// Modal
<dialog className="rounded-md">...</dialog>

// Avatar circular
<img className="rounded-full" />
```

## Regras

1. **Consistencia** - Usar tokens, nunca valores arbitrarios
2. **Hierarquia** - Elementos menores usam raios menores
3. **Aninhamento** - Container externo >= filhos internos
4. **Acessibilidade** - Bordas arredondadas facilitam reconhecimento de areas clicaveis
