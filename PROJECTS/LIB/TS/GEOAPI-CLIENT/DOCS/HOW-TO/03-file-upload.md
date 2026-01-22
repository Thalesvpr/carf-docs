---
type: leaf
title: "File Upload - @carf/geoapi-client"
status: review
updated: 2026-01-21
source: "interno"
---

# File Upload - Guia Pratico

Guia para upload de arquivos usando a Documents API.

## Upload Basico

```typescript
const file = document.getElementById('fileInput').files[0]

const document = await api.documents.upload(file, {
  type: 'ID_DOCUMENT',
  entityType: 'HOLDER',
  entityId: 'holder-123'
})

console.log('Upload completo:', document.id)
```

## Upload com Progresso

```typescript
const document = await api.documents.upload(file, metadata, {
  onProgress: (progress) => {
    console.log(`${progress.percentage}% (${progress.loaded}/${progress.total} bytes)`)
  }
})
```

## Componente React

### Upload Simples

```tsx
import { useState } from 'react'
import { useApi } from '../hooks/useApi'
import { DocumentType, UploadDocumentDTO } from '@carf/tscore/types'

interface FileUploadProps {
  entityType: 'UNIT' | 'HOLDER' | 'COMMUNITY'
  entityId: string
  documentType: DocumentType
  onSuccess?: (document: Document) => void
}

export function FileUpload({ entityType, entityId, documentType, onSuccess }: FileUploadProps) {
  const api = useApi()
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState<string | null>(null)

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    // Reset state
    setError(null)
    setProgress(0)
    setUploading(true)

    try {
      const doc = await api.documents.upload(
        file,
        {
          type: documentType,
          entityType,
          entityId
        },
        {
          onProgress: (p) => setProgress(p.percentage)
        }
      )

      onSuccess?.(doc)
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message)
      }
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="file-upload">
      <input
        type="file"
        onChange={handleFileChange}
        disabled={uploading}
        accept=".pdf,.jpg,.jpeg,.png"
      />

      {uploading && (
        <div className="progress-bar">
          <div
            className="progress-fill"
            style={{ width: `${progress}%` }}
          />
          <span>{progress}%</span>
        </div>
      )}

      {error && (
        <div className="error">{error}</div>
      )}
    </div>
  )
}
```

### Upload com Drag & Drop

```tsx
import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'

export function DragDropUpload({ entityType, entityId }: Props) {
  const api = useApi()
  const [files, setFiles] = useState<UploadFile[]>([])

  interface UploadFile {
    file: File
    id: string
    status: 'pending' | 'uploading' | 'success' | 'error'
    progress: number
    error?: string
    document?: Document
  }

  const onDrop = useCallback((acceptedFiles: File[]) => {
    // Adicionar arquivos a lista
    const newFiles = acceptedFiles.map(file => ({
      file,
      id: crypto.randomUUID(),
      status: 'pending' as const,
      progress: 0
    }))
    setFiles(prev => [...prev, ...newFiles])

    // Iniciar upload de cada arquivo
    newFiles.forEach(uploadFile)
  }, [])

  async function uploadFile(uploadFile: UploadFile) {
    // Marcar como uploading
    setFiles(prev =>
      prev.map(f =>
        f.id === uploadFile.id
          ? { ...f, status: 'uploading' as const }
          : f
      )
    )

    try {
      const doc = await api.documents.upload(
        uploadFile.file,
        {
          type: 'OTHER',
          entityType,
          entityId
        },
        {
          onProgress: (p) => {
            setFiles(prev =>
              prev.map(f =>
                f.id === uploadFile.id
                  ? { ...f, progress: p.percentage }
                  : f
              )
            )
          }
        }
      )

      // Marcar como sucesso
      setFiles(prev =>
        prev.map(f =>
          f.id === uploadFile.id
            ? { ...f, status: 'success' as const, document: doc }
            : f
        )
      )
    } catch (err) {
      // Marcar como erro
      setFiles(prev =>
        prev.map(f =>
          f.id === uploadFile.id
            ? { ...f, status: 'error' as const, error: err.message }
            : f
        )
      )
    }
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png'],
      'application/pdf': ['.pdf']
    },
    maxSize: 10 * 1024 * 1024  // 10MB
  })

  return (
    <div>
      <div
        {...getRootProps()}
        className={`dropzone ${isDragActive ? 'active' : ''}`}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Solte os arquivos aqui...</p>
        ) : (
          <p>Arraste arquivos ou clique para selecionar</p>
        )}
      </div>

      <ul className="file-list">
        {files.map(f => (
          <li key={f.id} className={`file-item ${f.status}`}>
            <span className="name">{f.file.name}</span>
            {f.status === 'uploading' && (
              <progress value={f.progress} max={100} />
            )}
            {f.status === 'success' && <span>Enviado</span>}
            {f.status === 'error' && <span className="error">{f.error}</span>}
          </li>
        ))}
      </ul>
    </div>
  )
}
```

## Upload com Cancelamento

```typescript
import { CancelToken } from '@carf/geoapi-client'

function UploadWithCancel() {
  const [cancelToken, setCancelToken] = useState<CancelTokenSource | null>(null)

  async function startUpload(file: File) {
    // Criar token de cancelamento
    const source = CancelToken.source()
    setCancelToken(source)

    try {
      const doc = await api.documents.upload(file, metadata, {
        cancelToken: source.token,
        onProgress: setProgress
      })
      return doc
    } catch (error) {
      if (CancelToken.isCancel(error)) {
        console.log('Upload cancelado pelo usuario')
      } else {
        throw error
      }
    } finally {
      setCancelToken(null)
    }
  }

  function cancelUpload() {
    cancelToken?.cancel('Cancelado pelo usuario')
  }

  return (
    <div>
      <input type="file" onChange={e => startUpload(e.target.files[0])} />
      <button onClick={cancelUpload} disabled={!cancelToken}>
        Cancelar
      </button>
    </div>
  )
}
```

## Validacao de Arquivos

### Client-side

```typescript
const MAX_FILE_SIZE = 10 * 1024 * 1024  // 10MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'application/pdf']
const ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.pdf']

function validateFile(file: File): string | null {
  // Tamanho
  if (file.size > MAX_FILE_SIZE) {
    return `Arquivo muito grande. Maximo: ${MAX_FILE_SIZE / 1024 / 1024}MB`
  }

  // Tipo MIME
  if (!ALLOWED_TYPES.includes(file.type)) {
    return `Tipo de arquivo nao permitido: ${file.type}`
  }

  // Extensao
  const ext = '.' + file.name.split('.').pop()?.toLowerCase()
  if (!ALLOWED_EXTENSIONS.includes(ext)) {
    return `Extensao nao permitida: ${ext}`
  }

  return null  // Valido
}
```

### Antes do Upload

```typescript
async function handleUpload(file: File) {
  // Validar
  const error = validateFile(file)
  if (error) {
    toast.error(error)
    return
  }

  // Upload
  await api.documents.upload(file, metadata)
}
```

## Compressao de Imagens

```typescript
import imageCompression from 'browser-image-compression'

async function compressAndUpload(file: File) {
  // Comprimir se for imagem maior que 1MB
  let fileToUpload = file

  if (file.type.startsWith('image/') && file.size > 1024 * 1024) {
    fileToUpload = await imageCompression(file, {
      maxSizeMB: 1,
      maxWidthOrHeight: 1920,
      useWebWorker: true
    })
    console.log(`Comprimido: ${file.size} -> ${fileToUpload.size}`)
  }

  return api.documents.upload(fileToUpload, metadata)
}
```

## Multiplos Arquivos

```typescript
async function uploadMultiple(files: File[]) {
  const results = await Promise.allSettled(
    files.map(file =>
      api.documents.upload(file, {
        type: 'OTHER',
        entityType: 'UNIT',
        entityId: 'unit-123'
      })
    )
  )

  const successful = results.filter(r => r.status === 'fulfilled')
  const failed = results.filter(r => r.status === 'rejected')

  console.log(`${successful.length} enviados, ${failed.length} falharam`)
}
```

## Tratamento de Erros

```typescript
try {
  await api.documents.upload(file, metadata)
} catch (error) {
  if (error instanceof ValidationError) {
    // Arquivo invalido
    toast.error('Arquivo invalido: ' + error.message)
  } else if (error.status === 413) {
    // Payload too large
    toast.error('Arquivo muito grande. Maximo: 10MB')
  } else if (error.status === 415) {
    // Unsupported media type
    toast.error('Tipo de arquivo nao suportado')
  } else if (error instanceof NetworkError) {
    toast.error('Erro de conexao. Verifique sua internet.')
  } else {
    toast.error('Erro ao enviar arquivo')
  }
}
```
