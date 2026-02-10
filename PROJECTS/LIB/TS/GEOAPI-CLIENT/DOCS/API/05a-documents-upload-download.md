---
type: leaf
status: review
updated: 2026-02-07
---

# Documents API - Upload e Download

## Visao Geral

A Documents API fornece operacoes para upload, download e gerenciamento de documentos anexados a entidades do sistema. O acesso ocorre via o namespace api.documents no GeoApiClient.

## Endpoints

| Metodo HTTP | Rota | Descricao |
|:------------|:-----|:----------|
| POST | /api/documents/upload | Upload de arquivo |
| GET | /api/documents/:id | Download de arquivo |
| GET | /api/documents/:id/metadata | Obter metadados |
| GET | /api/documents | Listar documentos com filtros |
| DELETE | /api/documents/:id | Deletar documento |

## Metodo upload

Faz upload de arquivo e vincula a uma entidade. Recebe o arquivo (File ou Blob), um objeto de metadados e opcoes opcionais. Retorna o Document criado.

### Metadados do Upload

| Campo | Tipo | Obrigatorio | Descricao |
|:------|:-----|:------------|:----------|
| type | DocumentType | Sim | Tipo do documento |
| entityType | string | Sim | UNIT, HOLDER, COMMUNITY ou LEGITIMATION |
| entityId | string | Sim | UUID da entidade |
| description | string | Nao | Descricao opcional |

### Opcoes de Upload

O upload aceita opcoes opcionais: onProgress recebe um callback com objeto contendo loaded (bytes enviados), total (bytes totais) e percentage (0 a 100). O campo cancelToken permite cancelar o upload em andamento.

### Estrutura de Retorno (Document)

| Campo | Tipo | Descricao |
|:------|:-----|:----------|
| id | string | UUID do documento |
| type | DocumentType | Tipo do documento |
| fileName | string | Nome do arquivo |
| fileSize | number | Tamanho em bytes |
| mimeType | string | Tipo MIME do arquivo |
| storageUrl | string | URL interna de armazenamento |
| entityType | string | Tipo da entidade vinculada |
| entityId | string | UUID da entidade vinculada |
| description | string (opcional) | Descricao |
| uploadedBy | string | ID do usuario que fez upload |
| createdAt | Date | Data de criacao |

### Erros Possiveis

O upload lanca ValidationError (400) para dados invalidos, FileTooLargeError (413) quando o arquivo excede 10MB, UnsupportedMediaTypeError (415) para tipos nao permitidos, UnauthorizedError (401) para falta de autenticacao e ForbiddenError (403) para falta de permissao.

### Tipos de Arquivo Permitidos

| Categoria | Extensoes | MIME Types |
|:----------|:----------|:-----------|
| Imagens | jpg, jpeg, png, gif, webp | image/* |
| Documentos | pdf | application/pdf |
| Planilhas | xlsx, xls, csv | application/vnd.openxmlformats-*, text/csv |
| Texto | doc, docx, txt | application/msword, text/plain |

O limite maximo e de 10MB por arquivo.

## Metodo download

Faz download de um arquivo. Recebe o ID do documento e opcoes opcionais de progresso e cancelamento. Retorna um Blob com o conteudo do arquivo.
