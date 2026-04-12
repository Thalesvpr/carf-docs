---
type: leaf
status: review
updated: 2026-02-07
---

# Communities API - Operacoes CRUD

O modulo communities do GeoApiClient expoe metodos para gerenciamento de comunidades e nucleos urbanos informais onde se aplicam processos de regularizacao fundiaria REURB. Os metodos sao acessiveis via api.communities.

## Endpoints

| Metodo HTTP | Rota | Descricao |
|:------------|:-----|:----------|
| GET | /api/communities | Listar comunidades com filtros |
| GET | /api/communities/:id | Buscar comunidade por ID |
| POST | /api/communities | Criar nova comunidade |
| PATCH | /api/communities/:id | Atualizar comunidade |
| DELETE | /api/communities/:id | Deletar comunidade via soft delete |

## list

O metodo list aceita ListCommunitiesQueryDTO opcional e retorna Promise de PaginatedResponse de Community.

| Parametro | Tipo | Obrigatorio | Descricao |
|:----------|:-----|:------------|:----------|
| page | number | nao | Pagina atual |
| limit | number | nao | Itens por pagina |
| status | enum | nao | ACTIVE, INACTIVE ou ARCHIVED |
| city | string | nao | Filtrar por municipio |
| state | string | nao | Filtrar por UF |
| search | string | nao | Busca textual em nome |
| sortBy | enum | nao | name, createdAt ou unitCount |
| sortOrder | enum | nao | asc ou desc |

## getById

O metodo getById aceita id string e opcoes com include aceitando units, blocks, geometry e statistics. Retorna Promise de Community completa com os relacionamentos solicitados populados.

## create

O metodo create aceita CreateCommunityDTO e retorna Promise de Community. Campos detalhados em 03b-communities-stats-geo-api.

## update

O metodo update aceita id string e UpdateCommunityDTO com campos parciais. Retorna Promise de Community atualizada.

## delete

O metodo delete aceita id string e retorna void. Executa soft delete. Comunidade com unidades vinculadas nao pode ser deletada. E necessario deletar ou mover todas as unidades antes da remocao.
