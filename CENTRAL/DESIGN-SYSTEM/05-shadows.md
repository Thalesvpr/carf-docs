---
status: approved
updated: 2026-01-20
---

# Shadows

Sistema de elevacao visual usando sombras para hierarquia de interface, indicando profundidade e foco de elementos no ecossistema CARF.

## Escala de Elevacao

| Token | Valor | Uso |
|:------|:------|:----|
| `none` | none | Elementos flat, inline |
| `sm` | 0 1px 2px rgba(0,0,0,0.05) | Inputs, buttons em repouso |
| `DEFAULT` | 0 4px 6px rgba(0,0,0,0.1) | Cards, containers |
| `md` | 0 6px 12px rgba(0,0,0,0.15) | Dropdowns, menus flutuantes |
| `lg` | 0 10px 25px rgba(0,0,0,0.2) | Modals, dialogs |
| `xl` | 0 20px 40px rgba(0,0,0,0.25) | Overlays criticos |

## Aplicacao por Componente

| Componente | Token | Elevacao |
|:-----------|:------|:---------|
| Card | `DEFAULT` | Nivel 1 |
| Button (hover) | `sm` | Nivel 0.5 |
| Dropdown | `md` | Nivel 2 |
| Tooltip | `md` | Nivel 2 |
| Modal | `lg` | Nivel 3 |
| Toast | `lg` | Nivel 3 |
| Command Palette | `xl` | Nivel 4 |

## CSS Variables

```css
:root {
  --shadow-none: none;
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 6px 12px rgba(0, 0, 0, 0.15);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.2);
  --shadow-xl: 0 20px 40px rgba(0, 0, 0, 0.25);
}
```

## Tailwind Config

```javascript
// tailwind.config.js
boxShadow: {
  none: 'var(--shadow-none)',
  sm: 'var(--shadow-sm)',
  DEFAULT: 'var(--shadow)',
  md: 'var(--shadow-md)',
  lg: 'var(--shadow-lg)',
  xl: 'var(--shadow-xl)',
}
```

## Exemplos de Uso

```tsx
// Card padrao
<div className="shadow rounded">...</div>

// Dropdown flutuante
<ul className="shadow-md rounded-md">...</ul>

// Modal
<dialog className="shadow-lg rounded-md">...</dialog>

// Button com hover
<button className="hover:shadow-sm transition-shadow">...</button>
```

## Regras de Hierarquia

1. **Elementos base** - Sem sombra ou `sm`
2. **Containers** - `DEFAULT`
3. **Elementos flutuantes** - `md`
4. **Overlays modais** - `lg` ou `xl`
5. **Transicoes** - Sombras devem animar suavemente (200ms)

## Dark Mode

Em modo escuro, sombras sao menos visiveis. Usar bordas sutis como complemento:

```css
.dark {
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 6px 12px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.5);
}
```
