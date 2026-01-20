---
status: approved
updated: 2026-01-20
---

# Interactive States

Especificacao de estados visuais interativos para garantir feedback consistente em todos os componentes do ecossistema CARF.

## Focus State

Estado de foco para acessibilidade via teclado:

| Propriedade | Valor |
|:------------|:------|
| Ring width | 2px |
| Ring color | var(--color-blue) `#3872C6` |
| Ring offset | 2px |
| Outline | none (substituido por ring) |

```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px white, 0 0 0 4px var(--color-blue);
}
```

## Disabled State

Estado desabilitado para elementos inativos:

| Propriedade | Valor |
|:------------|:------|
| Opacity | 0.5 |
| Cursor | not-allowed |
| Pointer events | none |
| Hover effects | Desabilitados |
| Focus effects | Desabilitados |

```css
:disabled,
[aria-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
```

## Hover State

Feedback visual ao passar o mouse:

| Componente | Efeito |
|:-----------|:-------|
| Button primary | Background escurece 10% |
| Button secondary | Background sutil |
| Link | Underline, cor escurece |
| Card | Elevacao aumenta (shadow) |
| Row/Item | Background sutil |

## Active/Pressed State

Feedback ao clicar/pressionar:

| Propriedade | Valor |
|:------------|:------|
| Transform | scale(0.98) |
| Background | Escurece 15% |
| Transition | 100ms |

## Error State

Indicador de erro ou validacao falha:

| Propriedade | Valor |
|:------------|:------|
| Border color | var(--color-accent) `#E63946` |
| Text color | var(--color-accent) `#E63946` |
| Icon | Exclamation circle |
| Background | rgba(230, 57, 70, 0.05) |

```css
[aria-invalid="true"],
.error {
  border-color: var(--color-accent);
  color: var(--color-accent);
}
```

## Loading State

Indicador de carregamento:

| Propriedade | Valor |
|:------------|:------|
| Opacity content | 0.7 |
| Cursor | wait |
| Spinner | Animacao circular |

## CSS Variables

```css
:root {
  /* Focus */
  --ring-width: 2px;
  --ring-color: var(--color-blue);
  --ring-offset: 2px;

  /* Disabled */
  --disabled-opacity: 0.5;

  /* Error */
  --error-color: var(--color-accent);
  --error-bg: rgba(230, 57, 70, 0.05);

  /* Hover */
  --hover-opacity: 0.9;
  --hover-bg-subtle: rgba(0, 0, 0, 0.05);
}
```

## Tailwind Classes

```tsx
// Focus ring
<button className="focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2">

// Disabled
<button disabled className="disabled:opacity-50 disabled:cursor-not-allowed">

// Error input
<input className="border-red-500 focus:ring-red-500" aria-invalid="true" />

// Hover card
<div className="hover:shadow-md transition-shadow">

// Active button
<button className="active:scale-[0.98] transition-transform">
```

## Aplicacao por Componente

| Componente | Focus | Hover | Active | Disabled |
|:-----------|:------|:------|:-------|:---------|
| Button | Ring | Bg darker | Scale | Opacity 0.5 |
| Input | Ring | Border color | - | Opacity 0.5 |
| Checkbox | Ring | Bg subtle | Scale | Opacity 0.5 |
| Link | Underline | Color darker | - | Opacity 0.5 |
| Card | - | Shadow up | - | Opacity 0.5 |
| Row | - | Bg subtle | Bg darker | Opacity 0.5 |

## Acessibilidade

1. **Focus visivel** - Sempre mostrar indicador de foco para navegacao por teclado
2. **Contraste** - Estados devem manter ratio minimo WCAG AA
3. **Nao depender de cor** - Usar multiplos indicadores (cor + icone + texto)
4. **ARIA states** - Usar atributos aria-disabled, aria-invalid, etc.
