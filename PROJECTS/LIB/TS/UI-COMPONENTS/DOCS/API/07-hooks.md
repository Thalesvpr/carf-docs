---
title: "Hooks - @carf/ui"
status: review
updated: 2026-01-21
source: "interno"
---

# Hooks - @carf/ui

React hooks utilitarios para uso comum em aplicacoes.

## useTheme

Gerencia tema (light/dark/system) com persistencia.

### Importacao

```tsx
import { useTheme } from '@carf/ui'
```

### Retorno

| Propriedade | Tipo | Descricao |
|:------------|:-----|:----------|
| theme | 'light' \| 'dark' \| 'system' | Tema atual configurado |
| setTheme | (theme) => void | Altera o tema |
| resolvedTheme | 'light' \| 'dark' | Tema efetivo aplicado |

### Uso

```tsx
function ThemeToggle() {
  const { theme, setTheme, resolvedTheme } = useTheme()

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
    >
      {resolvedTheme === 'dark' ? (
        <Sun className="h-4 w-4" />
      ) : (
        <Moon className="h-4 w-4" />
      )}
    </Button>
  )
}

// Dropdown com opcoes
function ThemeSelector() {
  const { theme, setTheme } = useTheme()

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">Tema: {theme}</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuRadioGroup value={theme} onValueChange={setTheme}>
          <DropdownMenuRadioItem value="light">Light</DropdownMenuRadioItem>
          <DropdownMenuRadioItem value="dark">Dark</DropdownMenuRadioItem>
          <DropdownMenuRadioItem value="system">Sistema</DropdownMenuRadioItem>
        </DropdownMenuRadioGroup>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
```

### Requisito

Requer `ThemeProvider` no root da aplicacao:

```tsx
import { ThemeProvider } from '@carf/ui'

function App() {
  return (
    <ThemeProvider defaultTheme="system">
      <MyApp />
    </ThemeProvider>
  )
}
```

---

## useMediaQuery

Detecta se uma media query corresponde ao viewport atual.

### Importacao

```tsx
import { useMediaQuery } from '@carf/ui'
```

### Parametros

| Parametro | Tipo | Descricao |
|:----------|:-----|:----------|
| query | string | Media query CSS |

### Retorno

| Tipo | Descricao |
|:-----|:----------|
| boolean | Se a media query corresponde |

### Uso

```tsx
function ResponsiveComponent() {
  const isMobile = useMediaQuery('(max-width: 768px)')
  const isTablet = useMediaQuery('(min-width: 769px) and (max-width: 1024px)')
  const isDesktop = useMediaQuery('(min-width: 1025px)')
  const prefersDark = useMediaQuery('(prefers-color-scheme: dark)')
  const prefersReducedMotion = useMediaQuery('(prefers-reduced-motion: reduce)')

  if (isMobile) {
    return <MobileLayout />
  }

  return <DesktopLayout />
}

// Layout responsivo
function Navigation() {
  const isMobile = useMediaQuery('(max-width: 768px)')

  return isMobile ? <MobileNav /> : <DesktopNav />
}

// Condicional em render
function DataTable({ data }) {
  const isSmall = useMediaQuery('(max-width: 640px)')

  return isSmall ? (
    <CardList data={data} />
  ) : (
    <Table data={data} />
  )
}
```

### Implementacao

```tsx
export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false)

  useEffect(() => {
    const media = window.matchMedia(query)
    setMatches(media.matches)

    const listener = (e: MediaQueryListEvent) => setMatches(e.matches)
    media.addEventListener('change', listener)

    return () => media.removeEventListener('change', listener)
  }, [query])

  return matches
}
```

---

## useDebounce

Atrasa atualizacao de valor ate parar de mudar.

### Importacao

```tsx
import { useDebounce } from '@carf/ui'
```

### Parametros

| Parametro | Tipo | Default | Descricao |
|:----------|:-----|:--------|:----------|
| value | T | - | Valor a ser debounced |
| delay | number | 500 | Delay em ms |

### Retorno

| Tipo | Descricao |
|:-----|:----------|
| T | Valor debounced |

### Uso

```tsx
function SearchInput() {
  const [search, setSearch] = useState('')
  const debouncedSearch = useDebounce(search, 300)

  // Busca so executa apos 300ms sem digitar
  useEffect(() => {
    if (debouncedSearch) {
      fetchResults(debouncedSearch)
    }
  }, [debouncedSearch])

  return (
    <Input
      value={search}
      onChange={(e) => setSearch(e.target.value)}
      placeholder="Buscar..."
    />
  )
}

// Filtro de tabela
function FilterableTable() {
  const [filter, setFilter] = useState('')
  const debouncedFilter = useDebounce(filter, 200)

  const filteredData = useMemo(() => {
    return data.filter((item) =>
      item.name.toLowerCase().includes(debouncedFilter.toLowerCase())
    )
  }, [data, debouncedFilter])

  return (
    <>
      <Input
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
      />
      <Table data={filteredData} />
    </>
  )
}
```

### Implementacao

```tsx
export function useDebounce<T>(value: T, delay = 500): T {
  const [debouncedValue, setDebouncedValue] = useState(value)

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value)
    }, delay)

    return () => clearTimeout(timer)
  }, [value, delay])

  return debouncedValue
}
```

---

## useLocalStorage

Persiste estado no localStorage com sincronizacao entre abas.

### Importacao

```tsx
import { useLocalStorage } from '@carf/ui'
```

### Parametros

| Parametro | Tipo | Descricao |
|:----------|:-----|:----------|
| key | string | Chave do localStorage |
| initialValue | T | Valor inicial se nao existir |

### Retorno

| Propriedade | Tipo | Descricao |
|:------------|:-----|:----------|
| [0] | T | Valor atual |
| [1] | (value: T) => void | Setter |

### Uso

```tsx
function Preferences() {
  const [sidebarOpen, setSidebarOpen] = useLocalStorage('sidebar-open', true)
  const [recentItems, setRecentItems] = useLocalStorage('recent-items', [])

  return (
    <Button onClick={() => setSidebarOpen(!sidebarOpen)}>
      {sidebarOpen ? 'Fechar' : 'Abrir'} Sidebar
    </Button>
  )
}

// Com objetos
const [settings, setSettings] = useLocalStorage('user-settings', {
  notifications: true,
  language: 'pt-BR',
})

setSettings({ ...settings, notifications: false })
```

### Implementacao

```tsx
export function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === 'undefined') return initialValue
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch {
      return initialValue
    }
  })

  const setValue = (value: T | ((val: T) => T)) => {
    const valueToStore = value instanceof Function ? value(storedValue) : value
    setStoredValue(valueToStore)
    window.localStorage.setItem(key, JSON.stringify(valueToStore))
  }

  return [storedValue, setValue] as const
}
```

---

## useCopyToClipboard

Copia texto para a area de transferencia.

### Importacao

```tsx
import { useCopyToClipboard } from '@carf/ui'
```

### Retorno

| Propriedade | Tipo | Descricao |
|:------------|:-----|:----------|
| copy | (text: string) => Promise<boolean> | Funcao para copiar |
| copied | boolean | Se foi copiado recentemente |

### Uso

```tsx
function CopyButton({ text }: { text: string }) {
  const { copy, copied } = useCopyToClipboard()

  return (
    <Button
      variant="outline"
      size="sm"
      onClick={() => copy(text)}
    >
      {copied ? (
        <>
          <Check className="h-4 w-4 mr-2" />
          Copiado!
        </>
      ) : (
        <>
          <Copy className="h-4 w-4 mr-2" />
          Copiar
        </>
      )}
    </Button>
  )
}

// Copiar codigo
function CodeBlock({ code }: { code: string }) {
  const { copy, copied } = useCopyToClipboard()

  return (
    <div className="relative">
      <pre>{code}</pre>
      <Button
        className="absolute top-2 right-2"
        size="icon"
        variant="ghost"
        onClick={() => copy(code)}
      >
        {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
      </Button>
    </div>
  )
}
```

### Implementacao

```tsx
export function useCopyToClipboard(resetDelay = 2000) {
  const [copied, setCopied] = useState(false)

  const copy = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), resetDelay)
      return true
    } catch {
      return false
    }
  }

  return { copy, copied }
}
```

---

## useOnClickOutside

Detecta cliques fora de um elemento.

### Importacao

```tsx
import { useOnClickOutside } from '@carf/ui'
```

### Parametros

| Parametro | Tipo | Descricao |
|:----------|:-----|:----------|
| ref | RefObject<HTMLElement> | Ref do elemento |
| handler | (event) => void | Callback ao clicar fora |

### Uso

```tsx
function Dropdown() {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  useOnClickOutside(ref, () => setOpen(false))

  return (
    <div ref={ref}>
      <Button onClick={() => setOpen(true)}>Abrir</Button>
      {open && (
        <div className="absolute ...">
          Conteudo do dropdown
        </div>
      )}
    </div>
  )
}
```

### Implementacao

```tsx
export function useOnClickOutside(
  ref: RefObject<HTMLElement>,
  handler: (event: MouseEvent | TouchEvent) => void
) {
  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) {
        return
      }
      handler(event)
    }

    document.addEventListener('mousedown', listener)
    document.addEventListener('touchstart', listener)

    return () => {
      document.removeEventListener('mousedown', listener)
      document.removeEventListener('touchstart', listener)
    }
  }, [ref, handler])
}
```
