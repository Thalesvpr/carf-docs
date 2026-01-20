---
status: approved
updated: 2026-01-20
---

# Form Components

Componentes de formulario baseados em Radix UI com estilizacao CARF.

## Button

Botao interativo com variantes semanticas e tamanhos.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| variant | `'default' \| 'destructive' \| 'outline' \| 'secondary' \| 'ghost' \| 'link' \| 'success' \| 'warning'` | `'default'` | Estilo visual |
| size | `'default' \| 'sm' \| 'lg' \| 'icon'` | `'default'` | Tamanho |
| asChild | `boolean` | `false` | Renderiza como filho (Slot pattern) |
| disabled | `boolean` | `false` | Estado desabilitado |

### Variants

| Variant | Cor | Uso |
|:--------|:----|:----|
| default | Verde primario (#2C5F2D) | Acao principal |
| destructive | Vermelho | Excluir, cancelar |
| outline | Borda cinza | Acao secundaria |
| secondary | Cinza | Acao terciaria |
| ghost | Transparente | Acoes sutis |
| link | Azul sublinhado | Links inline |
| success | Verde (#15981C) | Confirmacao positiva |
| warning | Amarelo (#FFCD07) | Alerta |

### Examples

```tsx
import { Button } from '@carf/ui'

// Basico
<Button>Salvar</Button>

// Variantes
<Button variant="destructive">Excluir</Button>
<Button variant="outline">Cancelar</Button>
<Button variant="success">Aprovar</Button>

// Tamanhos
<Button size="sm">Pequeno</Button>
<Button size="lg">Grande</Button>
<Button size="icon"><IconSearch /></Button>

// Estados
<Button disabled>Desabilitado</Button>
<Button asChild><a href="/link">Como Link</a></Button>
```

## Input

Campo de texto com suporte a estados e integracao com Label.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| type | `string` | `'text'` | Tipo do input (text, email, password, etc) |
| placeholder | `string` | - | Placeholder |
| disabled | `boolean` | `false` | Estado desabilitado |
| className | `string` | - | Classes adicionais |

### Examples

```tsx
import { Input, Label } from '@carf/ui'

// Basico
<Input placeholder="Digite seu nome" />

// Com Label
<div className="space-y-2">
  <Label htmlFor="email">E-mail</Label>
  <Input id="email" type="email" placeholder="email@exemplo.com" />
</div>

// Com erro (via className)
<Input className="border-carf-accent" />
```

## Label

Label acessivel para inputs.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| htmlFor | `string` | - | ID do input associado |

### Examples

```tsx
import { Label, Input } from '@carf/ui'

<Label htmlFor="cpf">CPF</Label>
<Input id="cpf" />
```

## Checkbox

Checkbox acessivel com Radix UI.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| checked | `boolean \| 'indeterminate'` | - | Estado marcado |
| onCheckedChange | `(checked: boolean) => void` | - | Callback de mudanca |
| disabled | `boolean` | `false` | Estado desabilitado |

### Examples

```tsx
import { Checkbox, Label } from '@carf/ui'

<div className="flex items-center gap-2">
  <Checkbox id="terms" />
  <Label htmlFor="terms">Aceito os termos</Label>
</div>

// Controlado
const [checked, setChecked] = useState(false)
<Checkbox checked={checked} onCheckedChange={setChecked} />
```

## Switch

Toggle on/off.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| checked | `boolean` | - | Estado ligado |
| onCheckedChange | `(checked: boolean) => void` | - | Callback de mudanca |
| disabled | `boolean` | `false` | Estado desabilitado |

### Examples

```tsx
import { Switch, Label } from '@carf/ui'

<div className="flex items-center gap-2">
  <Switch id="notifications" />
  <Label htmlFor="notifications">Notificacoes</Label>
</div>
```

## Select

Dropdown acessivel com compound components.

### Components

| Componente | Descricao |
|:-----------|:----------|
| Select | Container root |
| SelectTrigger | Botao que abre o dropdown |
| SelectValue | Valor selecionado |
| SelectContent | Container das opcoes |
| SelectItem | Opcao individual |
| SelectGroup | Grupo de opcoes |
| SelectLabel | Label do grupo |
| SelectSeparator | Separador visual |

### Examples

```tsx
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@carf/ui'

<Select>
  <SelectTrigger className="w-[200px]">
    <SelectValue placeholder="Selecione..." />
  </SelectTrigger>
  <SelectContent>
    <SelectItem value="pending">Pendente</SelectItem>
    <SelectItem value="approved">Aprovado</SelectItem>
    <SelectItem value="rejected">Rejeitado</SelectItem>
  </SelectContent>
</Select>
```

## Textarea

Campo de texto multilinhas.

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| placeholder | `string` | - | Placeholder |
| rows | `number` | - | Numero de linhas |
| disabled | `boolean` | `false` | Estado desabilitado |

### Examples

```tsx
import { Textarea, Label } from '@carf/ui'

<div className="space-y-2">
  <Label htmlFor="obs">Observacoes</Label>
  <Textarea id="obs" placeholder="Digite observacoes..." rows={4} />
</div>
```
