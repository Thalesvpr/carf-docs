# DocumentType

Value object enum representando categoria de documento ou arquivo vinculado a entidades do sistema, determinando validações de formato, tamanho máximo, obrigatoriedade e apresentação na interface. Valores possíveis incluem tipos de fotos (PHOTO_FRONT: foto frontal da unidade, PHOTO_AERIAL: foto aérea/drone, PHOTO_LANDMARK: foto de marco geodésico), documentos pessoais (DOC_RG, DOC_CPF, DOC_PROOF_RESIDENCE, DOC_CONTRACT), documentos técnicos (PLANT: planta de legitimação, MEMORIAL: memorial descritivo), e genérico (DOC_OTHER).

Métodos incluem IsPhoto() verificando se é tipo fotográfico permitindo preview, IsTechnicalDocument() verificando se requer assinatura digital ou ART, GetMaxFileSize() retornando tamanho máximo em MB (fotos: 10MB, plantas/memoriais: 50MB, outros: 5MB), GetAllowedMimeTypes() retornando lista de MIME types aceitos, RequiresGeotag() verificando se foto deve ter coordenadas GPS (PHOTO_FRONT, PHOTO_LANDMARK), e ToDisplayString() retornando descrição amigável.

Usado em Document.Type validando upload conforme categoria, apresentando ícones específicos em listas, agrupando documentos por tipo em visualizações de Unit e Holder, validando obrigatoriedade (Unit em aprovação requer PHOTO_FRONT, Holder requer DOC_CPF), e em geração de certidões onde PLANT e MEMORIAL são anexados automaticamente ao PDF final.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
