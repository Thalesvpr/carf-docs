---
title: "Globals CSS - @carf/ui"
status: review
updated: 2026-01-21
source: "CENTRAL/DESIGN-SYSTEM/README.md"
---

# Globals CSS - @carf/ui

CSS variables e estilos base para o tema CARF.

## globals.css

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* ============================================
   CSS VARIABLES - TEMA CARF
   ============================================ */

@layer base {
  :root {
    /* Background e foreground */
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;

    /* Card */
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;

    /* Popover */
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;

    /* Primary - Verde CARF */
    --primary: 121 37% 27%;
    --primary-foreground: 0 0% 98%;

    /* Secondary */
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;

    /* Muted */
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;

    /* Accent */
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;

    /* Destructive */
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;

    /* Border e Input */
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;

    /* Ring (focus) */
    --ring: 121 37% 27%;

    /* Border radius */
    --radius: 0.5rem;
  }

  .dark {
    /* Background e foreground - Dark */
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;

    /* Card - Dark */
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;

    /* Popover - Dark */
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    /* Primary - Dark */
    --primary: 121 37% 40%;
    --primary-foreground: 0 0% 98%;

    /* Secondary - Dark */
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    /* Muted - Dark */
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;

    /* Accent - Dark */
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;

    /* Destructive - Dark */
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    /* Border e Input - Dark */
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;

    /* Ring - Dark */
    --ring: 121 37% 50%;
  }
}

/* ============================================
   ESTILOS BASE
   ============================================ */

@layer base {
  * {
    @apply border-border;
  }

  body {
    @apply bg-background text-foreground;
    font-feature-settings: "rlig" 1, "calt" 1;
  }

  /* Focus visible */
  :focus-visible {
    @apply outline-none ring-2 ring-ring ring-offset-2 ring-offset-background;
  }

  /* Scrollbar customizada */
  ::-webkit-scrollbar {
    width: 8px;
    height: 8px;
  }

  ::-webkit-scrollbar-track {
    @apply bg-muted rounded-full;
  }

  ::-webkit-scrollbar-thumb {
    @apply bg-muted-foreground/30 rounded-full;
  }

  ::-webkit-scrollbar-thumb:hover {
    @apply bg-muted-foreground/50;
  }

  /* Selection */
  ::selection {
    @apply bg-primary/20 text-foreground;
  }
}

/* ============================================
   COMPONENTES UTILITARIOS
   ============================================ */

@layer components {
  /* Container padrao */
  .container-carf {
    @apply container mx-auto px-4 sm:px-6 lg:px-8;
  }

  /* Card padrao */
  .card-carf {
    @apply bg-card text-card-foreground rounded-lg border shadow-card;
  }

  .card-carf:hover {
    @apply shadow-card-hover;
  }

  /* Input padrao */
  .input-carf {
    @apply flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm;
    @apply ring-offset-background;
    @apply file:border-0 file:bg-transparent file:text-sm file:font-medium;
    @apply placeholder:text-muted-foreground;
    @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2;
    @apply disabled:cursor-not-allowed disabled:opacity-50;
  }

  /* Button base */
  .btn-carf {
    @apply inline-flex items-center justify-center rounded-md text-sm font-medium;
    @apply ring-offset-background transition-colors;
    @apply focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2;
    @apply disabled:pointer-events-none disabled:opacity-50;
  }

  /* Link */
  .link-carf {
    @apply text-primary underline-offset-4 hover:underline;
  }
}

/* ============================================
   UTILITARIOS ADICIONAIS
   ============================================ */

@layer utilities {
  /* Truncate com ellipsis */
  .truncate-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .truncate-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  /* Safe area padding (mobile) */
  .safe-top {
    padding-top: env(safe-area-inset-top);
  }

  .safe-bottom {
    padding-bottom: env(safe-area-inset-bottom);
  }

  /* Hide scrollbar */
  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }

  /* Backdrop blur fallback */
  .backdrop-blur-carf {
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
  }

  /* Print utilities */
  @media print {
    .print-hidden {
      display: none !important;
    }

    .print-only {
      display: block !important;
    }
  }
}

/* ============================================
   FONTES
   ============================================ */

/* Inter - fonte principal */
@font-face {
  font-family: 'Inter';
  font-style: normal;
  font-weight: 100 900;
  font-display: swap;
  src: url('/fonts/inter-var.woff2') format('woff2');
}

/* JetBrains Mono - codigo */
@font-face {
  font-family: 'JetBrains Mono';
  font-style: normal;
  font-weight: 400 700;
  font-display: swap;
  src: url('/fonts/jetbrains-mono-var.woff2') format('woff2');
}
```

## Uso em Projetos Consumidores

### Importar CSS

```tsx
// app.tsx ou _app.tsx (Next.js)
import '@carf/ui/globals.css'

// ou em CSS
@import '@carf/ui/globals.css';
```

### Customizar Variaveis

Para customizar o tema, sobrescreva as CSS variables:

```css
/* styles/custom-theme.css */
:root {
  /* Mudar cor primary para azul */
  --primary: 210 100% 50%;

  /* Mudar radius */
  --radius: 0.75rem;
}
```

### Dark Mode

O dark mode e ativado pela classe `.dark` no elemento root:

```html
<!-- Light mode -->
<html>
  <body>...</body>
</html>

<!-- Dark mode -->
<html class="dark">
  <body>...</body>
</html>
```

Para alternar dinamicamente:

```typescript
function toggleDarkMode() {
  document.documentElement.classList.toggle('dark')
}
```
