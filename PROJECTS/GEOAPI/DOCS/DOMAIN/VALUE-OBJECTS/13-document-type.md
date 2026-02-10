---
type: leaf
status: review
updated: 2026-02-08
---

# DocumentType

Value object enum imutavel representando o tipo de documento ou foto armazenado. Persiste na coluna document_type varchar(50) da tabela documents com CHECK constraint. Determina validacoes de formato (MIME type) e regras de obrigatoriedade por contexto.

## Valores Permitidos

| Valor | Descricao | MIME Types Aceitos |
|-------|-----------|-------------------|
| RG | Documento de identidade | image/jpeg, image/png, application/pdf |
| CPF | Cadastro de Pessoa Fisica | image/jpeg, image/png, application/pdf |
| CNH | Carteira Nacional de Habilitacao | image/jpeg, image/png, application/pdf |
| COMPROVANTE_RESIDENCIA | Comprovante de residencia | image/jpeg, image/png, application/pdf |
| FOTO_FACHADA | Foto da fachada principal da unidade | image/jpeg, image/png, image/webp |
| FOTO_DOCUMENTO | Foto generica de documento | image/jpeg, image/png, image/webp |
| CERTIDAO | Certidao cartorial | application/pdf |
| OUTRO | Outros documentos sem categoria especifica | Qualquer tipo aceito |

## Regras de Obrigatoriedade

Para aprovacao de Unit, exige-se ao menos FOTO_FACHADA. Para legitimacao, exige-se documentos do titular (RG ou CNH) e COMPROVANTE_RESIDENCIA.
