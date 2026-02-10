---
type: leaf
status: review
updated: 2026-02-08
---

# Community Queries

As queries de comunidades implementam o lado de leitura do CQRS para o agregado Community, incluindo consultas espaciais via PostGIS e exportacao GeoJSON.

## GetCommunityByIdQuery

Recebe Id da comunidade como Guid e flag opcional IncludeUnitsCount. O handler projeta para CommunityDto incluindo boundary em formato GeoJSON, area calculada e contagem de unidades quando flag ativo. Retorna 404 se nao encontrada.

## ListCommunitiesQuery

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| Page | int | 1 | Pagina atual |
| Limit | int | 20 | Registros por pagina (maximo 100) |
| CommunityType | string | nulo | Filtro por tipo |
| Search | string | nulo | Busca por nome ou codigo |
| SortBy | string | name | Campo de ordenacao |
| SortDir | string | asc | Direcao |

Retorna PaginatedResult de CommunityListItemDto contendo id, code, name, communityType, unitsCount e area.

## GetCommunityUnitsQuery

Recebe CommunityId e aceita mesmos parametros de paginacao e filtro da ListUnitsQuery (page, limit, status, search, sortBy, sortDir). Retorna PaginatedResult de UnitListItemDto filtrado pela comunidade.

## GetCommunityGeoJsonQuery

Recebe CommunityId. Retorna FeatureCollection GeoJSON contendo o boundary da comunidade como Feature principal e todas as unidades ativas como Features individuais com properties contendo id, code, status e attendance_status.
