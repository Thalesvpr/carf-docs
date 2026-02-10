---
type: leaf
status: review
updated: 2026-02-08
---

# DocumentType

Value object enum representando categoria de documento ou arquivo vinculado a entidades do sistema, determinando validacoes de formato, tamanho maximo e obrigatoriedade. No banco de dados, corresponde ao campo documents.document_type (varchar(50)) com CHECK constraint.

O tipo determina quais validacoes sao aplicadas no upload, quais MIME types sao aceitos e se o documento e obrigatorio para determinadas transicoes de workflow.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| RG | Documento de identidade (carteira de identidade). |
| CPF | Cadastro de Pessoa Fisica. |
| CNH | Carteira Nacional de Habilitacao. |
| COMPROVANTE_RESIDENCIA | Comprovante de residencia recente. |
| FOTO_FACHADA | Foto frontal da unidade habitacional. |
| FOTO_DOCUMENTO | Foto de documento digitalizado. |
| CERTIDAO | Certidao de nascimento, casamento ou obito. |
| OUTRO | Documento generico nao categorizado. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| MIME types | Fotos: image/jpeg, image/png, image/webp. Documentos: application/pdf. |
| Tamanho maximo | Fotos: 10MB. Documentos tecnicos: 50MB. Outros: 5MB. |
| Obrigatoriedade | Unit em aprovacao requer FOTO_FACHADA. Holder requer CPF ou RG. |

Usado em Document.document_type validando upload conforme categoria, agrupando documentos por tipo em visualizacoes de Unit e Holder, e validando obrigatoriedade em transicoes de workflow de aprovacao.
