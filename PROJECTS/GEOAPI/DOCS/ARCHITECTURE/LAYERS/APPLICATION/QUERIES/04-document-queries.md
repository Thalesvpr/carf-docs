---
type: leaf
status: review
updated: 2026-02-08
---

# Document Queries

As queries de documentos implementam o lado de leitura do CQRS para a tabela documents, incluindo geracao de URLs pre-assinadas para acesso aos arquivos no S3.

## GetDocumentByIdQuery

Recebe Id do documento como Guid. O handler carrega metadados do documento e gera URL pre-assinada via IFileStorage com validade de 1 hora para acesso direto ao arquivo. Retorna DocumentDto com id, fileName, fileSize, mimeType, checksum, uploadedAt e presignedUrl. Retorna 404 se nao encontrado.

## ListDocumentsQuery

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| EntityType | string | obrigatorio | UNIT, HOLDER ou COMMUNITY |
| EntityId | Guid | obrigatorio | ID da entidade pai |
| Page | int | 1 | Pagina atual |
| Limit | int | 20 | Registros por pagina |

O handler filtra documentos pelo par (entity_type, entity_id) usando indice composto e aplica paginacao. Retorna PaginatedResult de DocumentListItemDto contendo id, fileName, fileSize, mimeType, documentType e uploadedAt, sem incluir URLs pre-assinadas na listagem para economia de operacoes S3.

## GetDocumentDownloadQuery

Recebe Id do documento como Guid. O handler gera URL pre-assinada via IFileStorage com validade de 15 minutos e retorna a URL para redirect HTTP 302 no controller. Retorna 404 se nao encontrado.
