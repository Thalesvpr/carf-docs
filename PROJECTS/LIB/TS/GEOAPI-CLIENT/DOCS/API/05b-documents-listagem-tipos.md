---
type: leaf
status: review
updated: 2026-02-07
---

# Documents API - Listagem e Tipos

## Metodo list

Lista documentos com filtros e paginacao. Recebe um objeto opcional de consulta e retorna PaginatedResponse de Document.

### Parametros de Consulta

| Campo | Tipo | Obrigatorio | Descricao |
|:------|:-----|:------------|:----------|
| page | number | Nao | Pagina atual, padrao 1 |
| limit | number | Nao | Itens por pagina, padrao 20 |
| entityType | string | Nao | UNIT, HOLDER, COMMUNITY ou LEGITIMATION |
| entityId | string | Nao | UUID da entidade especifica |
| type | DocumentType | Nao | Filtrar por tipo de documento |
| uploadedBy | string | Nao | Filtrar por usuario que fez upload |
| createdAfter | Date | Nao | Documentos apos esta data |
| createdBefore | Date | Nao | Documentos antes desta data |
| sortBy | string | Nao | Ordenar por createdAt, fileName ou fileSize |
| sortOrder | string | Nao | Direcao asc ou desc |

Para listar documentos de uma entidade, combine entityType e entityId. Para filtrar por tipo especifico, adicione o campo type.

## Metodo getById

Busca documento por ID retornando apenas metadados, sem download do conteudo. Recebe o ID como string e retorna o objeto Document.

## Metodo getMetadata

Alias para getById. Obtem metadados de um documento sem baixar o arquivo. Recebe o ID como string e retorna o objeto Document.

## Metodo delete

Deleta um documento permanentemente. Recebe o ID como string e retorna void. Lanca NotFoundError (404) se o documento nao existe e ForbiddenError (403) se o usuario nao tem permissao para deletar.

## Tipos de Documento (DocumentType)

| Valor | Categoria | Descricao |
|:------|:----------|:----------|
| ID_DOCUMENT | Identificacao pessoal | RG ou CNH |
| CPF | Identificacao pessoal | Cadastro de Pessoa Fisica |
| PROOF_OF_RESIDENCE | Comprovantes | Comprovante de residencia |
| PROPERTY_TAX | Comprovantes | IPTU |
| MARRIAGE_CERTIFICATE | Documentos legais | Certidao de casamento |
| POWER_OF_ATTORNEY | Documentos legais | Procuracao |
| TECHNICAL_REPORT | Tecnicos | Laudo tecnico |
| PLANT | Tecnicos | Planta ou croqui |
| AERIAL_PHOTO | Tecnicos | Foto aerea |
| OTHER | Generico | Outro tipo de documento |

Os tipos de documento sao utilizados em todas as APIs que lidam com anexos, incluindo Legitimation API e o proprio upload de documentos. A escolha correta do tipo facilita a filtragem e organizacao dos arquivos vinculados as entidades.
