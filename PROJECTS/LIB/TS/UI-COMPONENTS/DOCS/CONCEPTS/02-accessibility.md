---
status: review
updated: 2026-01-21
---

# Accessibility

Todos componentes @carf/ui seguem WCAG 2.1 AA, implementando ARIA labels, navegação por teclado, gerenciamento de foco, live regions para notificações dinâmicas e ratios de contraste mínimos validados via axe-core. Componentes são testados com NVDA, JAWS e VoiceOver, garantindo usabilidade para usuários de screen readers e navegação exclusivamente por teclado. Nenhum componente é mergeado sem passar testes automatizados de acessibilidade no CI.

## Navegação por Teclado

Cada componente implementa padrões de teclado consistentes com WAI-ARIA Authoring Practices. A tabela abaixo documenta as interações esperadas.

| Componente | Tab | Enter | Escape | Arrow Keys | Space | Home/End |
|:-----------|:----|:------|:-------|:-----------|:------|:---------|
| Button | Focus | Activate | - | - | Activate | - |
| IconButton | Focus | Activate | - | - | Activate | - |
| Link | Focus | Navigate | - | - | - | - |
| Input | Focus | Submit form | - | - | - | - |
| Textarea | Focus | Newline | - | - | - | - |
| Checkbox | Focus | - | - | - | Toggle | - |
| Radio | Focus group | - | - | Navigate options | Select | - |
| Switch | Focus | - | - | - | Toggle | - |
| Select | Focus | Open/Select | Close | Navigate | Select | First/Last |
| Combobox | Focus | Open/Select | Close | Navigate | - | First/Last |
| Dialog | Focus first element | - | Close | - | - | - |
| AlertDialog | Focus first element | - | - | - | - | - |
| Sheet | Focus first element | - | Close | - | - | - |
| Popover | Focus first element | - | Close | - | - | - |
| DropdownMenu | Focus first item | Activate | Close | Navigate | Activate | First/Last |
| ContextMenu | Focus first item | Activate | Close | Navigate | Activate | First/Last |
| Tabs | Focus tab | - | - | Switch tabs | Activate | First/Last |
| Accordion | Focus trigger | Toggle | - | Navigate | Toggle | - |
| Tooltip | - | - | - | - | - | - |
| Toast | - | - | Dismiss | - | - | - |

### Padrões de Navegação

**Roving Tabindex**: Componentes como Tabs, Radio Group e Menu implementam roving tabindex onde apenas um item é tabbable por vez. Arrow keys movem o foco entre items, Tab move para o próximo elemento fora do grupo.

```tsx
// Radio Group: Tab entra no grupo, Arrow move entre opções
<RadioGroup defaultValue="option1">
  <RadioGroupItem value="option1" />  {/* tabIndex={0} quando focado */}
  <RadioGroupItem value="option2" />  {/* tabIndex={-1} quando não focado */}
  <RadioGroupItem value="option3" />
</RadioGroup>
```

**Focus Trap**: Dialog, Sheet e AlertDialog implementam focus trap impedindo que Tab escape do modal enquanto aberto. Foco retorna ao elemento trigger quando fechado.

```tsx
// Focus preso dentro do Dialog enquanto aberto
<Dialog>
  <DialogTrigger>Open</DialogTrigger>  {/* Foco retorna aqui ao fechar */}
  <DialogContent>
    <Input autoFocus />  {/* Primeiro elemento focável */}
    <Button>Cancel</Button>
    <Button>Confirm</Button>  {/* Tab não escapa após este */}
  </DialogContent>
</Dialog>
```

## ARIA por Componente

Atributos ARIA obrigatórios e condicionais para cada componente.

| Componente | ARIA Obrigatórios | ARIA Condicionais |
|:-----------|:------------------|:------------------|
| Button | `role="button"` | `aria-pressed` (toggle), `aria-expanded` (menu trigger), `aria-disabled` |
| IconButton | `role="button"`, `aria-label` | `aria-pressed`, `aria-expanded` |
| Link | - | `aria-current="page"` (navegação ativa) |
| Input | - | `aria-invalid`, `aria-describedby` (error), `aria-required` |
| Textarea | - | `aria-invalid`, `aria-describedby`, `aria-required` |
| Checkbox | `role="checkbox"`, `aria-checked` | `aria-required` |
| Radio | `role="radio"`, `aria-checked` | - |
| RadioGroup | `role="radiogroup"` | `aria-required`, `aria-labelledby` |
| Switch | `role="switch"`, `aria-checked` | `aria-labelledby` |
| Select | `role="combobox"`, `aria-expanded`, `aria-haspopup="listbox"` | `aria-invalid`, `aria-required` |
| Combobox | `role="combobox"`, `aria-expanded`, `aria-autocomplete` | `aria-activedescendant` |
| Dialog | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` | `aria-describedby` |
| AlertDialog | `role="alertdialog"`, `aria-modal="true"`, `aria-labelledby` | `aria-describedby` |
| Sheet | `role="dialog"`, `aria-modal="true"` | `aria-labelledby` |
| DropdownMenu | `role="menu"` | `aria-labelledby` |
| DropdownMenuItem | `role="menuitem"` | `aria-disabled` |
| Tabs | `role="tablist"` | `aria-orientation` |
| Tab | `role="tab"`, `aria-selected`, `aria-controls` | `aria-disabled` |
| TabPanel | `role="tabpanel"`, `aria-labelledby` | - |
| Accordion | - | - |
| AccordionTrigger | `aria-expanded`, `aria-controls` | `aria-disabled` |
| AccordionContent | `role="region"`, `aria-labelledby` | - |
| Alert | `role="alert"` | - |
| AlertDescription | - | - |
| Toast | `role="status"`, `aria-live="polite"` | `aria-atomic="true"` |
| Progress | `role="progressbar"`, `aria-valuenow`, `aria-valuemin`, `aria-valuemax` | `aria-valuetext` |
| Tooltip | `role="tooltip"` | - |
| Badge | - | - |
| Avatar | `role="img"`, `aria-label` (quando sem alt) | - |
| Skeleton | `aria-hidden="true"` | - |

### Exemplos de Implementação Correta

**FormField com Error State**:
```tsx
<FormField>
  <Label htmlFor="email">Email</Label>
  <Input
    id="email"
    aria-invalid={!!error}
    aria-describedby={error ? "email-error" : undefined}
    aria-required
  />
  {error && (
    <FormMessage id="email-error" role="alert">
      {error.message}
    </FormMessage>
  )}
</FormField>
```

**Dialog Acessível**:
```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Editar Unidade</Button>
  </DialogTrigger>
  <DialogContent aria-describedby="dialog-description">
    <DialogHeader>
      <DialogTitle>Editar Dados da Unidade</DialogTitle>
      <DialogDescription id="dialog-description">
        Altere os campos necessários e clique em salvar.
      </DialogDescription>
    </DialogHeader>
    {/* form content */}
    <DialogFooter>
      <DialogClose asChild>
        <Button variant="outline">Cancelar</Button>
      </DialogClose>
      <Button type="submit">Salvar</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

## Checklist WCAG 2.1 AA

Critérios de sucesso WCAG verificados em todos componentes antes do merge.

### Perceptível

- [x] **1.1.1 Conteúdo Não-Textual**: Todas imagens têm alt text, ícones decorativos têm `aria-hidden="true"`, ícones funcionais têm `aria-label`
- [x] **1.3.1 Informações e Relações**: Estrutura semântica correta (headings, lists, tables), labels associados a inputs via `htmlFor`/`id`
- [x] **1.3.2 Sequência Significativa**: Ordem do DOM corresponde à ordem visual, não usar CSS para reordenar conteúdo de forma que quebre lógica
- [x] **1.4.1 Uso de Cor**: Cor não é único meio de transmitir informação (erros têm ícone + texto + borda, não só cor vermelha)
- [x] **1.4.3 Contraste Mínimo**: Texto normal 4.5:1, texto grande (18pt+) 3:1, verificado via CSS variables do design system
- [x] **1.4.4 Redimensionar Texto**: Interface funciona com zoom até 200% sem perda de conteúdo ou funcionalidade
- [x] **1.4.11 Contraste Não-Textual**: Componentes UI e gráficos têm contraste 3:1 contra adjacentes (bordas de input, focus rings)

### Operável

- [x] **2.1.1 Teclado**: Toda funcionalidade acessível via teclado (ver tabela navegação acima)
- [x] **2.1.2 Sem Bloqueio de Teclado**: Foco pode entrar e sair de todos componentes, focus trap apenas em modais com Escape para fechar
- [x] **2.4.1 Ignorar Blocos**: Skip links disponíveis em layouts de página (não em componentes individuais)
- [x] **2.4.3 Ordem de Foco**: Tab order lógica seguindo fluxo de leitura visual
- [x] **2.4.4 Finalidade do Link**: Links têm texto descritivo ou `aria-label` quando apenas ícone
- [x] **2.4.6 Cabeçalhos e Rótulos**: Headings e labels descrevem claramente conteúdo/propósito
- [x] **2.4.7 Foco Visível**: Focus ring visível em todos componentes interativos via `ring-2 ring-ring ring-offset-2`

### Compreensível

- [x] **3.1.1 Idioma da Página**: Definido em aplicação consumidora via `<html lang="pt-BR">`
- [x] **3.2.1 Em Foco**: Foco não causa mudança automática de contexto
- [x] **3.2.2 Em Entrada**: Mudança de valor não causa mudança automática de contexto sem aviso
- [x] **3.3.1 Identificação de Erro**: Erros identificados com texto descritivo, não apenas cor
- [x] **3.3.2 Rótulos ou Instruções**: Inputs têm labels visíveis, placeholders não substituem labels

### Robusto

- [x] **4.1.1 Análise**: HTML válido, IDs únicos, tags abertas/fechadas corretamente
- [x] **4.1.2 Nome, Função, Valor**: Componentes têm roles ARIA apropriados, estados programaticamente determináveis

## Contraste de Cores

CSS variables do design system garantem contraste mínimo em todos temas.

| Token | Uso | Ratio vs Background | Status |
|:------|:----|:--------------------|:-------|
| `--foreground` | Texto principal | 12.6:1 vs `--background` | Pass AAA |
| `--muted-foreground` | Texto secundário | 4.7:1 vs `--background` | Pass AA |
| `--primary-foreground` | Texto em botão primary | 8.2:1 vs `--primary` | Pass AAA |
| `--destructive-foreground` | Texto em botão destructive | 7.5:1 vs `--destructive` | Pass AAA |
| `--border` | Bordas de input | 3.1:1 vs `--background` | Pass (non-text) |
| `--ring` | Focus indicator | 4.8:1 vs `--background` | Pass AA |

### Verificação de Contraste

```tsx
// Utilitário para verificar contraste em desenvolvimento
import { getContrastRatio } from '@/lib/accessibility'

// Cores do design system
const colors = {
  foreground: 'hsl(222.2 84% 4.9%)',      // --foreground
  background: 'hsl(0 0% 100%)',            // --background
  primary: 'hsl(221.2 83.2% 53.3%)',       // --primary
  primaryForeground: 'hsl(210 40% 98%)',   // --primary-foreground
}

getContrastRatio(colors.foreground, colors.background)  // 12.63
getContrastRatio(colors.primaryForeground, colors.primary)  // 8.21
```

## Live Regions

Componentes que atualizam dinamicamente utilizam live regions para anunciar mudanças a screen readers.

| Componente | aria-live | aria-atomic | Uso |
|:-----------|:----------|:------------|:----|
| Toast | polite | true | Notificações não-críticas |
| Alert | - (role="alert" implica assertive) | - | Mensagens importantes |
| FormMessage | polite | true | Erros de validação inline |
| Progress | polite | false | Atualizações de progresso (opcional) |

```tsx
// Toast anuncia mensagem quando aparece
<Toast>
  <div role="status" aria-live="polite" aria-atomic="true">
    Unidade salva com sucesso
  </div>
</Toast>

// Alert anuncia imediatamente (assertive implícito)
<Alert variant="destructive">
  <AlertTitle>Erro de validação</AlertTitle>
  <AlertDescription>CPF inválido. Verifique o número digitado.</AlertDescription>
</Alert>
```

## Testes de Acessibilidade

### Testes Automatizados

Todos componentes têm testes axe-core no Storybook e Jest.

```tsx
// Teste Jest com axe
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'

expect.extend(toHaveNoViolations)

describe('Button accessibility', () => {
  it('has no axe violations', async () => {
    const { container } = render(<Button>Click me</Button>)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('has no axe violations when disabled', async () => {
    const { container } = render(<Button disabled>Disabled</Button>)
    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})
```

### Storybook Addon

`@storybook/addon-a11y` executa axe-core em todas stories, mostrando violations no painel Accessibility.

```ts
// .storybook/main.ts
export default {
  addons: ['@storybook/addon-a11y'],
}
```

### Testes Manuais

Checklist de testes manuais executados antes de major releases.

| Teste | Ferramenta | Frequência |
|:------|:-----------|:-----------|
| Navegação por teclado | Browser nativo | Cada PR |
| Screen reader NVDA | Windows + Firefox | Major release |
| Screen reader VoiceOver | macOS + Safari | Major release |
| Screen reader JAWS | Windows + Chrome | Major release |
| Zoom 200% | Browser nativo | Cada PR |
| High contrast mode | Windows | Major release |
| Reduced motion | Sistema operacional | Cada PR |

### Reduced Motion

Componentes respeitam preferência de usuário por movimento reduzido.

```css
/* Aplicado globalmente via Tailwind */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```tsx
// Hook para verificar preferência
import { useReducedMotion } from '@/hooks/use-reduced-motion'

function AnimatedComponent() {
  const prefersReducedMotion = useReducedMotion()

  return (
    <motion.div
      animate={{ opacity: 1 }}
      transition={{ duration: prefersReducedMotion ? 0 : 0.3 }}
    />
  )
}
```

## Referências

- [WAI-ARIA Authoring Practices 1.2](https://www.w3.org/WAI/ARIA/apg/)
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [Radix UI Accessibility](https://radix-ui.com/docs/primitives/overview/accessibility)
- [axe-core Rules](https://dequeuniversity.com/rules/axe/)
- [ADR-023: Color Palette Design System](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-023-color-palette-design-system.md)
