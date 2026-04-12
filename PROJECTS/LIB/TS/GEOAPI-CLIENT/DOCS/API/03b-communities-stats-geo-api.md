---
type: leaf
status: review
updated: 2026-02-08
---

# Communities API - Campos, Estatisticas e Geometria

Detalhamento dos campos do CreateCommunityDTO conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md), metodos getUnits e getGeoJson do modulo api.communities. Campos mapeados com a tabela communities do [schema PostgreSQL](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md).

## Campos do CreateCommunityDTO

| Campo | Tipo TS | Obrigatorio | Descricao |
|:------|:--------|:------------|:----------|
| code | string | sim | Codigo unico por tenant, maximo 50 caracteres |
| name | string | sim | Nome da comunidade, maximo 200 caracteres |
| communityType | CommunityType | sim | URBANA, RURAL, QUILOMBOLA ou RIBEIRINHA |
| boundary | GeoJsonPolygon | nao | Perimetro como GeoJSON Polygon WGS84 |
| municipality | string | sim | Municipio, maximo 100 caracteres |
| state | string | sim | UF com exatamente 2 letras |
| district | string | nao | Distrito |
| neighborhood | string | nao | Bairro |
| reference | string | nao | Ponto de referencia em texto livre |

A response retorna CommunityDto com todos os campos incluindo id gerado, area calculada automaticamente a partir do boundary quando fornecido, status ACTIVE e timestamps. Restrito a roles manager ou superior.

## getUnits (GET /api/communities/{id}/units)

O metodo getUnits aceita communityId string e aceita os mesmos query params de paginacao e filtro da listagem de units: page, limit, status, search, sortBy e sortDir. Retorna Promise de PaginatedResponse de UnitListItemDto filtrado pela comunidade. UnitListItemDto e um subconjunto da Unit com id, code, status, endereco resumido, attendanceStatus e createdAt. Acessivel por todos os usuarios autenticados.

## getGeoJson (GET /api/communities/{id}/geojson)

O metodo getGeoJson aceita communityId string e retorna Promise de GeoJSON FeatureCollection. A FeatureCollection contem o boundary da comunidade como Feature com properties contendo id, code e name, e todas as unidades da comunidade como Features individuais com properties contendo id, code, status e attendanceStatus. Retorna NotFoundError 404 se a comunidade nao existir. Acessivel por todos os usuarios autenticados. O formato e diretamente consumivel por bibliotecas de mapeamento como Leaflet e Mapbox GL JS.
