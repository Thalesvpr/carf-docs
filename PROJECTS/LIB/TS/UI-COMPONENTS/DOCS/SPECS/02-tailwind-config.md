---
title: "Tailwind Config - @carf/ui"
status: review
updated: 2026-01-21
source: "CENTRAL/DESIGN-SYSTEM/README.md"
---

# Tailwind Config - @carf/ui

Configuracao Tailwind CSS com tema CARF completo.

## tailwind.config.js

```javascript
const { fontFamily } = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ['class'],
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: '2rem',
      screens: {
        '2xl': '1400px',
      },
    },
    extend: {
      // ============================================
      // CORES CARF
      // ============================================
      colors: {
        // Cores de marca
        carf: {
          primary: {
            DEFAULT: '#2C5F2D',
            50: '#E8F5E9',
            100: '#C8E6C9',
            200: '#A5D6A7',
            300: '#81C784',
            400: '#66BB6A',
            500: '#2C5F2D',
            600: '#255025',
            700: '#1E401E',
            800: '#173017',
            900: '#102010',
          },
          secondary: {
            DEFAULT: '#97BC62',
            light: '#B8D98C',
            dark: '#7A9E4F',
          },
          accent: {
            DEFAULT: '#E63946',
            light: '#FF6B6B',
            dark: '#C92A36',
          },
        },

        // Cores semanticas (usam CSS variables)
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))',
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))',
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))',
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))',
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))',
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))',
        },
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))',
        },

        // Status
        success: {
          DEFAULT: '#15981C',
          light: '#4ADE80',
          dark: '#166534',
        },
        warning: {
          DEFAULT: '#FFCD07',
          light: '#FEF08A',
          dark: '#CA8A04',
        },
        error: {
          DEFAULT: '#E63946',
          light: '#FCA5A5',
          dark: '#B91C1C',
        },
        info: {
          DEFAULT: '#3872C6',
          light: '#93C5FD',
          dark: '#1E40AF',
        },
      },

      // ============================================
      // TIPOGRAFIA
      // ============================================
      fontFamily: {
        sans: ['Inter', ...fontFamily.sans],
        mono: ['JetBrains Mono', ...fontFamily.mono],
      },
      fontSize: {
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },

      // ============================================
      // ESPACAMENTO
      // ============================================
      spacing: {
        '4.5': '1.125rem',
        '18': '4.5rem',
      },

      // ============================================
      // BORDAS
      // ============================================
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)',
      },

      // ============================================
      // ANIMACOES
      // ============================================
      keyframes: {
        'accordion-down': {
          from: { height: '0' },
          to: { height: 'var(--radix-accordion-content-height)' },
        },
        'accordion-up': {
          from: { height: 'var(--radix-accordion-content-height)' },
          to: { height: '0' },
        },
        'fade-in': {
          from: { opacity: '0' },
          to: { opacity: '1' },
        },
        'fade-out': {
          from: { opacity: '1' },
          to: { opacity: '0' },
        },
        'slide-in-from-top': {
          from: { transform: 'translateY(-100%)' },
          to: { transform: 'translateY(0)' },
        },
        'slide-in-from-bottom': {
          from: { transform: 'translateY(100%)' },
          to: { transform: 'translateY(0)' },
        },
        'slide-in-from-left': {
          from: { transform: 'translateX(-100%)' },
          to: { transform: 'translateX(0)' },
        },
        'slide-in-from-right': {
          from: { transform: 'translateX(100%)' },
          to: { transform: 'translateX(0)' },
        },
        'spin': {
          from: { transform: 'rotate(0deg)' },
          to: { transform: 'rotate(360deg)' },
        },
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out',
        'fade-in': 'fade-in 0.2s ease-out',
        'fade-out': 'fade-out 0.2s ease-out',
        'slide-in-from-top': 'slide-in-from-top 0.3s ease-out',
        'slide-in-from-bottom': 'slide-in-from-bottom 0.3s ease-out',
        'slide-in-from-left': 'slide-in-from-left 0.3s ease-out',
        'slide-in-from-right': 'slide-in-from-right 0.3s ease-out',
        'spin-slow': 'spin 2s linear infinite',
      },

      // ============================================
      // SOMBRAS
      // ============================================
      boxShadow: {
        'card': '0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1)',
        'card-hover': '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
        'dropdown': '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
      },
    },
  },
  plugins: [
    require('tailwindcss-animate'),
  ],
}
```

## Uso em Projetos Consumidores

### Estender Configuracao

```javascript
// tailwind.config.js do projeto
const carfConfig = require('@carf/ui/tailwind.config')

module.exports = {
  presets: [carfConfig],
  content: [
    './src/**/*.{js,ts,jsx,tsx}',
    './node_modules/@carf/ui/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      // Customizacoes do projeto
      colors: {
        brand: '#FF0000',
      },
    },
  },
}
```

### Dependencias Necessarias

```bash
bun add -D tailwindcss postcss autoprefixer tailwindcss-animate
```

### PostCSS Config

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

## Classes Utilitarias CARF

### Cores de Marca

```html
<!-- Background -->
<div class="bg-carf-primary">Primary background</div>
<div class="bg-carf-secondary">Secondary background</div>
<div class="bg-carf-accent">Accent background</div>

<!-- Texto -->
<p class="text-carf-primary">Primary text</p>
<p class="text-carf-secondary">Secondary text</p>

<!-- Tons -->
<div class="bg-carf-primary-100">Light primary</div>
<div class="bg-carf-primary-900">Dark primary</div>
```

### Status

```html
<span class="text-success">Aprovado</span>
<span class="text-warning">Pendente</span>
<span class="text-error">Rejeitado</span>
<span class="text-info">Em analise</span>

<div class="bg-success-light">Success background light</div>
<div class="border-error">Error border</div>
```

### Animacoes

```html
<div class="animate-fade-in">Fade in</div>
<div class="animate-slide-in-from-bottom">Slide up</div>
<div class="animate-spin-slow">Loading spinner</div>
```
