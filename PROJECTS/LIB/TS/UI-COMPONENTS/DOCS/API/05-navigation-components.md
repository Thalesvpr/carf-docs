---
title: "Navigation Components - @carf/ui"
status: review
updated: 2026-01-21
source: "interno"
---

# Navigation Components - @carf/ui

Componentes para navegacao e menus.

## DropdownMenu

Menu suspenso acionado por clique.

### Importacao

```tsx
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioItem,
  DropdownMenuRadioGroup,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuGroup,
  DropdownMenuSub,
  DropdownMenuSubTrigger,
  DropdownMenuSubContent,
} from '@carf/ui'
```

### Props

#### DropdownMenuContent

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| side | 'top' \| 'right' \| 'bottom' \| 'left' | 'bottom' | Posicao |
| sideOffset | number | 4 | Distancia do trigger |
| align | 'start' \| 'center' \| 'end' | 'start' | Alinhamento |

#### DropdownMenuItem

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| disabled | boolean | false | Desabilitar item |
| onSelect | () => void | - | Callback ao selecionar |

### Exemplos

```tsx
// Menu basico
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">Acoes</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuItem onClick={handleEdit}>
      <Pencil className="mr-2 h-4 w-4" />
      Editar
    </DropdownMenuItem>
    <DropdownMenuItem onClick={handleDuplicate}>
      <Copy className="mr-2 h-4 w-4" />
      Duplicar
    </DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem
      onClick={handleDelete}
      className="text-destructive"
    >
      <Trash className="mr-2 h-4 w-4" />
      Excluir
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>

// Menu com grupos
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="icon">
      <MoreHorizontal className="h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent className="w-56">
    <DropdownMenuLabel>Minha Conta</DropdownMenuLabel>
    <DropdownMenuSeparator />
    <DropdownMenuGroup>
      <DropdownMenuItem>
        <User className="mr-2 h-4 w-4" />
        Perfil
        <DropdownMenuShortcut>⇧⌘P</DropdownMenuShortcut>
      </DropdownMenuItem>
      <DropdownMenuItem>
        <Settings className="mr-2 h-4 w-4" />
        Configuracoes
        <DropdownMenuShortcut>⌘,</DropdownMenuShortcut>
      </DropdownMenuItem>
    </DropdownMenuGroup>
    <DropdownMenuSeparator />
    <DropdownMenuItem>
      <LogOut className="mr-2 h-4 w-4" />
      Sair
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>

// Menu com checkbox
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="outline">Colunas</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuLabel>Colunas visiveis</DropdownMenuLabel>
    <DropdownMenuSeparator />
    {columns.map((col) => (
      <DropdownMenuCheckboxItem
        key={col.id}
        checked={col.visible}
        onCheckedChange={(checked) => toggleColumn(col.id, checked)}
      >
        {col.label}
      </DropdownMenuCheckboxItem>
    ))}
  </DropdownMenuContent>
</DropdownMenu>

// Submenu
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button>Menu</Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    <DropdownMenuSub>
      <DropdownMenuSubTrigger>
        <Share className="mr-2 h-4 w-4" />
        Compartilhar
      </DropdownMenuSubTrigger>
      <DropdownMenuSubContent>
        <DropdownMenuItem>Email</DropdownMenuItem>
        <DropdownMenuItem>WhatsApp</DropdownMenuItem>
        <DropdownMenuItem>Link</DropdownMenuItem>
      </DropdownMenuSubContent>
    </DropdownMenuSub>
  </DropdownMenuContent>
</DropdownMenu>
```

---

## Command

Paleta de comandos com busca (estilo Ctrl+K).

### Importacao

```tsx
import {
  Command,
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandShortcut,
  CommandSeparator,
} from '@carf/ui'
```

### Exemplos

```tsx
// Command inline
<Command className="rounded-lg border shadow-md">
  <CommandInput placeholder="Buscar..." />
  <CommandList>
    <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>
    <CommandGroup heading="Sugestoes">
      <CommandItem>
        <Calendar className="mr-2 h-4 w-4" />
        Calendario
      </CommandItem>
      <CommandItem>
        <Smile className="mr-2 h-4 w-4" />
        Buscar Emoji
      </CommandItem>
    </CommandGroup>
  </CommandList>
</Command>

// Command dialog (Ctrl+K)
function CommandMenu() {
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        setOpen((open) => !open)
      }
    }
    document.addEventListener('keydown', down)
    return () => document.removeEventListener('keydown', down)
  }, [])

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Digite um comando ou busque..." />
      <CommandList>
        <CommandEmpty>Nenhum resultado.</CommandEmpty>
        <CommandGroup heading="Navegacao">
          <CommandItem onSelect={() => navigate('/units')}>
            <Home className="mr-2 h-4 w-4" />
            Unidades
            <CommandShortcut>⌘U</CommandShortcut>
          </CommandItem>
          <CommandItem onSelect={() => navigate('/holders')}>
            <Users className="mr-2 h-4 w-4" />
            Posseiros
            <CommandShortcut>⌘H</CommandShortcut>
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Acoes">
          <CommandItem onSelect={() => openCreateUnit()}>
            <Plus className="mr-2 h-4 w-4" />
            Nova Unidade
            <CommandShortcut>⌘N</CommandShortcut>
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  )
}
```

---

## Breadcrumb

Navegacao hierarquica mostrando localizacao atual.

### Importacao

```tsx
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
  BreadcrumbEllipsis,
} from '@carf/ui'
```

### Exemplos

```tsx
// Breadcrumb basico
<Breadcrumb>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/units">Unidades</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbPage>UN-001</BreadcrumbPage>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumb>

// Com ellipsis (muitos niveis)
<Breadcrumb>
  <BreadcrumbList>
    <BreadcrumbItem>
      <BreadcrumbLink href="/">Home</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbEllipsis />
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbLink href="/communities/A">Comunidade A</BreadcrumbLink>
    </BreadcrumbItem>
    <BreadcrumbSeparator />
    <BreadcrumbItem>
      <BreadcrumbPage>Unidade UN-001</BreadcrumbPage>
    </BreadcrumbItem>
  </BreadcrumbList>
</Breadcrumb>

// Dinamico
function DynamicBreadcrumb({ items }: { items: BreadcrumbItem[] }) {
  return (
    <Breadcrumb>
      <BreadcrumbList>
        {items.map((item, index) => (
          <React.Fragment key={item.href || item.label}>
            {index > 0 && <BreadcrumbSeparator />}
            <BreadcrumbItem>
              {index === items.length - 1 ? (
                <BreadcrumbPage>{item.label}</BreadcrumbPage>
              ) : (
                <BreadcrumbLink href={item.href}>{item.label}</BreadcrumbLink>
              )}
            </BreadcrumbItem>
          </React.Fragment>
        ))}
      </BreadcrumbList>
    </Breadcrumb>
  )
}
```

---

## NavigationMenu

Menu de navegacao horizontal com dropdowns.

### Importacao

```tsx
import {
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuTrigger,
  NavigationMenuContent,
  NavigationMenuLink,
  navigationMenuTriggerStyle,
} from '@carf/ui'
```

### Exemplos

```tsx
<NavigationMenu>
  <NavigationMenuList>
    <NavigationMenuItem>
      <NavigationMenuTrigger>Cadastros</NavigationMenuTrigger>
      <NavigationMenuContent>
        <ul className="grid w-[400px] gap-3 p-4 md:grid-cols-2">
          <li>
            <NavigationMenuLink asChild>
              <a href="/units" className="block p-3 rounded-md hover:bg-accent">
                <div className="font-medium">Unidades</div>
                <p className="text-sm text-muted-foreground">
                  Gerenciar unidades territoriais
                </p>
              </a>
            </NavigationMenuLink>
          </li>
          <li>
            <NavigationMenuLink asChild>
              <a href="/holders" className="block p-3 rounded-md hover:bg-accent">
                <div className="font-medium">Posseiros</div>
                <p className="text-sm text-muted-foreground">
                  Gerenciar cadastro de posseiros
                </p>
              </a>
            </NavigationMenuLink>
          </li>
        </ul>
      </NavigationMenuContent>
    </NavigationMenuItem>
    <NavigationMenuItem>
      <NavigationMenuLink className={navigationMenuTriggerStyle()} href="/map">
        Mapa
      </NavigationMenuLink>
    </NavigationMenuItem>
  </NavigationMenuList>
</NavigationMenu>
```

---

## Pagination

Navegacao entre paginas de dados.

### Importacao

```tsx
import {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
  PaginationEllipsis,
} from '@carf/ui'
```

### Exemplos

```tsx
// Paginacao basica
<Pagination>
  <PaginationContent>
    <PaginationItem>
      <PaginationPrevious href="#" />
    </PaginationItem>
    <PaginationItem>
      <PaginationLink href="#">1</PaginationLink>
    </PaginationItem>
    <PaginationItem>
      <PaginationLink href="#" isActive>2</PaginationLink>
    </PaginationItem>
    <PaginationItem>
      <PaginationLink href="#">3</PaginationLink>
    </PaginationItem>
    <PaginationItem>
      <PaginationEllipsis />
    </PaginationItem>
    <PaginationItem>
      <PaginationNext href="#" />
    </PaginationItem>
  </PaginationContent>
</Pagination>

// Paginacao controlada
function ControlledPagination({ page, totalPages, onPageChange }) {
  const pages = generatePageNumbers(page, totalPages)

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            onClick={() => onPageChange(page - 1)}
            disabled={page === 1}
          />
        </PaginationItem>
        {pages.map((p, i) => (
          <PaginationItem key={i}>
            {p === '...' ? (
              <PaginationEllipsis />
            ) : (
              <PaginationLink
                isActive={p === page}
                onClick={() => onPageChange(p)}
              >
                {p}
              </PaginationLink>
            )}
          </PaginationItem>
        ))}
        <PaginationItem>
          <PaginationNext
            onClick={() => onPageChange(page + 1)}
            disabled={page === totalPages}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )
}
```

---

## Aspectos de Acessibilidade

### DropdownMenu
- Navegacao por teclado (setas, Enter, Escape)
- `role="menu"` e `role="menuitem"` automaticos
- Focus management automatico

### Command
- Filtragem por teclado integrada
- Anuncio de resultados para leitores de tela
- Navegacao por setas

### Breadcrumb
- `nav` com `aria-label="Breadcrumb"`
- Link atual marcado com `aria-current="page"`
- Separadores decorativos (ignorados por leitores)

### Pagination
- `nav` com `aria-label="Pagination"`
- Pagina atual marcada com `aria-current="page"`
- Links desabilitados com `aria-disabled`
