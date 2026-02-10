---
type: leaf
status: review
updated: 2026-02-08
---

# Document Validators

Os validators de documentos utilizam FluentValidation para validar requests de upload de arquivos.

## UploadDocumentRequestValidator

Valida o request de upload de documento com as seguintes regras:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| File | Obrigatorio, tamanho maximo 50MB (52428800 bytes) | Arquivo obrigatorio / Arquivo excede 50MB |
| File.ContentType | Deve ser image/jpeg, image/png, image/webp ou application/pdf | Formato de arquivo nao suportado |
| EntityType | Obrigatorio, enum UNIT, HOLDER, COMMUNITY | Tipo de entidade invalido |
| EntityId | Obrigatorio, UUID valido | ID da entidade obrigatorio |
| DocumentType | Obrigatorio, enum RG, CPF, CNH, COMPROVANTE_RESIDENCIA, FOTO_FACHADA, FOTO_DOCUMENTO, CERTIDAO, OUTRO | Tipo de documento invalido |

A validacao de Content-Type verifica o MIME type declarado pelo client. O handler adicionalmente valida os magic bytes do arquivo para prevenir upload de arquivos maliciosos com Content-Type forjado, comparando os primeiros bytes do stream com assinaturas conhecidas de JPEG (FF D8 FF), PNG (89 50 4E 47) e PDF (25 50 44 46).

## UploadOrtofotoRequestValidator

Valida o request de upload de ortofoto com regras especificas:

| Campo | Regras | Mensagem de Erro |
|-------|--------|-----------------|
| File | Obrigatorio, tamanho maximo 500MB (524288000 bytes) | Arquivo excede 500MB |
| File.ContentType | Deve ser image/tiff | Formato de arquivo nao suportado, apenas GeoTIFF |
| CommunityId | Opcional, UUID valido quando presente | ID da comunidade invalido |
| CaptureDate | Opcional, data no passado quando presente | Data de captura invalida |
