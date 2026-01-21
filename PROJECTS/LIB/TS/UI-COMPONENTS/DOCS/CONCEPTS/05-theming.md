---
title: "Theming - @carf/ui"
status: review
updated: 2026-01-21
source: "CENTRAL/DESIGN-SYSTEM/README.md"
---

# Theming - @carf/ui

Sistema de temas baseado em CSS variables para suporte a light/dark mode.

## Arquitetura do Tema

### CSS Variables

O tema usa HSL (Hue, Saturation, Lightness) para flexibilidade:

```css
:root {
  /* Formato: H S% L% (sem virgulas para compatibilidade Tailwind) */
  --primary: 121 37% 27%;
  --primary-foreground: 0 0% 98%;
}
```

### Uso no Tailwind

```javascript
// tailwind.config.js
colors: {
  primary: {
    DEFAULT: 'hsl(var(--primary))',
    foreground: 'hsl(var(--primary-foreground))',
  }
}
```

```html
<!-- Uso em componentes -->
<button class="bg-primary text-primary-foreground">
  Botao
</button>
```

## Paleta de Cores

### Cores Semanticas

| Variable | Light Mode | Dark Mode | Uso |
|:---------|:-----------|:----------|:----|
| `--background` | #ffffff | #0a0a0a | Fundo da pagina |
| `--foreground` | #0a0a0a | #fafafa | Texto principal |
| `--card` | #ffffff | #0a0a0a | Fundo de cards |
| `--card-foreground` | #0a0a0a | #fafafa | Texto em cards |
| `--primary` | #2C5F2D | #3d7a3e | Acoes principais |
| `--primary-foreground` | #fafafa | #fafafa | Texto em primary |
| `--secondary` | #f4f4f5 | #27272a | Acoes secundarias |
| `--muted` | #f4f4f5 | #27272a | Fundos sutis |
| `--accent` | #f4f4f5 | #27272a | Highlights |
| `--destructive` | #ef4444 | #7f1d1d | Acoes destrutivas |

### Cores de Marca CARF

```css
/* Sempre disponiveis, independente do tema */
--carf-primary: #2C5F2D;      /* Verde principal */
--carf-secondary: #97BC62;    /* Verde claro */
--carf-accent: #E63946;       /* Vermelho destaque */
```

### Cores de Status

```css
--success: #15981C;
--warning: #FFCD07;
--error: #E63946;
--info: #3872C6;
```

## Implementando Dark Mode

### 1. Ativar Dark Mode

```html
<!-- Adicionar classe 'dark' no html -->
<html class="dark">
  <body>...</body>
</html>
```

### 2. Toggle Programatico

```typescript
// hooks/use-theme.ts
import { useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

export function useTheme() {
  const [theme, setTheme] = useState<Theme>('system')

  useEffect(() => {
    const root = document.documentElement

    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
      root.classList.toggle('dark', systemTheme === 'dark')
    } else {
      root.classList.toggle('dark', theme === 'dark')
    }
  }, [theme])

  return { theme, setTheme }
}
```

### 3. Persistencia

```typescript
// Salvar preferencia
function useThemeWithPersistence() {
  const [theme, setTheme] = useState<Theme>(() => {
    if (typeof window === 'undefined') return 'system'
    return (localStorage.getItem('theme') as Theme) || 'system'
  })

  useEffect(() => {
    localStorage.setItem('theme', theme)
  }, [theme])

  // ... resto da logica
}
```

### 4. Evitar Flash (SSR)

```html
<!-- Adicionar no <head> antes do CSS -->
<script>
  (function() {
    const theme = localStorage.getItem('theme')
    if (theme === 'dark' ||
        (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark')
    }
  })()
</script>
```

## Customizando o Tema

### Sobrescrever Variaveis

```css
/* styles/custom-theme.css */
:root {
  /* Mudar primary para azul */
  --primary: 210 100% 50%;
  --primary-foreground: 0 0% 100%;

  /* Ajustar radius */
  --radius: 0.75rem;
}

.dark {
  --primary: 210 100% 60%;
}
```

### Temas por Contexto

```css
/* Tema para area administrativa */
.theme-admin {
  --primary: 220 90% 45%;
  --accent: 45 100% 50%;
}

/* Tema para portal publico */
.theme-public {
  --primary: 121 37% 27%;
  --accent: 80 60% 45%;
}
```

```html
<div class="theme-admin">
  <!-- Componentes usam cores admin -->
</div>
```

## Componente ThemeProvider

```tsx
// components/theme-provider.tsx
import { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark' | 'system'

interface ThemeContextValue {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined)

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  storageKey = 'carf-theme'
}: {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}) {
  const [theme, setTheme] = useState<Theme>(defaultTheme)
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    const stored = localStorage.getItem(storageKey) as Theme
    if (stored) setTheme(stored)
  }, [storageKey])

  useEffect(() => {
    const root = document.documentElement

    let resolved: 'light' | 'dark'
    if (theme === 'system') {
      resolved = window.matchMedia('(prefers-color-scheme: dark)').matches
        ? 'dark'
        : 'light'
    } else {
      resolved = theme
    }

    root.classList.remove('light', 'dark')
    root.classList.add(resolved)
    setResolvedTheme(resolved)
    localStorage.setItem(storageKey, theme)
  }, [theme, storageKey])

  return (
    <ThemeContext.Provider value={{ theme, setTheme, resolvedTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider')
  }
  return context
}
```

## Uso em Componentes

### Estilos Responsivos ao Tema

```tsx
// Automatico via CSS variables
<div className="bg-background text-foreground">
  Automaticamente muda com o tema
</div>

// Classes condicionais dark:
<div className="bg-white dark:bg-gray-900">
  Estilos especificos por tema
</div>
```

### Acessando Tema Programaticamente

```tsx
function MyComponent() {
  const { resolvedTheme, setTheme } = useTheme()

  return (
    <button onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}>
      {resolvedTheme === 'dark' ? '☀️' : '🌙'}
    </button>
  )
}
```

## Acessibilidade

### Contraste

Todas as combinacoes de cores garantem contraste minimo WCAG AA:
- Texto normal: 4.5:1
- Texto grande: 3:1
- Elementos UI: 3:1

### Preferencias do Usuario

```css
/* Respeitar preferencia de movimento reduzido */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}

/* Respeitar preferencia de alto contraste */
@media (prefers-contrast: high) {
  :root {
    --border: 0 0% 0%;
  }
}
```
