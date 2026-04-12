---
type: leaf
status: review
updated: 2026-02-08
---

# Document DTOs

Os Data Transfer Objects de documentos definem os contratos de entrada e saida da API para operacoes sobre a tabela documents com armazenamento S3.

## DTOs de Resposta

DocumentDto e o DTO completo retornado em operacoes de leitura individual.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico |
| FileName | string | Nome original do arquivo |
| FileSize | long | Tamanho em bytes |
| MimeType | string | Tipo MIME do arquivo |
| DocumentType | string | Tipo do documento (RG, CPF, etc.) |
| Checksum | string | Hash SHA-256 do conteudo |
| UploadedAt | DateTime | Momento do upload |
| UploadedBy | Guid | Quem fez upload |
| PresignedUrl | string | URL pre-assinada S3 valida por 1 hora |

DocumentListItemDto e o DTO reduzido para listagens contendo Id, FileName, FileSize, MimeType, DocumentType e UploadedAt, sem URL pre-assinada.

## DTOs de Request

UploadDocumentRequest e recebido como multipart/form-data contendo file (IFormFile obrigatorio, maximo 50MB), entityType (string obrigatoria: UNIT, HOLDER ou COMMUNITY), entityId (UUID obrigatorio) e documentType (string obrigatoria: RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO, OUTRO).

## DTOs Auxiliares

ImportResultDto e retornado pelo endpoint de importacao de titulares contendo totalProcessed (total de linhas), totalImported (sucesso), totalErrors (falhas) e errors (array de ImportErrorDto com lineNumber, field e message).
