---
type: leaf
status: review
updated: 2026-02-08
---

# Common DTOs

DTOs compartilhados utilizados por multiplos dominios da GEOAPI. Definem contratos genericos de paginacao, erro e dados geoespaciais.

## PaginatedResult

DTO generico de resposta paginada retornado por todas as listagens da API.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Items | lista de T | Array de resultados da pagina atual |
| Total | int | Contagem absoluta de registros |
| Page | int | Pagina atual |
| Limit | int | Tamanho da pagina |
| HasNext | bool | Se existe proxima pagina |

Parametros de entrada padrao: page (inteiro, default 1), limit (inteiro, default 20, maximo 100). Total e calculado via COUNT sem paginacao. HasNext e derivado de page * limit menor que total.

## ErrorResponse

DTO de erro padrao conforme RFC 7807 ProblemDetails.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Type | string | URI do tipo de erro |
| Title | string | Descricao curta |
| Status | int | Codigo HTTP |
| Detail | string | Mensagem legivel com contexto |
| Extensions.ErrorCode | string | Codigo maquina (ex: CPF_INVALID) |
| Extensions.Fields | lista de FieldError | Erros por campo quando validacao |

FieldError contem Field (nome do campo), Message (descricao do erro) e Code (codigo do erro).

## GeoJsonFeature

DTO para representacao de dados geoespaciais em formato GeoJSON conforme RFC 7946.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Type | string | Sempre "Feature" |
| Geometry | object | Geometria GeoJSON (Point, Polygon, etc.) |
| Properties | object | Propriedades da feature |

GeoJsonFeatureCollection contem Type (sempre "FeatureCollection") e Features (array de GeoJsonFeature).

GeometryDto contem Type (sempre "Polygon" para unidades e comunidades) e Coordinates (array tridimensional de doubles representando aneis de coordenadas WGS84).

CentroidDto contem Latitude e Longitude como doubles.

BoundingBox contem MinLon, MinLat, MaxLon e MaxLat como doubles para filtros espaciais.
