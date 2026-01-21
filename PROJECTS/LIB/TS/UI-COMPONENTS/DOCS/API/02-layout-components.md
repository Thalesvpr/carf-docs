---
title: "Layout Components - @carf/ui"
status: review
updated: 2026-01-21
source: "interno"
---

# Layout Components - @carf/ui

Componentes para estruturacao e organizacao de conteudo.

## Card

Container com borda e sombra para agrupar conteudo relacionado.

### Importacao

```tsx
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '@carf/ui'
```

### Anatomia

```tsx
<Card>
  <CardHeader>
    <CardTitle>Titulo</CardTitle>
    <CardDescription>Descricao opcional</CardDescription>
  </CardHeader>
  <CardContent>
    Conteudo principal
  </CardContent>
  <CardFooter>
    Acoes ou informacoes adicionais
  </CardFooter>
</Card>
```

### Props

#### Card

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| className | string | - | Classes CSS adicionais |
| asChild | boolean | false | Renderizar como filho |

### Exemplos

```tsx
// Card simples
<Card>
  <CardHeader>
    <CardTitle>Unidade UN-001</CardTitle>
    <CardDescription>Rua das Flores, 123</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Area: 250m²</p>
    <p>Posseiros: 2</p>
  </CardContent>
</Card>

// Card com acoes
<Card>
  <CardHeader>
    <CardTitle>Configuracoes</CardTitle>
  </CardHeader>
  <CardContent>
    <form>...</form>
  </CardContent>
  <CardFooter className="flex justify-end gap-2">
    <Button variant="outline">Cancelar</Button>
    <Button>Salvar</Button>
  </CardFooter>
</Card>
```

---

## Separator

Linha divisoria visual entre secoes de conteudo.

### Importacao

```tsx
import { Separator } from '@carf/ui'
```

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| orientation | 'horizontal' \| 'vertical' | 'horizontal' | Direcao do separador |
| decorative | boolean | true | Se e decorativo (sem semantica) |
| className | string | - | Classes CSS adicionais |

### Exemplos

```tsx
// Horizontal (padrao)
<div>
  <p>Secao 1</p>
  <Separator className="my-4" />
  <p>Secao 2</p>
</div>

// Vertical
<div className="flex h-5 items-center space-x-4">
  <span>Item 1</span>
  <Separator orientation="vertical" />
  <span>Item 2</span>
  <Separator orientation="vertical" />
  <span>Item 3</span>
</div>
```

---

## Tabs

Navegacao em abas para alternar entre paineis de conteudo.

### Importacao

```tsx
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@carf/ui'
```

### Props

#### Tabs

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| defaultValue | string | - | Valor inicial da aba ativa |
| value | string | - | Valor controlado |
| onValueChange | (value: string) => void | - | Callback ao mudar aba |

#### TabsTrigger

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| value | string | obrigatorio | Identificador unico da aba |
| disabled | boolean | false | Desabilitar aba |

#### TabsContent

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| value | string | obrigatorio | Corresponde ao TabsTrigger |
| forceMount | boolean | false | Manter montado mesmo inativo |

### Exemplos

```tsx
// Tabs basico
<Tabs defaultValue="dados">
  <TabsList>
    <TabsTrigger value="dados">Dados</TabsTrigger>
    <TabsTrigger value="documentos">Documentos</TabsTrigger>
    <TabsTrigger value="historico">Historico</TabsTrigger>
  </TabsList>
  <TabsContent value="dados">
    <Card>
      <CardContent>Formulario de dados...</CardContent>
    </Card>
  </TabsContent>
  <TabsContent value="documentos">
    <Card>
      <CardContent>Lista de documentos...</CardContent>
    </Card>
  </TabsContent>
  <TabsContent value="historico">
    <Card>
      <CardContent>Timeline de eventos...</CardContent>
    </Card>
  </TabsContent>
</Tabs>

// Tabs controlado
function ControlledTabs() {
  const [tab, setTab] = useState('dados')

  return (
    <Tabs value={tab} onValueChange={setTab}>
      <TabsList>
        <TabsTrigger value="dados">Dados</TabsTrigger>
        <TabsTrigger value="mapa">Mapa</TabsTrigger>
      </TabsList>
      <TabsContent value="dados">...</TabsContent>
      <TabsContent value="mapa">...</TabsContent>
    </Tabs>
  )
}
```

---

## Accordion

Paineis expansiveis para mostrar/ocultar conteudo.

### Importacao

```tsx
import { Accordion, AccordionItem, AccordionTrigger, AccordionContent } from '@carf/ui'
```

### Props

#### Accordion

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| type | 'single' \| 'multiple' | 'single' | Um ou varios abertos |
| collapsible | boolean | false | Permitir fechar todos (type='single') |
| defaultValue | string \| string[] | - | Itens abertos inicialmente |
| value | string \| string[] | - | Valor controlado |
| onValueChange | (value) => void | - | Callback ao mudar |

#### AccordionItem

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| value | string | obrigatorio | Identificador unico |
| disabled | boolean | false | Desabilitar item |

### Exemplos

```tsx
// Accordion simples
<Accordion type="single" collapsible>
  <AccordionItem value="endereco">
    <AccordionTrigger>Endereco</AccordionTrigger>
    <AccordionContent>
      <p>Rua das Flores, 123</p>
      <p>Centro - Cidade/UF</p>
    </AccordionContent>
  </AccordionItem>
  <AccordionItem value="documentos">
    <AccordionTrigger>Documentos</AccordionTrigger>
    <AccordionContent>
      <ul>
        <li>RG - Verificado</li>
        <li>CPF - Verificado</li>
      </ul>
    </AccordionContent>
  </AccordionItem>
</Accordion>

// Multiplos abertos
<Accordion type="multiple" defaultValue={['item-1', 'item-2']}>
  <AccordionItem value="item-1">
    <AccordionTrigger>Primeiro</AccordionTrigger>
    <AccordionContent>Conteudo 1</AccordionContent>
  </AccordionItem>
  <AccordionItem value="item-2">
    <AccordionTrigger>Segundo</AccordionTrigger>
    <AccordionContent>Conteudo 2</AccordionContent>
  </AccordionItem>
</Accordion>
```

---

## ScrollArea

Area de scroll customizada com scrollbars estilizados.

### Importacao

```tsx
import { ScrollArea, ScrollBar } from '@carf/ui'
```

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| className | string | - | Classes CSS adicionais |
| type | 'auto' \| 'always' \| 'scroll' \| 'hover' | 'hover' | Quando mostrar scrollbar |

### Exemplos

```tsx
// Scroll vertical
<ScrollArea className="h-72 w-48 rounded-md border">
  <div className="p-4">
    {items.map((item) => (
      <div key={item.id} className="py-2">
        {item.name}
      </div>
    ))}
  </div>
</ScrollArea>

// Scroll horizontal
<ScrollArea className="w-96 whitespace-nowrap rounded-md border">
  <div className="flex w-max space-x-4 p-4">
    {images.map((image) => (
      <img key={image.id} src={image.url} className="h-32 w-32" />
    ))}
  </div>
  <ScrollBar orientation="horizontal" />
</ScrollArea>
```

---

## Aspectos de Acessibilidade

### Card
- Usar `<article>` se o card representa conteudo independente
- Garantir hierarquia de headings correta

### Separator
- `decorative={false}` adiciona `role="separator"` para leitores de tela

### Tabs
- Navegacao por teclado automatica (setas)
- `aria-selected` e `aria-controls` gerenciados automaticamente

### Accordion
- `aria-expanded` gerenciado automaticamente
- Navegacao por teclado (Enter/Space para toggle)
