---
title: "Utils - @carf/ui"
status: review
updated: 2026-01-21
source: "interno"
---

# Utils - @carf/ui

Funcoes utilitarias para uso em componentes e aplicacoes.

## cn()

Combina classes CSS com suporte a conflitos Tailwind.

### Importacao

```tsx
import { cn } from '@carf/ui'
```

### Uso

```tsx
// Combinar classes
<div className={cn('p-4 bg-white', 'rounded-lg')}>
  {/* class="p-4 bg-white rounded-lg" */}
</div>

// Classes condicionais
<div className={cn(
  'p-4 rounded-lg',
  isActive && 'bg-primary text-white',
  isDisabled && 'opacity-50 cursor-not-allowed'
)}>
  {/* Aplica classes baseado em condicoes */}
</div>

// Resolver conflitos Tailwind
<div className={cn('p-4', 'p-8')}>
  {/* class="p-8" - tailwind-merge resolve o conflito */}
</div>

// Em componentes
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'outline'
}

function Button({ className, variant = 'default', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'px-4 py-2 rounded-md font-medium',
        variant === 'default' && 'bg-primary text-white',
        variant === 'outline' && 'border border-primary text-primary',
        className
      )}
      {...props}
    />
  )
}

// Permite customizacao
<Button className="px-8">Botao Largo</Button>
```

### Implementacao

```tsx
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

---

## cva()

Class Variance Authority para variantes de componentes.

### Importacao

```tsx
import { cva, type VariantProps } from 'class-variance-authority'
```

### Uso

```tsx
// Definir variantes
const buttonVariants = cva(
  // Classes base (sempre aplicadas)
  'inline-flex items-center justify-center rounded-md font-medium transition-colors',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

// Usar em componente
interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

function Button({ className, variant, size, ...props }: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  )
}

// Uso
<Button>Default</Button>
<Button variant="destructive" size="lg">Excluir</Button>
```

---

## Formatters

Funcoes para formatacao de dados.

### formatCPF

```tsx
import { formatCPF } from '@carf/ui'

formatCPF('12345678900')
// "123.456.789-00"

formatCPF('123.456.789-00')
// "123.456.789-00" (ja formatado)
```

### formatCNPJ

```tsx
import { formatCNPJ } from '@carf/ui'

formatCNPJ('12345678000100')
// "12.345.678/0001-00"
```

### formatPhone

```tsx
import { formatPhone } from '@carf/ui'

formatPhone('11999998888')
// "(11) 99999-8888"

formatPhone('1133334444')
// "(11) 3333-4444"
```

### formatCurrency

```tsx
import { formatCurrency } from '@carf/ui'

formatCurrency(1234.56)
// "R$ 1.234,56"

formatCurrency(1234.56, { currency: 'USD' })
// "$ 1,234.56"
```

### formatDate

```tsx
import { formatDate } from '@carf/ui'

formatDate(new Date())
// "20/01/2026"

formatDate(new Date(), { format: 'long' })
// "20 de janeiro de 2026"

formatDate(new Date(), { format: 'relative' })
// "hoje" | "ontem" | "ha 3 dias"
```

### formatArea

```tsx
import { formatArea } from '@carf/ui'

formatArea(1234.5)
// "1.234,5 m²"

formatArea(10000, { unit: 'hectare' })
// "1 ha"
```

### Implementacoes

```tsx
export function formatCPF(value: string): string {
  const digits = value.replace(/\D/g, '')
  return digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
}

export function formatCNPJ(value: string): string {
  const digits = value.replace(/\D/g, '')
  return digits.replace(
    /(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/,
    '$1.$2.$3/$4-$5'
  )
}

export function formatPhone(value: string): string {
  const digits = value.replace(/\D/g, '')
  if (digits.length === 11) {
    return digits.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3')
  }
  return digits.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3')
}

export function formatCurrency(
  value: number,
  options?: { currency?: string; locale?: string }
): string {
  const { currency = 'BRL', locale = 'pt-BR' } = options || {}
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency,
  }).format(value)
}

export function formatDate(
  date: Date,
  options?: { format?: 'short' | 'long' | 'relative'; locale?: string }
): string {
  const { format = 'short', locale = 'pt-BR' } = options || {}

  if (format === 'relative') {
    const rtf = new Intl.RelativeTimeFormat(locale, { numeric: 'auto' })
    const diff = Math.floor((date.getTime() - Date.now()) / (1000 * 60 * 60 * 24))
    return rtf.format(diff, 'day')
  }

  return new Intl.DateTimeFormat(locale, {
    dateStyle: format === 'long' ? 'long' : 'short',
  }).format(date)
}

export function formatArea(
  value: number,
  options?: { unit?: 'sqm' | 'hectare' }
): string {
  const { unit = 'sqm' } = options || {}
  if (unit === 'hectare') {
    return `${(value / 10000).toLocaleString('pt-BR')} ha`
  }
  return `${value.toLocaleString('pt-BR')} m²`
}
```

---

## Validators

Funcoes de validacao comuns.

### isValidCPF

```tsx
import { isValidCPF } from '@carf/ui'

isValidCPF('123.456.789-09') // true
isValidCPF('111.111.111-11') // false (digitos repetidos)
```

### isValidCNPJ

```tsx
import { isValidCNPJ } from '@carf/ui'

isValidCNPJ('12.345.678/0001-95') // true
```

### isValidEmail

```tsx
import { isValidEmail } from '@carf/ui'

isValidEmail('joao@email.com') // true
isValidEmail('invalido@') // false
```

### isValidPhone

```tsx
import { isValidPhone } from '@carf/ui'

isValidPhone('(11) 99999-8888') // true
isValidPhone('11999998888') // true
```

---

## Helpers

Funcoes auxiliares diversas.

### getInitials

```tsx
import { getInitials } from '@carf/ui'

getInitials('Joao Silva')
// "JS"

getInitials('Maria')
// "MA"

getInitials('Joao Pedro Silva')
// "JS" (primeiro e ultimo)
```

### slugify

```tsx
import { slugify } from '@carf/ui'

slugify('Meu Titulo Aqui')
// "meu-titulo-aqui"

slugify('Conteúdo com Acentos')
// "conteudo-com-acentos"
```

### truncate

```tsx
import { truncate } from '@carf/ui'

truncate('Texto muito longo que precisa ser cortado', 20)
// "Texto muito longo..."

truncate('Curto', 20)
// "Curto"
```

### debounce

```tsx
import { debounce } from '@carf/ui'

const debouncedSearch = debounce((term: string) => {
  fetchResults(term)
}, 300)

// Chamadas rapidas sao agrupadas
debouncedSearch('a')
debouncedSearch('ab')
debouncedSearch('abc') // So essa executa (apos 300ms)
```

### throttle

```tsx
import { throttle } from '@carf/ui'

const throttledScroll = throttle(() => {
  updateScrollPosition()
}, 100)

window.addEventListener('scroll', throttledScroll)
```

### Implementacoes

```tsx
export function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/)
  if (parts.length === 1) {
    return parts[0].slice(0, 2).toUpperCase()
  }
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
}

export function truncate(text: string, length: number): string {
  if (text.length <= length) return text
  return text.slice(0, length - 3) + '...'
}

export function debounce<T extends (...args: any[]) => any>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}

export function throttle<T extends (...args: any[]) => any>(
  fn: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle = false
  return (...args) => {
    if (!inThrottle) {
      fn(...args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), limit)
    }
  }
}
```

---

## Constantes

### carfColors

Cores do tema CARF para uso programatico.

```tsx
import { carfColors } from '@carf/ui'

carfColors.primary.DEFAULT  // '#2C5F2D'
carfColors.primary[500]     // '#2C5F2D'
carfColors.secondary.light  // '#B8D98C'
carfColors.status.success   // '#15981C'
carfColors.status.error     // '#E63946'
```

### breakpoints

Breakpoints responsivos.

```tsx
import { breakpoints } from '@carf/ui'

breakpoints.sm   // '640px'
breakpoints.md   // '768px'
breakpoints.lg   // '1024px'
breakpoints.xl   // '1280px'
breakpoints['2xl'] // '1536px'
```
