---
type: leaf
status: review
updated: 2026-02-08
---

# DocumentUploadedEvent

Domain event emitido quando documento, arquivo ou foto e anexado a uma entidade do sistema, representando adicao de evidencia documental para o processo de regularizacao. Permite validacao de completude e processamento assincrono de arquivos.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| DocumentId | Guid | Identificador unico do documento criado. |
| EntityType | EntityType | Tipo da entidade pai: UNIT, HOLDER, COMMUNITY. |
| EntityId | Guid | ID da entidade ao qual documento foi anexado. |
| DocumentType | DocumentType | Categoria: RG, CPF, FOTO_FACHADA, CERTIDAO, etc. |
| FileName | string | Nome original do arquivo preservado. |
| FileSize | bigint | Tamanho em bytes. |
| MimeType | string | Tipo MIME: image/jpeg, application/pdf, etc. |
| UploadedBy | Guid | AccountId que realizou upload. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC do upload. |

## Handlers

| Handler | Acao |
| --- | --- |
| DocumentThumbnailHandler | Gera thumbnails para imagens facilitando preview. |
| DocumentChecklistHandler | Atualiza checklist de documentacao obrigatoria. |
| DocumentCacheHandler | Invalida cache de listagem de documentos da entidade. |
| DocumentAuditHandler | Registra upload em audit trail para compliance. |

## Contexto de Emissao

Emitido pela camada de aplicacao apos upload bem-sucedido via IFileStorage e persistencia do registro em documents. O arquivo e armazenado no S3 com checksum SHA-256 para verificacao de integridade.
