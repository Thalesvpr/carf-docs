---
type: leaf
status: review
updated: 2026-02-08
---

# Document Commands

Os commands de documentos representam operacoes de escrita sobre a tabela documents com armazenamento binario no S3. Os handlers coordenam upload de arquivo, calculo de checksum SHA-256 e persistencia de metadados.

---

## UploadDocumentCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| File | IFormFile | sim | Arquivo binario (maximo 50MB) |
| EntityType | string | sim | UNIT, HOLDER ou COMMUNITY |
| EntityId | Guid | sim | ID da entidade pai |
| DocumentType | string | sim | RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO, OUTRO |

O handler executa quatro passos sequenciais. Primeiro, valida tipo MIME do arquivo aceitando apenas image/jpeg, image/png, image/webp e application/pdf, retornando 415 UNSUPPORTED_FORMAT para tipos nao aceitos. Segundo, valida tamanho maximo de 50MB, retornando 413 FILE_TOO_LARGE para arquivos maiores. Terceiro, calcula checksum SHA-256 do conteudo do arquivo para garantia de integridade. Quarto, armazena o arquivo no S3 via IFileStorage e persiste metadados na tabela documents incluindo file_path, file_name (nome original preservado), file_size, mime_type, checksum e uploaded_by.

Emite DocumentUploadedEvent com Id, EntityType, EntityId e DocumentType. O response inclui presignedUrl valida por 1 hora para acesso direto ao arquivo.

---

## DeleteDocumentCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| DocumentId | Guid | sim | Identificador do documento |

O handler carrega o documento pelo Id e executa soft delete preenchendo deleted_at. O arquivo binario no S3 e mantido por 30 dias antes de limpeza automatica via job agendado. Retorna 204 em caso de sucesso ou 404 se o documento nao existe.
