---
title: "Data Components - @carf/ui"
status: review
updated: 2026-01-21
source: "interno"
---

# Data Components - @carf/ui

Componentes para exibicao e organizacao de dados.

## Avatar

Exibe imagem de perfil ou iniciais do usuario.

### Importacao

```tsx
import { Avatar, AvatarImage, AvatarFallback } from '@carf/ui'
```

### Props

#### Avatar

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| className | string | - | Classes CSS (tamanho) |

#### AvatarImage

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| src | string | - | URL da imagem |
| alt | string | - | Texto alternativo |

#### AvatarFallback

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| delayMs | number | 600 | Delay antes de mostrar fallback |

### Exemplos

```tsx
// Avatar com imagem
<Avatar>
  <AvatarImage src="/avatar.jpg" alt="Joao Silva" />
  <AvatarFallback>JS</AvatarFallback>
</Avatar>

// Avatar com fallback
<Avatar>
  <AvatarImage src="/inexistente.jpg" alt="Usuario" />
  <AvatarFallback>US</AvatarFallback>
</Avatar>

// Tamanhos
<Avatar className="h-6 w-6">...</Avatar>   {/* Pequeno */}
<Avatar className="h-10 w-10">...</Avatar> {/* Medio (padrao) */}
<Avatar className="h-16 w-16">...</Avatar> {/* Grande */}

// Lista de avatares
<div className="flex -space-x-2">
  {users.map((user) => (
    <Avatar key={user.id} className="border-2 border-background">
      <AvatarImage src={user.avatar} alt={user.name} />
      <AvatarFallback>{getInitials(user.name)}</AvatarFallback>
    </Avatar>
  ))}
</div>
```

---

## Badge

Rotulos pequenos para status, categorias ou contagens.

### Importacao

```tsx
import { Badge } from '@carf/ui'
```

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| variant | 'default' \| 'secondary' \| 'destructive' \| 'outline' | 'default' | Estilo visual |
| className | string | - | Classes CSS adicionais |

### Exemplos

```tsx
// Variantes
<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="destructive">Destructive</Badge>
<Badge variant="outline">Outline</Badge>

// Status
<Badge className="bg-success text-white">Aprovado</Badge>
<Badge className="bg-warning text-black">Pendente</Badge>
<Badge className="bg-error text-white">Rejeitado</Badge>

// Com contagem
<div className="relative">
  <Bell className="h-5 w-5" />
  <Badge className="absolute -top-2 -right-2 h-5 w-5 p-0 flex items-center justify-center">
    3
  </Badge>
</div>
```

---

## Table

Tabela para exibicao de dados tabulares.

### Importacao

```tsx
import {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
} from '@carf/ui'
```

### Exemplos

```tsx
// Tabela basica
<Table>
  <TableCaption>Lista de unidades cadastradas</TableCaption>
  <TableHeader>
    <TableRow>
      <TableHead>Codigo</TableHead>
      <TableHead>Endereco</TableHead>
      <TableHead>Area (m²)</TableHead>
      <TableHead className="text-right">Status</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {units.map((unit) => (
      <TableRow key={unit.id}>
        <TableCell className="font-medium">{unit.code}</TableCell>
        <TableCell>{unit.address}</TableCell>
        <TableCell>{unit.area}</TableCell>
        <TableCell className="text-right">
          <Badge>{unit.status}</Badge>
        </TableCell>
      </TableRow>
    ))}
  </TableBody>
</Table>

// Com footer
<Table>
  <TableHeader>
    <TableRow>
      <TableHead>Item</TableHead>
      <TableHead className="text-right">Valor</TableHead>
    </TableRow>
  </TableHeader>
  <TableBody>
    {items.map((item) => (
      <TableRow key={item.id}>
        <TableCell>{item.name}</TableCell>
        <TableCell className="text-right">{item.value}</TableCell>
      </TableRow>
    ))}
  </TableBody>
  <TableFooter>
    <TableRow>
      <TableCell>Total</TableCell>
      <TableCell className="text-right">{total}</TableCell>
    </TableRow>
  </TableFooter>
</Table>

// Linha clicavel
<TableRow
  className="cursor-pointer hover:bg-muted"
  onClick={() => navigate(`/units/${unit.id}`)}
>
  ...
</TableRow>
```

---

## Tooltip

Dica contextual ao passar o mouse sobre elemento.

### Importacao

```tsx
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from '@carf/ui'
```

### Setup

```tsx
// No layout principal (uma vez)
import { TooltipProvider } from '@carf/ui'

export default function Layout({ children }) {
  return (
    <TooltipProvider>
      {children}
    </TooltipProvider>
  )
}
```

### Props

#### Tooltip

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| delayDuration | number | 400 | Delay antes de mostrar (ms) |
| skipDelayDuration | number | 300 | Delay ao mover entre tooltips |

#### TooltipContent

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| side | 'top' \| 'right' \| 'bottom' \| 'left' | 'top' | Posicao |
| sideOffset | number | 4 | Distancia do trigger |
| align | 'start' \| 'center' \| 'end' | 'center' | Alinhamento |

### Exemplos

```tsx
// Tooltip simples
<Tooltip>
  <TooltipTrigger asChild>
    <Button variant="outline" size="icon">
      <Settings className="h-4 w-4" />
    </Button>
  </TooltipTrigger>
  <TooltipContent>
    <p>Configuracoes</p>
  </TooltipContent>
</Tooltip>

// Posicoes
<Tooltip>
  <TooltipTrigger>Hover</TooltipTrigger>
  <TooltipContent side="right">
    Tooltip a direita
  </TooltipContent>
</Tooltip>

// Tooltip em icone de ajuda
<div className="flex items-center gap-1">
  <Label>Area total</Label>
  <Tooltip>
    <TooltipTrigger asChild>
      <HelpCircle className="h-3 w-3 text-muted-foreground" />
    </TooltipTrigger>
    <TooltipContent className="max-w-xs">
      <p>A area total e calculada automaticamente com base no poligono desenhado no mapa.</p>
    </TooltipContent>
  </Tooltip>
</div>
```

---

## Popover

Conteudo flutuante acionado por clique.

### Importacao

```tsx
import { Popover, PopoverTrigger, PopoverContent } from '@carf/ui'
```

### Props

#### PopoverContent

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| side | 'top' \| 'right' \| 'bottom' \| 'left' | 'bottom' | Posicao |
| sideOffset | number | 4 | Distancia do trigger |
| align | 'start' \| 'center' \| 'end' | 'center' | Alinhamento |

### Exemplos

```tsx
// Popover com form
<Popover>
  <PopoverTrigger asChild>
    <Button variant="outline">Filtrar</Button>
  </PopoverTrigger>
  <PopoverContent className="w-80">
    <div className="space-y-4">
      <h4 className="font-medium">Filtros</h4>
      <div className="space-y-2">
        <Label>Status</Label>
        <Select>...</Select>
      </div>
      <div className="space-y-2">
        <Label>Comunidade</Label>
        <Select>...</Select>
      </div>
      <Button className="w-full">Aplicar</Button>
    </div>
  </PopoverContent>
</Popover>

// Date picker
<Popover>
  <PopoverTrigger asChild>
    <Button variant="outline">
      <Calendar className="mr-2 h-4 w-4" />
      {date ? format(date, 'dd/MM/yyyy') : 'Selecionar data'}
    </Button>
  </PopoverTrigger>
  <PopoverContent className="w-auto p-0" align="start">
    <CalendarComponent
      selected={date}
      onSelect={setDate}
    />
  </PopoverContent>
</Popover>
```

---

## HoverCard

Card informativo ao passar mouse (preview de conteudo).

### Importacao

```tsx
import { HoverCard, HoverCardTrigger, HoverCardContent } from '@carf/ui'
```

### Exemplos

```tsx
// Preview de usuario
<HoverCard>
  <HoverCardTrigger asChild>
    <span className="cursor-pointer underline">@joaosilva</span>
  </HoverCardTrigger>
  <HoverCardContent className="w-80">
    <div className="flex space-x-4">
      <Avatar>
        <AvatarImage src="/joao.jpg" />
        <AvatarFallback>JS</AvatarFallback>
      </Avatar>
      <div>
        <h4 className="font-semibold">Joao Silva</h4>
        <p className="text-sm text-muted-foreground">
          Tecnico de campo - Comunidade A
        </p>
        <p className="text-sm mt-2">
          Cadastrou 45 unidades este mes.
        </p>
      </div>
    </div>
  </HoverCardContent>
</HoverCard>
```

---

## Aspectos de Acessibilidade

### Avatar
- `alt` obrigatorio em AvatarImage
- Fallback anunciado por leitores de tela

### Badge
- Usar cores com contraste adequado
- Considerar adicionar `aria-label` para badges so com icones

### Table
- Estrutura semantica correta (`<thead>`, `<tbody>`)
- `TableCaption` fornece descricao para leitores de tela
- Usar `scope="col"` em headers (automatico)

### Tooltip
- Mostra automaticamente ao focar trigger
- `role="tooltip"` automatico
- Conteudo anunciado por leitores de tela
