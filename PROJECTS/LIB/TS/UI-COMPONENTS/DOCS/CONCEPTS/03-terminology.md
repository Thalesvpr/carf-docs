---
status: review
updated: 2026-01-21
---

# Terminology

Glossário de termos técnicos e arquiteturais utilizados na biblioteca @carf/ui, cobrindo padrões React, metodologia de design, CSS e ferramentas de desenvolvimento. Cada termo inclui definição, exemplo de código correto e anti-patterns a evitar.

## Termos Arquiteturais

### Atomic Design

Metodologia de design criada por Brad Frost que organiza componentes em cinco níveis de abstração: Atoms, Molecules, Organisms, Templates e Pages. @carf/ui implementa os três primeiros níveis.

| Nível | Definição | Exemplos @carf/ui |
|:------|:----------|:------------------|
| Atom | Componente indivisível, menor unidade UI | `Button`, `Input`, `Badge`, `Avatar`, `Label` |
| Molecule | Combinação de atoms formando grupo funcional | `FormField` (Label + Input + FormMessage), `SearchInput` (Input + IconButton) |
| Organism | Grupo de molecules formando seção completa | `UnitCard`, `HolderCard`, `LoginForm`, `DataTable` |

**Exemplo Correto - Molecule**:
```tsx
// FormField é molecule: combina atoms Label, Input, FormMessage
<FormField>
  <Label htmlFor="cpf">CPF</Label>
  <Input id="cpf" {...field} />
  <FormMessage>{error?.message}</FormMessage>
</FormField>
```

**Anti-pattern - Atom fazendo trabalho de Molecule**:
```tsx
// Input não deveria incluir label internamente
<Input label="CPF" error={error} />  // ❌ Viola separação de concerns
```

### Compound Component

Padrão React onde um componente pai fornece contexto compartilhado para subcomponentes filhos, permitindo composição flexível sem prop drilling. Subcomponentes são acessados como propriedades estáticas do componente pai.

**Exemplo Correto**:
```tsx
// Card usa compound components para máxima flexibilidade
<Card>
  <Card.Header>
    <Card.Title>Unidade Habitacional</Card.Title>
    <Card.Description>Dados do imóvel cadastrado</Card.Description>
  </Card.Header>
  <Card.Content>
    {/* Conteúdo livre */}
  </Card.Content>
  <Card.Footer>
    <Button variant="outline">Cancelar</Button>
    <Button>Salvar</Button>
  </Card.Footer>
</Card>
```

**Anti-pattern - Props Bloat**:
```tsx
// Muitas props booleanas e slots como props
<Card
  title="Unidade Habitacional"
  description="Dados do imóvel cadastrado"
  content={<div>...</div>}
  footerLeft={<Button variant="outline">Cancelar</Button>}
  footerRight={<Button>Salvar</Button>}
  showHeader={true}
  showFooter={true}
/>  // ❌ Inflexível, difícil de estender
```

**Componentes @carf/ui que usam Compound Pattern**:
- `Dialog` → `Dialog.Trigger`, `Dialog.Content`, `Dialog.Header`, `Dialog.Footer`, `Dialog.Close`
- `Card` → `Card.Header`, `Card.Title`, `Card.Description`, `Card.Content`, `Card.Footer`
- `Tabs` → `Tabs.List`, `Tabs.Trigger`, `Tabs.Content`
- `Accordion` → `Accordion.Item`, `Accordion.Trigger`, `Accordion.Content`
- `DropdownMenu` → `DropdownMenu.Trigger`, `DropdownMenu.Content`, `DropdownMenu.Item`
- `Table` → `Table.Header`, `Table.Body`, `Table.Row`, `Table.Head`, `Table.Cell`

### Controlled vs Uncontrolled

Dois padrões para gerenciar estado de inputs em React.

| Aspecto | Controlled | Uncontrolled |
|:--------|:-----------|:-------------|
| Estado | Gerenciado externamente via props (`value`, `onChange`) | Estado interno, acesso via `ref` |
| Re-renders | A cada keystroke | Apenas quando necessário |
| Validação | Síncrona, a cada mudança | Na submissão ou blur |
| Uso ideal | Formulários complexos, validação inline | Formulários simples, performance crítica |
| React Hook Form | `<Controller>` ou `register` com `mode: 'onChange'` | `register` com `mode: 'onSubmit'` |

**Controlled - Validação Inline**:
```tsx
// Estado controlado pelo parent
const [value, setValue] = useState('')
const [error, setError] = useState<string | null>(null)

<Input
  value={value}
  onChange={(e) => {
    setValue(e.target.value)
    setError(validateCpf(e.target.value) ? null : 'CPF inválido')
  }}
/>
{error && <FormMessage>{error}</FormMessage>}
```

**Uncontrolled - Performance**:
```tsx
// Estado interno, acesso via ref ou submissão
const inputRef = useRef<HTMLInputElement>(null)

<Input ref={inputRef} defaultValue="" />

function handleSubmit() {
  const value = inputRef.current?.value
  // Validar no submit
}
```

**@carf/ui**: Todos componentes de input suportam ambos padrões. Preferir controlled quando usando React Hook Form com validação Zod.

### Headless Component

Componente que fornece lógica e comportamento (state, keyboard navigation, ARIA) sem nenhum estilo visual. Radix UI Primitives são headless, permitindo customização completa via CSS/Tailwind.

**Exemplo - Radix Headless → @carf/ui Styled**:
```tsx
// Radix fornece comportamento sem estilo
import * as DialogPrimitive from '@radix-ui/react-dialog'

// @carf/ui adiciona estilos Tailwind
const DialogContent = React.forwardRef<...>(({ className, ...props }, ref) => (
  <DialogPrimitive.Content
    ref={ref}
    className={cn(
      'fixed left-[50%] top-[50%] translate-x-[-50%] translate-y-[-50%]',
      'w-full max-w-lg rounded-lg border bg-background p-6 shadow-lg',
      'data-[state=open]:animate-in data-[state=closed]:animate-out',
      className
    )}
    {...props}
  />
))
```

### Render Props / Children as Function

Padrão onde componente aceita função como children, passando estado interno para customização do render.

**Exemplo**:
```tsx
<Combobox>
  {({ open, selectedItem }) => (
    <>
      <Combobox.Input displayValue={(item) => item.name} />
      {open && (
        <Combobox.Options>
          {items.map(item => (
            <Combobox.Option key={item.id} value={item}>
              {item.name}
              {selectedItem?.id === item.id && <CheckIcon />}
            </Combobox.Option>
          ))}
        </Combobox.Options>
      )}
    </>
  )}
</Combobox>
```

### Polymorphic Component

Componente que pode renderizar como diferentes elementos HTML ou outros componentes via prop `as` ou `asChild`.

**Exemplo com asChild (padrão Radix)**:
```tsx
// Button renderiza como <a> para navegação
<Button asChild>
  <Link href="/units">Ver Unidades</Link>
</Button>

// DialogTrigger renderiza como Button customizado
<Dialog.Trigger asChild>
  <Button variant="outline">Abrir</Button>
</Dialog.Trigger>
```

**Anti-pattern**:
```tsx
// Não usar asChild quando não necessário
<Button asChild>
  <button>Click</button>  // ❌ Redundante, Button já é button
</Button>
```

## Termos CSS

### CSS Variables (Custom Properties)

Valores reutilizáveis definidos em CSS permitindo theming dinâmico sem recompilação. @carf/ui define tokens em `globals.css` seguindo convenções shadcn/ui.

```css
/* globals.css */
:root {
  --background: 0 0% 100%;           /* HSL sem hsl() */
  --foreground: 222.2 84% 4.9%;
  --primary: 221.2 83.2% 53.3%;
  --primary-foreground: 210 40% 98%;
  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
}
```

**Uso em Componentes**:
```tsx
// Tailwind usa tokens via hsl()
<Button className="bg-primary text-primary-foreground" />

// CSS compilado
.bg-primary { background-color: hsl(var(--primary)); }
```

### Design Tokens

Constantes de design (cores, tipografia, espaçamento, sombras) extraídas em variáveis reutilizáveis garantindo consistência visual. @carf/ui tokens definidos em `tailwind.config.ts` e `globals.css`.

| Categoria | Tokens @carf/ui | Exemplo |
|:----------|:----------------|:--------|
| Cores | `--primary`, `--secondary`, `--destructive`, `--muted` | `bg-primary`, `text-destructive` |
| Tipografia | `--font-sans`, `--font-mono` | `font-sans`, `font-mono` |
| Espaçamento | Escala Tailwind padrão | `p-4`, `gap-2`, `space-y-4` |
| Raio de Borda | `--radius` | `rounded-md` (usa `calc(var(--radius) - 2px)`) |
| Sombras | Escala Tailwind padrão | `shadow-md`, `shadow-lg` |

### Utility-First CSS

Metodologia onde estilos são aplicados via classes utilitárias de propósito único ao invés de CSS semântico. Tailwind CSS implementa utility-first.

**Utility-First (Tailwind)**:
```tsx
<button className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600">
  Click
</button>
```

**Semântico (BEM)**:
```tsx
<button className="btn btn--primary btn--medium">Click</button>
```

```css
.btn { padding: 0.5rem 1rem; border-radius: 0.375rem; }
.btn--primary { background: blue; color: white; }
.btn--primary:hover { background: darkblue; }
```

**@carf/ui** usa utility-first via Tailwind, com `cn()` para merge condicional de classes.

### cn() Utility

Função utilitária que combina `clsx` e `tailwind-merge` para merge inteligente de classes Tailwind, resolvendo conflitos automaticamente.

```tsx
import { cn } from '@/lib/utils'

// Resolve conflitos: p-4 vence p-2
cn('p-2', 'p-4')  // → 'p-4'

// Condicional
cn('base-class', isActive && 'active-class', isDisabled && 'opacity-50')

// Permite override via className prop
const Button = ({ className, ...props }) => (
  <button
    className={cn(
      'px-4 py-2 rounded-md bg-primary text-primary-foreground',
      className  // Permite override: <Button className="bg-red-500" />
    )}
    {...props}
  />
)
```

## Termos de Ferramentas

### Storybook

Ferramenta para desenvolvimento isolado de componentes, permitindo visualizar, documentar e testar cada componente em diferentes estados sem rodar a aplicação completa.

**Estrutura de Story**:
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
      options: ['default', 'destructive', 'outline', 'ghost'],
    },
  },
}

export default meta
type Story = StoryObj<typeof Button>

export const Default: Story = {
  args: { children: 'Button' },
}

export const Destructive: Story = {
  args: { children: 'Delete', variant: 'destructive' },
}

export const Loading: Story = {
  args: { children: 'Loading...', disabled: true },
}
```

### Testing Library

Filosofia e conjunto de bibliotecas para testes user-centric, consultando elementos DOM como usuário real vê (por role, label, text) ao invés de detalhes de implementação (por testId, className).

**Exemplo Correto - User-Centric**:
```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

test('submits form with CPF', async () => {
  const user = userEvent.setup()
  const onSubmit = vi.fn()

  render(<LoginForm onSubmit={onSubmit} />)

  // Queries como usuário vê
  await user.type(screen.getByLabelText(/cpf/i), '123.456.789-00')
  await user.type(screen.getByLabelText(/senha/i), 'password')
  await user.click(screen.getByRole('button', { name: /entrar/i }))

  expect(onSubmit).toHaveBeenCalledWith({
    cpf: '123.456.789-00',
    password: 'password',
  })
})
```

**Anti-pattern - Implementation Details**:
```tsx
// Evitar queries por testId ou className
screen.getByTestId('cpf-input')  // ❌ Acoplado à implementação
screen.getByClassName('input-cpf')  // ❌ Testing Library não tem getByClassName

// Evitar acessar state interno
expect(component.state.isValid).toBe(true)  // ❌ Detalhe interno
```

### Radix UI

Biblioteca de primitives React headless, acessíveis e sem estilo, fornecendo comportamento complexo (keyboard navigation, focus management, ARIA) para componentes como Dialog, Dropdown, Tabs. @carf/ui é construída sobre Radix Primitives.

**Componentes @carf/ui baseados em Radix**:

| @carf/ui | Radix Primitive |
|:---------|:----------------|
| Dialog | @radix-ui/react-dialog |
| AlertDialog | @radix-ui/react-alert-dialog |
| DropdownMenu | @radix-ui/react-dropdown-menu |
| Select | @radix-ui/react-select |
| Tabs | @radix-ui/react-tabs |
| Accordion | @radix-ui/react-accordion |
| Popover | @radix-ui/react-popover |
| Tooltip | @radix-ui/react-tooltip |
| Switch | @radix-ui/react-switch |
| Checkbox | @radix-ui/react-checkbox |
| RadioGroup | @radix-ui/react-radio-group |
| Slider | @radix-ui/react-slider |
| Progress | @radix-ui/react-progress |

### shadcn/ui

Coleção de componentes React reutilizáveis construídos sobre Radix UI e Tailwind CSS. Diferente de bibliotecas tradicionais, código é copiado para o projeto (não instalado como dependência npm), permitindo customização total. @carf/ui é baseada em shadcn/ui com adaptações para design system CARF.

**Características**:
- Código fonte no projeto (não em node_modules)
- Customização via CSS variables
- TypeScript nativo
- Acessibilidade via Radix
- Sem breaking changes de dependências

## Termos de Estado

### Server State vs Client State

Distinção fundamental para gerenciamento de estado em aplicações React.

| Aspecto | Server State | Client State |
|:--------|:-------------|:-------------|
| Origem | API externa, banco de dados | Local na aplicação |
| Ownership | Backend é source of truth | Frontend é owner |
| Cache | Requer invalidação, refetch | Persistência opcional |
| Sincronização | Múltiplos clientes podem mutar | Isolado por sessão |
| Ferramenta @carf | TanStack Query | Zustand |
| Exemplos | Lista de unidades, dados de usuário | UI state, filtros, modais abertos |

**Server State (TanStack Query)**:
```tsx
// Dados vêm da API, cache automático
const { data: units, isLoading } = useQuery({
  queryKey: ['units', tenantId],
  queryFn: () => geoApiClient.units.list(tenantId),
})
```

**Client State (Zustand)**:
```tsx
// Estado local da UI
const useFilterStore = create((set) => ({
  statusFilter: 'all',
  setStatusFilter: (status) => set({ statusFilter: status }),
}))
```

### Optimistic Updates

Técnica onde UI é atualizada imediatamente assumindo sucesso da operação, revertendo se falhar. Melhora percepção de performance.

```tsx
const mutation = useMutation({
  mutationFn: updateUnit,
  onMutate: async (newData) => {
    // Cancel outgoing refetches
    await queryClient.cancelQueries({ queryKey: ['unit', id] })

    // Snapshot previous value
    const previousUnit = queryClient.getQueryData(['unit', id])

    // Optimistically update
    queryClient.setQueryData(['unit', id], newData)

    return { previousUnit }
  },
  onError: (err, newData, context) => {
    // Rollback on error
    queryClient.setQueryData(['unit', id], context.previousUnit)
  },
  onSettled: () => {
    // Refetch after error or success
    queryClient.invalidateQueries({ queryKey: ['unit', id] })
  },
})
```

## Referências

- [Atomic Design by Brad Frost](https://bradfrost.com/blog/post/atomic-web-design/)
- [React Patterns](https://reactpatterns.com/)
- [Radix UI Documentation](https://radix-ui.com/docs/primitives)
- [shadcn/ui Documentation](https://ui.shadcn.com/docs)
- [Testing Library Guiding Principles](https://testing-library.com/docs/guiding-principles)
- [TanStack Query Concepts](https://tanstack.com/query/latest/docs/framework/react/overview)
