# Testing - @carf/ui

## Testes de Componentes

Testes de componentes usam Testing Library com `render()` para montar componente, `screen.getByRole()` para queries acessíveis, `userEvent.click()` para interações, e `expect().toHaveTextContent()` para assertions, por exemplo testar Button com `test('calls onClick when clicked', () => { const onClick = vi.fn(); render(<Button onClick={onClick}>Click</Button>); userEvent.click(screen.getByRole('button')); expect(onClick).toHaveBeenCalled(); })`, testes de acessibilidade com `axe-core` via `@axe-core/react`, snapshot tests para prevenir regressões visuais, coverage mínimo de 80% para cada componente antes de merge.

## Setup de Testes

### Instalação

```bash
bun add -d @testing-library/react @testing-library/user-event
bun add -d @testing-library/jest-dom vitest
bun add -d @axe-core/react jsdom
```

### Configuração Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      reporter: ['text', 'html'],
      threshold: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80,
      },
    },
  },
})
```

## Estrutura de Teste

### Teste Básico

```typescript
// src/components/ui/button/Button.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Button } from './Button'

describe('Button', () => {
  it('renders children', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button')).toHaveTextContent('Click me')
  })

  it('calls onClick when clicked', async () => {
    const user = userEvent.setup()
    const onClick = vi.fn()

    render(<Button onClick={onClick}>Click me</Button>)
    await user.click(screen.getByRole('button'))

    expect(onClick).toHaveBeenCalledTimes(1)
  })

  it('applies variant styles', () => {
    render(<Button variant="destructive">Delete</Button>)
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-destructive')
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Disabled</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### Teste de Acessibilidade

```typescript
import { axe } from 'jest-axe'

it('has no accessibility violations', async () => {
  const { container } = render(<Button>Accessible</Button>)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

### Snapshot Test

```typescript
it('matches snapshot', () => {
  const { container } = render(<Button>Snapshot</Button>)
  expect(container.firstChild).toMatchSnapshot()
})
```

## Queries Recomendadas

### Por Acessibilidade (Preferir)

```typescript
// ✅ MELHOR - Por role (acessível)
screen.getByRole('button', { name: /submit/i })
screen.getByRole('textbox', { name: /email/i })
screen.getByRole('heading', { level: 1 })

// ✅ BOM - Por label
screen.getByLabelText(/email address/i)

// ✅ BOM - Por texto
screen.getByText(/hello world/i)
```

### Por Implementação (Evitar)

```typescript
// ❌ EVITAR - Por test ID (último recurso)
screen.getByTestId('submit-button')

// ❌ EVITAR - Por classe CSS
container.querySelector('.btn-primary')
```

## Interações

### Clicks

```typescript
const user = userEvent.setup()

// Click simples
await user.click(screen.getByRole('button'))

// Double click
await user.dblClick(screen.getByRole('button'))

// Click com modificadores
await user.click(screen.getByRole('button'), { ctrlKey: true })
```

### Digitação

```typescript
const user = userEvent.setup()

// Digitar texto
await user.type(screen.getByRole('textbox'), 'Hello World')

// Limpar e digitar
await user.clear(screen.getByRole('textbox'))
await user.type(screen.getByRole('textbox'), 'New text')
```

### Teclado

```typescript
const user = userEvent.setup()

// Pressionar tecla
await user.keyboard('{Enter}')
await user.keyboard('{Escape}')
await user.keyboard('{ArrowDown}')
```

## Testes Específicos CARF

### UnitCard

```typescript
import { UnitCard } from './UnitCard'
import type { Unit } from '@carf/tscore/types'

const mockUnit: Unit = {
  id: '1',
  code: 'UN-001',
  address: 'Rua das Flores, 123',
  area: 250,
  status: 'ACTIVE',
}

it('renders unit information', () => {
  render(<UnitCard unit={mockUnit} />)

  expect(screen.getByText('UN-001')).toBeInTheDocument()
  expect(screen.getByText(/rua das flores/i)).toBeInTheDocument()
  expect(screen.getByText(/250m²/i)).toBeInTheDocument()
})

it('calls onEdit when edit button is clicked', async () => {
  const user = userEvent.setup()
  const onEdit = vi.fn()

  render(<UnitCard unit={mockUnit} onEdit={onEdit} />)
  await user.click(screen.getByRole('button', { name: /edit/i }))

  expect(onEdit).toHaveBeenCalledWith(mockUnit)
})
```

## Comandos

```bash
# Rodar todos os testes
bun test

# Watch mode
bun test --watch

# Coverage report
bun test --coverage

# Rodar arquivo específico
bun test UnitCard.test.tsx

# Update snapshots
bun test -u
```

## Referências

- [Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Vitest](https://vitest.dev/)
- [jest-axe](https://github.com/nickcolley/jest-axe)
- [User Event](https://testing-library.com/docs/user-event/intro)

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Contém code blocks - considerar converter para prosa.
