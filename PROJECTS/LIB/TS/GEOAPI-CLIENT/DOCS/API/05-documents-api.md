---
type: leaf
title: "Documents API - Gerenciamento de Documentos"
status: review
updated: 2026-01-21
source: "interno"
---

# Documents API - Gerenciamento de Documentos

API para upload, download e gerenciamento de documentos anexados a entidades do sistema.

## Import

```typescript
import { GeoApiClient } from '@carf/geoapi-client'
import type { Document, DocumentType, UploadDocumentDTO } from '@carf/tscore/types'

const api = new GeoApiClient({ baseURL: '...', auth })

// Acessar Documents API
api.documents.upload()
api.documents.download()
api.documents.list()
api.documents.getById()
api.documents.delete()
api.documents.getMetadata()
```

## Endpoints

```
POST   /api/documents/upload      - Upload de arquivo
GET    /api/documents/:id         - Download de arquivo
GET    /api/documents/:id/metadata - Obter metadados
GET    /api/documents             - Listar documentos (com filtros)
DELETE /api/documents/:id         - Deletar documento
```

## Methods

### upload()

Faz upload de arquivo e vincula a uma entidade.

```typescript
upload(
  file: File | Blob,
  metadata: UploadDocumentDTO,
  options?: UploadOptions
): Promise<Document>
```

#### Parametros

**file** (obrigatorio): Arquivo a ser enviado

**metadata** (obrigatorio):
```typescript
interface UploadDocumentDTO {
  type: DocumentType           // Tipo do documento
  entityType: 'UNIT' | 'HOLDER' | 'COMMUNITY' | 'LEGITIMATION'
  entityId: string             // UUID da entidade
  description?: string         // Descricao opcional
}
```

**options** (opcional):
```typescript
interface UploadOptions {
  onProgress?: (progress: UploadProgress) => void
  cancelToken?: CancelToken
}

interface UploadProgress {
  loaded: number      // Bytes enviados
  total: number       // Total de bytes
  percentage: number  // 0-100
}
```

#### Retorno

```typescript
interface Document {
  id: string
  type: DocumentType
  fileName: string
  fileSize: number          // Em bytes
  mimeType: string          // Ex: 'application/pdf', 'image/jpeg'
  storageUrl: string        // URL interna (nao usar diretamente)
  entityType: 'UNIT' | 'HOLDER' | 'COMMUNITY' | 'LEGITIMATION'
  entityId: string
  description?: string
  uploadedBy: string        // User ID
  createdAt: Date
}
```

#### Throws

- `ValidationError` (400) - Arquivo invalido ou metadados incorretos
- `FileTooLargeError` (413) - Arquivo excede limite (10MB)
- `UnsupportedMediaTypeError` (415) - Tipo de arquivo nao permitido
- `UnauthorizedError` (401) - Nao autenticado
- `ForbiddenError` (403) - Sem permissao para anexar a esta entidade

#### Exemplo

```typescript
// Upload basico
const file = document.getElementById('fileInput').files[0]

const doc = await api.documents.upload(file, {
  type: 'ID_DOCUMENT',
  entityType: 'HOLDER',
  entityId: 'holder-123',
  description: 'RG frente'
})

console.log(`Upload completo: ${doc.fileName} (${doc.fileSize} bytes)`)

// Upload com progress
const doc = await api.documents.upload(file, metadata, {
  onProgress: (progress) => {
    console.log(`Upload: ${progress.percentage}%`)
    progressBar.value = progress.percentage
  }
})

// Com cancelamento
const cancelToken = CancelToken.source()

setTimeout(() => cancelToken.cancel(), 30000)  // Cancela apos 30s

try {
  await api.documents.upload(file, metadata, { cancelToken: cancelToken.token })
} catch (error) {
  if (CancelToken.isCancel(error)) {
    console.log('Upload cancelado')
  }
}
```

#### Tipos de Arquivo Permitidos

| Categoria | Extensoes | MIME Types |
|:----------|:----------|:-----------|
| Imagens | jpg, jpeg, png, gif, webp | image/* |
| Documentos | pdf | application/pdf |
| Planilhas | xlsx, xls, csv | application/vnd.openxmlformats-*, text/csv |
| Texto | doc, docx, txt | application/msword, text/plain |

**Limite:** 10MB por arquivo

---

### download()

Faz download de arquivo.

```typescript
download(id: string, options?: DownloadOptions): Promise<Blob>
```

#### Parametros

**id** (obrigatorio): UUID do documento

**options** (opcional):
```typescript
interface DownloadOptions {
  onProgress?: (progress: DownloadProgress) => void
  cancelToken?: CancelToken
}
```

#### Retorno

`Blob` com o conteudo do arquivo.

#### Exemplo

```typescript
// Download basico
const blob = await api.documents.download('doc-123')

// Criar link de download
const url = window.URL.createObjectURL(blob)
const link = document.createElement('a')
link.href = url
link.download = 'documento.pdf'
link.click()
window.URL.revokeObjectURL(url)

// Com progress
const blob = await api.documents.download('doc-123', {
  onProgress: (progress) => {
    console.log(`Download: ${progress.percentage}%`)
  }
})

// Exibir imagem
const blob = await api.documents.download('photo-123')
const imageUrl = window.URL.createObjectURL(blob)
document.getElementById('preview').src = imageUrl
```

---

### list()

Lista documentos com filtros.

```typescript
list(query?: ListDocumentsQueryDTO): Promise<PaginatedResponse<Document>>
```

#### Parametros

```typescript
interface ListDocumentsQueryDTO {
  page?: number                // Pagina (padrao: 1)
  limit?: number               // Itens por pagina (padrao: 20)
  entityType?: 'UNIT' | 'HOLDER' | 'COMMUNITY' | 'LEGITIMATION'
  entityId?: string            // Filtrar por entidade especifica
  type?: DocumentType          // Filtrar por tipo de documento
  uploadedBy?: string          // Filtrar por usuario
  createdAfter?: Date          // Documentos apos esta data
  createdBefore?: Date         // Documentos antes desta data
  sortBy?: 'createdAt' | 'fileName' | 'fileSize'
  sortOrder?: 'asc' | 'desc'
}
```

#### Exemplo

```typescript
// Listar documentos de uma unidade
const docs = await api.documents.list({
  entityType: 'UNIT',
  entityId: 'unit-123'
})

// Listar por tipo
const idDocs = await api.documents.list({
  entityType: 'HOLDER',
  entityId: 'holder-456',
  type: 'ID_DOCUMENT'
})

// Paginado
const page2 = await api.documents.list({
  entityType: 'COMMUNITY',
  entityId: 'comm-789',
  page: 2,
  limit: 50
})
```

---

### getById()

Busca documento por ID (apenas metadados).

```typescript
getById(id: string): Promise<Document>
```

#### Exemplo

```typescript
const doc = await api.documents.getById('doc-123')
console.log(`${doc.fileName} - ${doc.type}`)
```

---

### getMetadata()

Alias para getById - obtem metadados sem baixar arquivo.

```typescript
getMetadata(id: string): Promise<Document>
```

---

### delete()

Deleta documento.

```typescript
delete(id: string): Promise<void>
```

#### Throws

- `NotFoundError` (404) - Documento nao existe
- `ForbiddenError` (403) - Sem permissao para deletar

#### Exemplo

```typescript
await api.documents.delete('doc-123')
console.log('Documento deletado')
```

---

## DocumentType Enum

```typescript
enum DocumentType {
  // Identificacao pessoal
  ID_DOCUMENT = 'ID_DOCUMENT'           // RG, CNH
  CPF = 'CPF'

  // Comprovantes
  PROOF_OF_RESIDENCE = 'PROOF_OF_RESIDENCE'
  PROPERTY_TAX = 'PROPERTY_TAX'         // IPTU

  // Documentos legais
  MARRIAGE_CERTIFICATE = 'MARRIAGE_CERTIFICATE'
  POWER_OF_ATTORNEY = 'POWER_OF_ATTORNEY'

  // Tecnicos
  TECHNICAL_REPORT = 'TECHNICAL_REPORT'
  PLANT = 'PLANT'                       // Planta/croqui
  AERIAL_PHOTO = 'AERIAL_PHOTO'

  // Generico
  OTHER = 'OTHER'
}
```

## Uso com React

```tsx
import { useState } from 'react'
import { useApi } from './hooks/useApi'

function DocumentUpload({ entityType, entityId }: Props) {
  const api = useApi()
  const [progress, setProgress] = useState(0)
  const [uploading, setUploading] = useState(false)

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    try {
      const doc = await api.documents.upload(file, {
        type: 'ID_DOCUMENT',
        entityType,
        entityId
      }, {
        onProgress: (p) => setProgress(p.percentage)
      })

      console.log('Upload completo:', doc.id)
    } catch (error) {
      console.error('Erro no upload:', error)
    } finally {
      setUploading(false)
      setProgress(0)
    }
  }

  return (
    <div>
      <input type="file" onChange={handleUpload} disabled={uploading} />
      {uploading && <progress value={progress} max={100} />}
    </div>
  )
}
```
