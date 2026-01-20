---
status: approved
updated: 2026-01-20
---

# Breakpoints

Sistema de breakpoints responsivos para garantir experiencia consistente em todos os dispositivos, desde mobile ate monitores ultrawide.

## Escala de Breakpoints

| Token | Valor | Dispositivo | Uso |
|:------|:------|:------------|:----|
| `sm` | 640px | Mobile landscape | Smartphones em paisagem |
| `md` | 768px | Tablet | Tablets em retrato |
| `lg` | 1024px | Desktop | Laptops, desktops |
| `xl` | 1280px | Desktop wide | Monitores grandes |
| `2xl` | 1536px | Ultrawide | Monitores ultrawide |

## Container Widths

| Breakpoint | Container Max |
|:-----------|:--------------|
| Default | 100% |
| `sm` | 640px |
| `md` | 768px |
| `lg` | 1024px |
| `xl` | 1280px |
| `2xl` | 1400px |

## CSS Variables

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}
```

## Media Queries

```css
/* Mobile first approach */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
@media (min-width: 1536px) { /* 2xl */ }
```

## Tailwind Config

```javascript
// tailwind.config.js
screens: {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  '2xl': '1536px',
},
container: {
  center: true,
  padding: {
    DEFAULT: '1rem',
    sm: '2rem',
    lg: '4rem',
    xl: '5rem',
    '2xl': '6rem',
  },
},
```

## Exemplos de Uso

```tsx
// Grid responsivo
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
  ...
</div>

// Sidebar responsiva
<aside className="hidden lg:block w-64">...</aside>
<main className="lg:ml-64">...</main>

// Tipografia responsiva
<h1 className="text-2xl md:text-3xl lg:text-4xl">...</h1>

// Espacamento responsivo
<section className="p-4 md:p-6 lg:p-8">...</section>
```

## Estrategia Mobile-First

1. **Base** - Estilos para mobile (< 640px)
2. **sm** - Ajustes para mobile landscape
3. **md** - Layout tablet (sidebar opcional)
4. **lg** - Layout desktop completo
5. **xl/2xl** - Otimizacoes para telas grandes

## Layouts por Breakpoint

### Mobile (< 640px)
- Navegacao em bottom bar ou hamburger
- Conteudo em coluna unica
- Cards em stack vertical

### Tablet (md: 768px)
- Grid 2 colunas
- Sidebar colapsavel
- Navegacao em top bar

### Desktop (lg: 1024px)
- Sidebar fixa
- Grid multi-coluna
- Todas features visiveis

### Wide (xl: 1280px+)
- Conteudo centralizado com max-width
- Espacamento aumentado
- Tipografia maior opcional
