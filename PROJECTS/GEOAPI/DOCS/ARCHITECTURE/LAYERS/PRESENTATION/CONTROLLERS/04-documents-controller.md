---
type: leaf
status: review
updated: 2026-02-08
---

# Documents Controller

O DocumentsController gerencia upload, consulta e exclusao de documentos e fotos vinculados a entidades do sistema. A rota base e /api/documents. O upload utiliza multipart/form-data para receber o arquivo binario junto com metadados. Downloads sao servidos via redirect para URL pre-assinada do S3.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/documents/upload | Upload multipart/form-data | 201 | 413 FILE_TOO_LARGE, 415 UNSUPPORTED_FORMAT | todos autenticados |
| GET | /api/documents/{id} | Obter metadados com URL pre-assinada | 200 | 404 | todos autenticados |
| GET | /api/documents | Listar por entidade | 200 | - | todos autenticados |
| DELETE | /api/documents/{id} | Excluir documento | 204 | 404 | todos autenticados |
| GET | /api/documents/{id}/download | Redirect para URL pre-assinada S3 | 302 | 404 | todos autenticados |

## Comportamento

O endpoint de upload recebe multipart/form-data com campo file (maximo 50MB), entityType (UNIT, HOLDER, COMMUNITY), entityId (UUID) e documentType (RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO, OUTRO). O handler calcula checksum SHA-256 do arquivo, armazena no S3 via IFileStorage e persiste metadados na tabela documents. O response retorna DocumentDto incluindo presignedUrl valida por 1 hora. O endpoint de download retorna HTTP 302 com header Location apontando para URL pre-assinada valida por 15 minutos, permitindo que o client baixe diretamente do S3. O endpoint de listagem requer query params entityType e entityId obrigatorios para filtrar documentos de uma entidade especifica.

## Autorizacao

Todos os endpoints sao acessiveis por qualquer usuario autenticado do tenant. O isolamento por tenant e garantido via tenant_id na tabela documents filtrado por RLS.
