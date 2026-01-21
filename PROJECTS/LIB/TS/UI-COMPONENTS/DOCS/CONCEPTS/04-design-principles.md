---
status: review
updated: 2026-01-21
---

# Design Principles

Princípios de design que guiam todas as decisões arquiteturais e de implementação da biblioteca @carf/ui. Cada princípio inclui justificativa, exemplos práticos de uso correto (DO) e anti-patterns a evitar (DON'T).

## 1. Composition over Configuration

Preferir composição de subcomponentes ao invés de props booleanas excessivas. Componentes compostos oferecem flexibilidade máxima sem explosão combinatória de props, mantendo single responsibility principle.

### Justificativa

Componentes configurados por props tendem a acumular variantes (`showHeader`, `showFooter`, `headerVariant`, `footerAlign`) até se tornarem impossíveis de manter. Composição permite que cada subcomponente seja simples enquanto o todo permanece flexível.

### DO: Compound Components

```tsx
// Cada subcomponente tem responsabilidade única
<Dialog>
  <Dialog.Trigger asChild>
    <Button variant="outline">Editar Unidade</Button>
  </Dialog.Trigger>
  <Dialog.Content>
    <Dialog.Header>
      <Dialog.Title>Editar Dados</Dialog.Title>
      <Dialog.Description>
        Atualize as informações da unidade habitacional.
      </Dialog.Description>
    </Dialog.Header>
    <form>
      <FormField>
        <Label>Endereço</Label>
        <Input {...register('address')} />
      </FormField>
    </form>
    <Dialog.Footer>
      <Dialog.Close asChild>
        <Button variant="outline">Cancelar</Button>
      </Dialog.Close>
      <Button type="submit">Salvar</Button>
    </Dialog.Footer>
  </Dialog.Content>
</Dialog>
```

### DON'T: Props Bloat

```tsx
// Dezenas de props para controlar tudo
<Dialog
  trigger={<Button>Editar</Button>}
  triggerVariant="outline"
  title="Editar Dados"
  description="Atualize as informações..."
  showDescription={true}
  content={<form>...</form>}
  footerAlign="right"
  showFooter={true}
  cancelText="Cancelar"
  cancelVariant="outline"
  confirmText="Salvar"
  confirmVariant="default"
  onCancel={handleCancel}
  onConfirm={handleConfirm}
  closeOnOverlayClick={true}
  closeOnEscape={true}
/>
```

**Problemas do props bloat:**
- Explosão combinatória de variantes
- Documentação extensa e difícil de navegar
- Difícil adicionar casos especiais
- TypeScript autocomplete poluído

## 2. Accessibility First

Acessibilidade não é feature opcional - é requisito fundamental. Nenhum componente é considerado completo sem ARIA correto, navegação por teclado funcional e testes axe-core passando.

### Justificativa

Componentes são usados em aplicações governamentais que devem cumprir Lei Brasileira de Inclusão (Lei 13.146/2015) e WCAG 2.1 AA. Adicionar acessibilidade depois é exponencialmente mais difícil e caro.

### DO: ARIA e Keyboard Desde o Início

```tsx
// Componente já nasce acessível
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, disabled, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(buttonVariants({ variant }), className)}
      disabled={disabled}
      aria-disabled={disabled}
      {...props}
    />
  )
)

// FormField associa label e error corretamente
<FormField>
  <Label htmlFor="cpf">CPF</Label>
  <Input
    id="cpf"
    aria-invalid={!!error}
    aria-describedby={error ? 'cpf-error' : undefined}
  />
  {error && (
    <FormMessage id="cpf-error" role="alert">
      {error.message}
    </FormMessage>
  )}
</FormField>
```

### DON'T: Acessibilidade como Afterthought

```tsx
// Componente sem ARIA, keyboard, ou associações
<div onClick={handleClick} style={{ cursor: 'pointer' }}>
  Click me
</div>

// Erro sem associação ao campo
<input type="text" />
<span className="text-red-500">CPF inválido</span>

// Label sem htmlFor
<label>Nome</label>
<input type="text" />
```

**Checklist obrigatório antes de merge:**
- [ ] Navegável por teclado (Tab, Enter, Escape, Arrow)
- [ ] ARIA roles e attributes corretos
- [ ] Contraste 4.5:1 (texto) e 3:1 (UI)
- [ ] Focus visível
- [ ] Testado com axe-core

## 3. Mobile-First Responsive

Design começa no mobile e expande para desktop via breakpoints Tailwind. Touch targets mínimos de 44x44px, espaçamentos adequados para evitar fat finger errors.

### Justificativa

Técnicos de campo usam tablets e smartphones para cadastro em visitas domiciliares. Interface deve funcionar perfeitamente em telas pequenas com interação touch.

### DO: Mobile Base, Desktop Enhancement

```tsx
// Classes mobile primeiro, breakpoints expandem
<div className="
  flex flex-col gap-4           /* Mobile: stack vertical */
  md:flex-row md:gap-6          /* Tablet+: horizontal */
  lg:gap-8                      /* Desktop: mais espaço */
">
  <Card className="
    w-full                      /* Mobile: full width */
    md:w-1/2                    /* Tablet: metade */
    lg:w-1/3                    /* Desktop: terço */
  ">
    {/* ... */}
  </Card>
</div>

// Touch targets mínimos 44x44px
<Button className="
  min-h-[44px] min-w-[44px]     /* Touch target */
  px-4 py-2                     /* Padding interno */
">
  Salvar
</Button>
```

### DON'T: Desktop-First Degradation

```tsx
// Desktop primeiro, mobile quebra
<div className="
  flex flex-row gap-8          /* Desktop assume */
  sm:flex-col sm:gap-4         /* Tentar corrigir para mobile */
">
  {/* ... */}
</div>

// Touch targets pequenos demais
<Button className="px-2 py-1 text-xs">
  <Icon size={12} />
</Button>
```

**Breakpoints Tailwind utilizados:**

| Breakpoint | Min Width | Uso Típico |
|:-----------|:----------|:-----------|
| (default) | 0px | Mobile |
| `sm:` | 640px | Mobile landscape |
| `md:` | 768px | Tablet |
| `lg:` | 1024px | Desktop |
| `xl:` | 1280px | Desktop wide |

## 4. Design Tokens via CSS Variables

Customização visual via CSS variables definidas em `globals.css`, permitindo theming dinâmico (dark mode, white-labeling) sem modificar código de componentes.

### Justificativa

CARF pode ser implantado em múltiplos municípios com identidades visuais diferentes. Tokens permitem trocar cores institucionais via configuração, não código.

### DO: Usar Tokens Semânticos

```tsx
// Componentes usam tokens semânticos
<Button className="bg-primary text-primary-foreground">
  Salvar
</Button>

<Alert className="bg-destructive text-destructive-foreground">
  Erro de validação
</Alert>

// globals.css define tokens
:root {
  --primary: 221.2 83.2% 53.3%;           /* Azul CARF default */
  --primary-foreground: 210 40% 98%;
  --destructive: 0 84.2% 60.2%;           /* Vermelho erro */
}

/* Município X customiza apenas tokens */
.theme-municipio-x {
  --primary: 142 76% 36%;                 /* Verde institucional */
}
```

### DON'T: Cores Hardcoded

```tsx
// Cores fixas no código
<Button className="bg-blue-600 text-white">
  Salvar
</Button>

// Hex inline impossibilita theming
<div style={{ backgroundColor: '#2C5F2D' }}>
  Header
</div>
```

**Tokens obrigatórios:**

| Token | Uso | Contraparte Foreground |
|:------|:----|:-----------------------|
| `--background` | Fundo da página | `--foreground` |
| `--card` | Fundo de cards | `--card-foreground` |
| `--primary` | Ações principais | `--primary-foreground` |
| `--secondary` | Ações secundárias | `--secondary-foreground` |
| `--muted` | Elementos desabilitados | `--muted-foreground` |
| `--accent` | Destaques hover | `--accent-foreground` |
| `--destructive` | Ações destrutivas | `--destructive-foreground` |

## 5. Performance by Default

Bundle size monitorado, code splitting implícito via imports individuais, lazy loading para componentes pesados. Lighthouse Performance Score >90 como meta.

### Justificativa

Conexões de internet em áreas de regularização fundiária podem ser instáveis. Bundle leve significa app funcional mesmo em 3G.

### DO: Imports Granulares e Lazy Loading

```tsx
// Import apenas componentes necessários (tree-shaking)
import { Button, Input } from '@carf/ui'

// Lazy load componentes pesados
const DataTable = React.lazy(() => import('@carf/ui/DataTable'))
const Map = React.lazy(() => import('@carf/ui/Map'))

function UnitsPage() {
  return (
    <Suspense fallback={<Skeleton className="h-96" />}>
      <DataTable columns={columns} data={units} />
    </Suspense>
  )
}
```

### DON'T: Import Barrel ou Bundle Inteiro

```tsx
// Import barrel carrega tudo
import * as UI from '@carf/ui'

// Componentes pesados sem lazy loading
import { DataTable, Map, Chart, RichTextEditor } from '@carf/ui'

function Dashboard() {
  // Tudo carregado mesmo se usuário nunca vê Chart
  return (
    <div>
      <DataTable />
      {showChart && <Chart />}
    </div>
  )
}
```

**Orçamento de bundle:**

| Categoria | Limite |
|:----------|:-------|
| Core components (Button, Input, etc.) | <20KB gzip |
| Dialog, Sheet, Popover | <5KB gzip cada |
| DataTable | <30KB gzip |
| Total @carf/ui | <80KB gzip |

## 6. Consistency via Storybook

Cada componente documentado no Storybook com todas variantes, estados e exemplos de uso. Storybook é source of truth para designers e desenvolvedores.

### Justificativa

Desenvolvedores em diferentes projetos (GEOWEB, ADMIN, Keycloak) devem usar componentes da mesma forma. Storybook elimina ambiguidade e reduz bugs de integração.

### DO: Stories Completas

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react'
import { Button } from './Button'

const meta: Meta<typeof Button> = {
  component: Button,
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'secondary', 'destructive', 'outline', 'ghost', 'link'],
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'icon'],
    },
  },
}
export default meta

type Story = StoryObj<typeof Button>

export const Default: Story = {
  args: { children: 'Button' },
}

export const AllVariants: Story = {
  render: () => (
    <div className="flex flex-wrap gap-4">
      <Button variant="default">Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  ),
}

export const Disabled: Story = {
  args: { children: 'Disabled', disabled: true },
}

export const Loading: Story = {
  render: () => (
    <Button disabled>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      Salvando...
    </Button>
  ),
}

export const WithIcon: Story = {
  render: () => (
    <Button>
      <Plus className="mr-2 h-4 w-4" />
      Adicionar
    </Button>
  ),
}
```

### DON'T: Componentes sem Documentação

```tsx
// Arquivo sem stories
export const Button = ({ children }) => (
  <button>{children}</button>
)

// Story mínima sem variantes
export const Default = {
  args: { children: 'Button' },
}
// Onde estão disabled, loading, sizes, com ícone?
```

## 7. Testability via Testing Library

Componentes testados com filosofia user-centric: queries por role, label e text. Testes verificam comportamento observável, não implementação interna.

### Justificativa

Testes acoplados à implementação quebram com refatorações seguras. Testes user-centric verificam o que usuário percebe, permanecendo válidos enquanto comportamento externo não mudar.

### DO: Testar como Usuário

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('Dialog', () => {
  it('opens and closes via trigger and escape', async () => {
    const user = userEvent.setup()

    render(
      <Dialog>
        <Dialog.Trigger>Open</Dialog.Trigger>
        <Dialog.Content>
          <Dialog.Title>Modal Title</Dialog.Title>
          <Dialog.Close>Close</Dialog.Close>
        </Dialog.Content>
      </Dialog>
    )

    // Inicialmente fechado
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()

    // Abre via click no trigger
    await user.click(screen.getByRole('button', { name: /open/i }))
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    expect(screen.getByText('Modal Title')).toBeInTheDocument()

    // Fecha via Escape
    await user.keyboard('{Escape}')
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument()
  })

  it('traps focus inside when open', async () => {
    const user = userEvent.setup()

    render(
      <Dialog defaultOpen>
        <Dialog.Content>
          <input data-testid="first" />
          <input data-testid="last" />
        </Dialog.Content>
      </Dialog>
    )

    // Focus no primeiro elemento
    expect(document.activeElement).toBe(screen.getByTestId('first'))

    // Tab cicla dentro do dialog
    await user.tab()
    expect(document.activeElement).toBe(screen.getByTestId('last'))

    await user.tab()
    // Volta para o primeiro (focus trap)
    expect(document.activeElement).toBe(screen.getByTestId('first'))
  })
})
```

### DON'T: Testar Implementação

```tsx
// Teste acoplado a estado interno
it('sets isOpen to true', () => {
  const { result } = renderHook(() => useDialog())
  act(() => result.current.open())
  expect(result.current.isOpen).toBe(true)  // ❌ Detalhe interno
})

// Teste acoplado a classes CSS
it('has correct classes', () => {
  render(<Button variant="primary" />)
  expect(screen.getByRole('button')).toHaveClass('bg-primary')  // ❌ Implementação
})

// Snapshot tests frágeis
it('matches snapshot', () => {
  const { container } = render(<Button>Click</Button>)
  expect(container).toMatchSnapshot()  // ❌ Quebra com qualquer mudança
})
```

## 8. Developer Experience

TypeScript strict, autocomplete completo, props bem documentadas, error messages úteis. Desenvolvedores devem ser produtivos sem consultar documentação externa constantemente.

### Justificativa

Boa DX reduz tempo de onboarding, diminui bugs de integração e aumenta satisfação da equipe. Investir em DX é investir em velocidade de entrega.

### DO: Types Expressivos

```tsx
// Variants tipadas com autocomplete
type ButtonVariant = 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
type ButtonSize = 'default' | 'sm' | 'lg' | 'icon'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  /** Visual style variant */
  variant?: ButtonVariant
  /** Size preset */
  size?: ButtonSize
  /** Renders as child element (Radix Slot) */
  asChild?: boolean
}

// Props opcionais com defaults sensatos
const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = 'default', size = 'default', asChild = false, ...props }, ref) => {
    // ...
  }
)

// Error messages úteis em runtime
if (process.env.NODE_ENV !== 'production') {
  if (asChild && props.disabled) {
    console.warn(
      '@carf/ui: Button with asChild={true} cannot use disabled prop. ' +
      'Apply disabled to the child component instead.'
    )
  }
}
```

### DON'T: Types Genéricos ou any

```tsx
// Props genéricas demais
interface ButtonProps {
  variant?: string
  size?: string
  [key: string]: any  // ❌ Sem autocomplete
}

// Sem JSDoc
const Button = (props: ButtonProps) => { ... }

// Error silencioso
if (asChild && disabled) {
  // Falha silenciosa, desenvolvedores perdem tempo debugando
}
```

## Referências

- [Radix UI Design Principles](https://radix-ui.com/docs/primitives/overview/philosophy)
- [shadcn/ui Design Philosophy](https://ui.shadcn.com/docs)
- [Tailwind CSS Best Practices](https://tailwindcss.com/docs/reusing-styles)
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles)
- [Lei Brasileira de Inclusão](https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm)
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
