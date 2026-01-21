---
title: "Feedback Components - @carf/ui"
status: review
updated: 2026-01-21
source: "interno"
---

# Feedback Components - @carf/ui

Componentes para comunicar estados, resultados e solicitar confirmacoes.

## Alert

Exibe mensagens importantes para o usuario.

### Importacao

```tsx
import { Alert, AlertTitle, AlertDescription } from '@carf/ui'
```

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| variant | 'default' \| 'destructive' | 'default' | Estilo visual |
| className | string | - | Classes CSS adicionais |

### Exemplos

```tsx
// Alert informativo
<Alert>
  <AlertTitle>Atencao</AlertTitle>
  <AlertDescription>
    Suas alteracoes serao salvas automaticamente.
  </AlertDescription>
</Alert>

// Alert de erro
<Alert variant="destructive">
  <AlertTitle>Erro</AlertTitle>
  <AlertDescription>
    Nao foi possivel salvar. Tente novamente.
  </AlertDescription>
</Alert>

// Com icone
<Alert>
  <InfoIcon className="h-4 w-4" />
  <AlertTitle>Dica</AlertTitle>
  <AlertDescription>
    Voce pode arrastar os itens para reordenar.
  </AlertDescription>
</Alert>
```

---

## Toast

Notificacoes temporarias que aparecem na tela.

### Importacao

```tsx
import { useToast, Toaster, Toast } from '@carf/ui'
```

### Setup

```tsx
// No layout principal
import { Toaster } from '@carf/ui'

export default function Layout({ children }) {
  return (
    <>
      {children}
      <Toaster />
    </>
  )
}
```

### Hook useToast

```tsx
const { toast, dismiss, toasts } = useToast()
```

| Metodo | Descricao |
|:-------|:----------|
| `toast(options)` | Exibe um toast |
| `dismiss(id?)` | Remove toast(s) |
| `toasts` | Lista de toasts ativos |

### Opcoes do Toast

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| title | string | - | Titulo do toast |
| description | string | - | Descricao |
| variant | 'default' \| 'destructive' | 'default' | Estilo |
| duration | number | 5000 | Duracao em ms |
| action | ReactNode | - | Acao opcional |

### Exemplos

```tsx
function SaveButton() {
  const { toast } = useToast()

  async function handleSave() {
    try {
      await save()
      toast({
        title: 'Sucesso',
        description: 'Dados salvos com sucesso.',
      })
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Erro',
        description: 'Falha ao salvar dados.',
      })
    }
  }

  return <Button onClick={handleSave}>Salvar</Button>
}

// Toast com acao
toast({
  title: 'Documento excluido',
  description: 'O documento foi movido para a lixeira.',
  action: (
    <ToastAction altText="Desfazer" onClick={undo}>
      Desfazer
    </ToastAction>
  ),
})

// Toast persistente
toast({
  title: 'Upload em progresso',
  description: 'Enviando arquivo...',
  duration: Infinity, // Nao fecha automaticamente
})
```

---

## Dialog

Modal para interacoes que requerem atencao do usuario.

### Importacao

```tsx
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from '@carf/ui'
```

### Props

#### Dialog

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| open | boolean | - | Estado controlado |
| onOpenChange | (open: boolean) => void | - | Callback ao mudar estado |
| defaultOpen | boolean | false | Aberto inicialmente |

#### DialogContent

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| onEscapeKeyDown | (e) => void | - | Callback ao pressionar Escape |
| onPointerDownOutside | (e) => void | - | Callback ao clicar fora |

### Exemplos

```tsx
// Dialog simples
<Dialog>
  <DialogTrigger asChild>
    <Button>Abrir</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Editar Perfil</DialogTitle>
      <DialogDescription>
        Faca alteracoes no seu perfil aqui.
      </DialogDescription>
    </DialogHeader>
    <form>
      <Input placeholder="Nome" />
    </form>
    <DialogFooter>
      <DialogClose asChild>
        <Button variant="outline">Cancelar</Button>
      </DialogClose>
      <Button>Salvar</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>

// Dialog controlado
function ConfirmDialog() {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="destructive">Excluir</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirmar exclusao?</DialogTitle>
          <DialogDescription>
            Esta acao nao pode ser desfeita.
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Cancelar
          </Button>
          <Button variant="destructive" onClick={handleDelete}>
            Excluir
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

---

## AlertDialog

Dialog de confirmacao que bloqueia interacao ate resposta.

### Importacao

```tsx
import {
  AlertDialog,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogAction,
  AlertDialogCancel,
} from '@carf/ui'
```

### Diferenca do Dialog

- Nao fecha ao clicar fora
- Nao fecha com Escape (por padrao)
- Semanticamente indica acao destrutiva

### Exemplos

```tsx
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Excluir Unidade</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Tem certeza?</AlertDialogTitle>
      <AlertDialogDescription>
        Esta acao excluira permanentemente a unidade UN-001 e todos os
        dados associados. Esta acao nao pode ser desfeita.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancelar</AlertDialogCancel>
      <AlertDialogAction onClick={deleteUnit}>
        Excluir
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

---

## Progress

Indica progresso de operacoes longas.

### Importacao

```tsx
import { Progress } from '@carf/ui'
```

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| value | number | 0 | Progresso atual (0-100) |
| max | number | 100 | Valor maximo |
| className | string | - | Classes CSS adicionais |

### Exemplos

```tsx
// Progresso basico
<Progress value={33} />

// Com label
<div className="space-y-2">
  <div className="flex justify-between text-sm">
    <span>Enviando...</span>
    <span>{progress}%</span>
  </div>
  <Progress value={progress} />
</div>

// Upload com progresso
function UploadProgress({ file }) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    uploadFile(file, {
      onProgress: (p) => setProgress(p),
    })
  }, [file])

  return (
    <div className="space-y-2">
      <p className="text-sm">{file.name}</p>
      <Progress value={progress} />
    </div>
  )
}
```

---

## Skeleton

Placeholder de carregamento que indica conteudo sendo carregado.

### Importacao

```tsx
import { Skeleton } from '@carf/ui'
```

### Props

| Prop | Tipo | Default | Descricao |
|:-----|:-----|:--------|:----------|
| className | string | - | Define dimensoes e forma |

### Exemplos

```tsx
// Card skeleton
<Card>
  <CardHeader>
    <Skeleton className="h-4 w-[200px]" />
    <Skeleton className="h-3 w-[150px]" />
  </CardHeader>
  <CardContent>
    <Skeleton className="h-20 w-full" />
  </CardContent>
</Card>

// Lista skeleton
<div className="space-y-3">
  {[1, 2, 3].map((i) => (
    <div key={i} className="flex items-center space-x-4">
      <Skeleton className="h-12 w-12 rounded-full" />
      <div className="space-y-2">
        <Skeleton className="h-4 w-[200px]" />
        <Skeleton className="h-3 w-[150px]" />
      </div>
    </div>
  ))}
</div>
```

---

## Aspectos de Acessibilidade

### Alert
- Usa `role="alert"` automaticamente
- Anunciado por leitores de tela

### Toast
- `role="status"` para notificacoes
- `aria-live="polite"` para anuncios
- Foco gerenciado para acoes

### Dialog/AlertDialog
- Focus trap automatico
- Retorno de foco ao fechar
- `aria-labelledby` e `aria-describedby` automaticos

### Progress
- `role="progressbar"` automatico
- `aria-valuenow`, `aria-valuemin`, `aria-valuemax` gerenciados
