---
type: leaf
status: review
updated: 2026-02-07
---

# Units API - Operacoes CRUD Basicas

O modulo units do GeoApiClient expoe metodos de leitura e criacao de unidades habitacionais. Os metodos sao acessiveis via api.units.list, api.units.getById e api.units.create.

## Endpoints

| Metodo HTTP | Rota | Descricao |
|:------------|:-----|:----------|
| GET | /api/units | Listar unidades com filtros e paginacao |
| GET | /api/units/:id | Buscar unidade por ID |
| POST | /api/units | Criar nova unidade habitacional |

## list

O metodo list aceita ListUnitsQueryDTO opcional e retorna Promise de PaginatedResponse de Unit. A resposta paginada contem items, total, page, limit, totalPages, hasNext e hasPrevious.

| Parametro | Tipo | Obrigatorio | Descricao |
|:----------|:-----|:------------|:----------|
| page | number | nao | Pagina atual, padrao 1 |
| limit | number | nao | Itens por pagina, padrao 20, maximo 100 |
| communityId | string | nao | Filtrar por comunidade |
| blockId | string | nao | Filtrar por quadra |
| status | UnitStatus | nao | Filtrar por status |
| occupationType | enum | nao | RESIDENTIAL, COMMERCIAL, MIXED ou INSTITUTIONAL |
| search | string | nao | Busca textual em code, street e neighborhood |
| sortBy | enum | nao | code, createdAt, updatedAt ou status |
| sortOrder | enum | nao | asc ou desc |
| include | array | nao | community, holders, documents ou surveyPoints |

## getById

O metodo getById aceita id string obrigatorio e opcoes com include opcional. O include aceita community, block, plot, holders, documents, surveyPoints e annotations. Retorna objeto Unit completo. Lanca NotFoundError 404 se a unidade nao existir, UnauthorizedError 401 se nao autenticado, ou ForbiddenError 403 se sem permissao.

## create

O metodo create aceita CreateUnitDTO e retorna Promise de Unit com ID gerado. Para detalhes dos campos do DTO, ver 01b-units-update-api. Lanca ValidationError 400 para dados invalidos ou ConflictError 409 se o codigo ja existir na comunidade.
