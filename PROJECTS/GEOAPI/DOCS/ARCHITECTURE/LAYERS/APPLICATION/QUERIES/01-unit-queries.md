---
type: leaf
status: active
updated: 2026-02-07
---

# Unit Queries

As queries CQRS de unidades implementam o lado de leitura do padrao CQRS na GEOAPI. Todas sao records imutaveis que implementam IRequest do MediatR, separando claramente operacoes de leitura das de escrita.

## GetUnitByIdQuery

Recebe o Id da unidade e dois flags opcionais: IncludeHolders e IncludeCommunity (ambos falso por padrao). O handler constroi a query base filtrando por Id e adiciona Include/ThenInclude condicionalmente conforme os flags. Retorna Result contendo UnitDto mapeado via AutoMapper ou nulo se nao encontrado.

## ListUnitsQuery

Query de listagem paginada com filtros compostos.

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| Page | int | 1 | Pagina atual |
| Limit | int | 20 | Registros por pagina |
| Status | string | nulo | Filtro por status da unidade |
| Neighborhood | string | nulo | Filtro por bairro |
| CommunityId | Guid | nulo | Filtro por comunidade |
| Bbox | BoundingBox | nulo | Envelope geografico para filtro espacial |
| Search | string | nulo | Busca textual |
| Sort | string | -created_at | Campo e direcao de ordenacao |

Retorna PagedResult de UnitSummaryDto.

## GetUnitsGeoJsonQuery

Recebe filtros opcionais por CommunityId e Status. Retorna um GeoJsonFeatureCollection para renderizacao em mapa. O handler simplifica geometrias conforme o viewport atual.

## GetUnitStatisticsQuery

Recebe filtro opcional por CommunityId. Retorna UnitStatisticsDto contendo agregacoes como total de unidades, contagem por status e area total.
