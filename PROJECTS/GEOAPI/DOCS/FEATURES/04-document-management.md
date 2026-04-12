---
type: leaf
status: review
updated: 2026-02-08
---

# Document Management Feature

A feature de gerenciamento de documentos permite upload, consulta e exclusao de arquivos vinculados a unidades, titulares e comunidades via relacionamento polimorfico. Os arquivos binarios sao armazenados no S3 (MinIO em desenvolvimento) enquanto os metadados ficam na tabela documents do PostgreSQL. Cada upload calcula checksum SHA-256 para garantia de integridade.

## User Stories

US-030 Upload de Documento: o cadastrista faz upload de arquivo via multipart/form-data informando o tipo de entidade (UNIT, HOLDER, COMMUNITY), o id da entidade e o tipo de documento. O servidor armazena o arquivo no S3, calcula o checksum SHA-256, persiste os metadados e retorna DocumentDto com URL pre-assinada valida por 1 hora.

US-031 Download de Documento: o usuario solicita download e recebe redirect HTTP 302 para URL pre-assinada do S3 valida por 15 minutos. O client segue o redirect para baixar o arquivo diretamente do storage.

US-032 Listar Documentos por Entidade: o usuario consulta documentos de uma entidade especifica usando filtros entityType e entityId obrigatorios, recebendo lista paginada de metadados sem incluir URLs pre-assinadas na listagem.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /api/documents/upload | Upload multipart/form-data |
| GET | /api/documents/{id} | Obter metadados com URL pre-assinada |
| GET | /api/documents | Listar por entidade |
| DELETE | /api/documents/{id} | Excluir documento |
| GET | /api/documents/{id}/download | Redirect para URL pre-assinada S3 |

## Regras de Negocio

RN-030: tamanho maximo de arquivo e 50MB. Uploads maiores retornam 413 FILE_TOO_LARGE. RN-031: tipos MIME aceitos sao image/jpeg, image/png, image/webp e application/pdf. Outros tipos retornam 415 UNSUPPORTED_FORMAT. RN-032: o checksum SHA-256 e calculado pelo servidor apos receber o arquivo completo. RN-033: URLs pre-assinadas para consulta individual expiram em 1 hora, URLs de download expiram em 15 minutos. RN-034: exclusao e soft delete via preenchimento de deleted_at, o arquivo binario no S3 e mantido por 30 dias antes de limpeza automatica. RN-035: document_type aceita valores RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO e OUTRO.

## Permissoes

| Acao | field-cadastrator | field-coordinator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|---------|---------|-------|-------------|
| Upload | sim | sim | sim | sim | sim | sim |
| Visualizar | sim | sim | sim | sim | sim | sim |
| Download | sim | sim | sim | sim | sim | sim |
| Excluir | sim | sim | sim | sim | sim | sim |
