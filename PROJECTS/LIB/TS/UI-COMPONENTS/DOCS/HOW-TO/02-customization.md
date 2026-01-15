# Customization - @carf/ui

## Customização de Tema

Customização de tema é feita nas aplicações consumidoras (GEOWEB/ADMIN) modificando CSS variables em `app/globals.css` definindo cores (`--primary`, `--secondary`, `--destructive`), raios de borda (`--radius`), fontes (`--font-sans`, `--font-mono`), e spacing via Tailwind config, por exemplo alterar cor primária para verde com `--primary: 142 76% 36%;` (HSL format), ou trocar fonte para Inter com `import { Inter } from 'next/font/google'` e aplicar em `:root`, componentes automaticamente refletem mudanças via CSS variables sem rebuild da biblioteca.

## CSS Variables Disponíveis

### Cores

```css
/* app/globals.css */
@layer base {
  :root {
    /* Cores principais */
    --primary: 220 90% 56%;        /* Azul primário */
    --secondary: 240 5% 64%;       /* Cinza secundário */
    --destructive: 0 84% 60%;      /* Vermelho para ações destrutivas */
    --success: 142 76% 36%;        /* Verde para sucesso */
    --warning: 48 96% 53%;         /* Amarelo para avisos */

    /* Backgrounds */
    --background: 0 0% 100%;       /* Branco */
    --foreground: 222 47% 11%;     /* Texto escuro */

    /* Borders */
    --border: 214 32% 91%;
    --input: 214 32% 91%;
    --ring: 220 90% 56%;
  }

  .dark {
    --primary: 220 90% 56%;
    --background: 222 47% 11%;
    --foreground: 210 40% 98%;
    /* ... demais cores dark mode */
  }
}
```

### Tipografia

```css
:root {
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'Fira Code', monospace;
}
```

### Espaçamento

```css
:root {
  --radius: 0.5rem;  /* Border radius padrão */
}
```

## Customizar Cores

### Alterar Cor Primária

```css
/* Azul (padrão) */
--primary: 220 90% 56%;

/* Verde */
--primary: 142 76% 36%;

/* Roxo */
--primary: 262 83% 58%;

/* Laranja */
--primary: 25 95% 53%;
```

Formato: `H S% L%` (Hue Saturation Lightness)

### Converter de HEX para HSL

```typescript
// Ferramenta online: https://www.htmlcsscolor.com/hex/3B82F6
// Ou usar função:
function hexToHSL(hex: string) {
  // Converte #3B82F6 → 220 90% 56%
}
```

## Customizar Fonte

```typescript
// app/layout.tsx
import { Inter, Fira_Code } from 'next/font/google'

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-sans',
})

const firaCode = Fira_Code({
  subsets: ['latin'],
  variable: '--font-mono',
})

export default function RootLayout({ children }) {
  return (
    <html className={`${inter.variable} ${firaCode.variable}`}>
      <body>{children}</body>
    </html>
  )
}
```

## Customizar Border Radius

```css
/* Bordas arredondadas (padrão) */
--radius: 0.5rem;

/* Bordas retas */
--radius: 0;

/* Bordas muito arredondadas */
--radius: 1rem;
```

## Exemplo Completo - Tema Verde

```css
/* app/globals.css */
@layer base {
  :root {
    --primary: 142 76% 36%;        /* Verde */
    --secondary: 160 60% 45%;      /* Verde-azulado */
    --success: 142 76% 36%;        /* Verde igual ao primário */
    --radius: 0.25rem;             /* Bordas menos arredondadas */
  }
}
```

```typescript
// app/layout.tsx
import { Roboto } from 'next/font/google'

const roboto = Roboto({
  weight: ['400', '500', '700'],
  subsets: ['latin'],
  variable: '--font-sans',
})
```

Componentes automaticamente refletem o novo tema sem rebuild.

## Referências

- [shadcn/ui Theming](https://ui.shadcn.com/docs/theming)
- [Tailwind CSS Customization](https://tailwindcss.com/docs/theme)
- [CSS Variables](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
