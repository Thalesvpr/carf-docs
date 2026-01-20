---
status: approved
updated: 2026-01-20
---

# Transitions

Sistema de transicoes e animacoes para feedback visual fluido e consistente em todos os componentes do ecossistema CARF.

## Duracao

| Token | Valor | Uso |
|:------|:------|:----|
| `fast` | 150ms | Hover, focus, micro-interacoes |
| `DEFAULT` | 200ms | Maioria das transicoes |
| `slow` | 300ms | Modais, acordeoes, expansoes |
| `slower` | 500ms | Animacoes de entrada de pagina |

## Easing (Timing Functions)

| Token | Valor | Uso |
|:------|:------|:----|
| `DEFAULT` | cubic-bezier(0.4, 0, 0.2, 1) | Movimento natural |
| `in` | cubic-bezier(0.4, 0, 1, 1) | Entrada (aceleracao) |
| `out` | cubic-bezier(0, 0, 0.2, 1) | Saida (desaceleracao) |
| `in-out` | cubic-bezier(0.4, 0, 0.2, 1) | Entrada e saida |

## Propriedades Animaveis

| Propriedade | Duracao | Easing |
|:------------|:--------|:-------|
| `opacity` | fast | out |
| `transform` | DEFAULT | DEFAULT |
| `background-color` | fast | out |
| `border-color` | fast | out |
| `box-shadow` | DEFAULT | out |
| `height/width` | slow | DEFAULT |
| `color` | fast | out |

## CSS Variables

```css
:root {
  /* Duracoes */
  --duration-fast: 150ms;
  --duration-default: 200ms;
  --duration-slow: 300ms;
  --duration-slower: 500ms;

  /* Easings */
  --ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}
```

## Tailwind Config

```javascript
// tailwind.config.js
transitionDuration: {
  fast: '150ms',
  DEFAULT: '200ms',
  slow: '300ms',
  slower: '500ms',
},
transitionTimingFunction: {
  DEFAULT: 'cubic-bezier(0.4, 0, 0.2, 1)',
  in: 'cubic-bezier(0.4, 0, 1, 1)',
  out: 'cubic-bezier(0, 0, 0.2, 1)',
  'in-out': 'cubic-bezier(0.4, 0, 0.2, 1)',
},
```

## Exemplos de Uso

```tsx
// Hover em button
<button className="transition-colors duration-fast hover:bg-opacity-90">

// Card com shadow transition
<div className="transition-shadow duration-default hover:shadow-md">

// Accordion expand
<div className="transition-[height] duration-slow ease-default">

// Modal fade in
<dialog className="transition-opacity duration-default ease-out">

// All transitions
<div className="transition-all duration-default">
```

## Aplicacao por Componente

| Componente | Propriedades | Duracao |
|:-----------|:-------------|:--------|
| Button | colors, transform | fast |
| Input | border-color, shadow | fast |
| Card | shadow | DEFAULT |
| Modal | opacity, transform | DEFAULT |
| Accordion | height | slow |
| Dropdown | opacity, transform | DEFAULT |
| Toast | opacity, transform | DEFAULT |
| Tooltip | opacity | fast |

## Keyframes Comuns

```css
/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide up */
@keyframes slideUp {
  from { transform: translateY(10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Scale in */
@keyframes scaleIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

/* Accordion down */
@keyframes accordionDown {
  from { height: 0; }
  to { height: var(--radix-accordion-content-height); }
}
```

## Reducao de Movimento

Respeitar preferencias do usuario:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
// Tailwind
<div className="motion-safe:transition-all motion-reduce:transition-none">
```

## Regras

1. **Consistencia** - Usar tokens, nunca valores arbitrarios
2. **Performance** - Preferir transform e opacity (GPU accelerated)
3. **Proposito** - Animacoes devem ter funcao, nao apenas decoracao
4. **Acessibilidade** - Respeitar prefers-reduced-motion
5. **Duracao** - Rapidas para feedback, lentas para atencao
