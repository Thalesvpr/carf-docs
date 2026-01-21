---
status: rejected
description: "Mistura spec com implementacao. Codigo CSS/Tailwind vai para PROJECTS/LIB/TS/UI-COMPONENTS. Aqui so spec abstrata. Contem blocos de codigo."
updated: 2026-01-20
---

# Typography

Sistema tipográfico do CARF definindo família de fontes, escala de tamanhos, pesos e line-heights para garantir legibilidade e hierarquia visual consistente.

## Font Stack

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
             'Helvetica Neue', Arial, 'Noto Sans', sans-serif,
             'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol';
```

Sistema de fontes nativas priorizando performance e consistência com o sistema operacional do usuário.

## Escala de Tamanhos

Baseada em progressão modular para hierarquia clara:

| Token | Tamanho | Line Height | Uso |
|:------|:--------|:------------|:----|
| `xs` | 12px | 16px | Labels menores, captions |
| `sm` | 14px | 20px | Texto secundário, metadata |
| `base` | 16px | 24px | Corpo de texto, parágrafos |
| `lg` | 18px | 28px | Texto destacado, leads |
| `xl` | 20px | 28px | Headings H4 |
| `2xl` | 24px | 32px | Headings H3 |
| `3xl` | 30px | 36px | Headings H2 |
| `4xl` | 36px | 40px | Headings H1 |
| `5xl` | 48px | 48px | Display, hero |

## Pesos

| Token | Valor | Uso |
|:------|:------|:----|
| `normal` | 400 | Corpo de texto |
| `medium` | 500 | Labels, botões |
| `semibold` | 600 | Subheadings, destaques |
| `bold` | 700 | Headings |

## CSS Variables

```css
:root {
  /* Font Family */
  --font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-mono: ui-monospace, 'Cascadia Code', 'Source Code Pro', monospace;

  /* Font Sizes */
  --font-size-xs: 0.75rem;   /* 12px */
  --font-size-sm: 0.875rem;  /* 14px */
  --font-size-base: 1rem;    /* 16px */
  --font-size-lg: 1.125rem;  /* 18px */
  --font-size-xl: 1.25rem;   /* 20px */
  --font-size-2xl: 1.5rem;   /* 24px */
  --font-size-3xl: 1.875rem; /* 30px */
  --font-size-4xl: 2.25rem;  /* 36px */
  --font-size-5xl: 3rem;     /* 48px */

  /* Line Heights */
  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.625;

  /* Font Weights */
  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;
}
```

## Aplicação

### Headings

```css
h1 { font-size: var(--font-size-4xl); font-weight: var(--font-weight-bold); }
h2 { font-size: var(--font-size-3xl); font-weight: var(--font-weight-bold); }
h3 { font-size: var(--font-size-2xl); font-weight: var(--font-weight-semibold); }
h4 { font-size: var(--font-size-xl); font-weight: var(--font-weight-semibold); }
```

### Body

```css
body {
  font-family: var(--font-family);
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
  font-weight: var(--font-weight-normal);
}
```

### Code

```css
code, pre {
  font-family: var(--font-mono);
  font-size: var(--font-size-sm);
}
```

## Responsividade

Headings reduzidos em mobile:

| Breakpoint | H1 | H2 | H3 |
|:-----------|:---|:---|:---|
| Desktop (>768px) | 36px | 30px | 24px |
| Mobile (<768px) | 30px | 24px | 20px |

## Acessibilidade

- Tamanho mínimo de corpo: 16px
- Line-height mínimo: 1.5 para texto corrido
- Contraste adequado (ver [01-colors](01-colors.md))
- Não usar texto todo em maiúsculas para parágrafos
