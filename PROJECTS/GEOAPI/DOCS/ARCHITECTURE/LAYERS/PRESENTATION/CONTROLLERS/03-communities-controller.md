---
type: leaf
status: review
updated: 2026-02-08
---

# Communities Controller

O CommunitiesController gerencia operacoes REST sobre comunidades e assentamentos. A rota base e /api/communities. Anotado com ApiController e Authorize, exige autenticacao JWT em todos os endpoints. Operacoes de escrita sao restritas a roles manager ou superior.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/communities | Criar comunidade | 201 | 400 VALIDATION_ERROR | manager+ |
| GET | /api/communities/{id} | Obter comunidade | 200 | 404 | todos autenticados |
| GET | /api/communities | Listar com paginacao | 200 | - | todos autenticados |
| PATCH | /api/communities/{id} | Atualizar comunidade | 200 | 404 | manager+ |
| GET | /api/communities/{id}/units | Listar unidades da comunidade | 200 | - | todos autenticados |
| GET | /api/communities/{id}/geojson | Exportar como GeoJSON | 200 | 404 | todos autenticados |

## Comportamento

O endpoint de criacao monta CreateCommunityCommand com codigo, nome, tipo, municipio, estado e boundary opcional em formato GeoJSON Polygon, retornando CreatedAtAction com CommunityDto. A validacao de boundary via PostGIS ST_IsValid ocorre no handler apos conversao para geometria NetTopologySuite. O endpoint de listagem de unidades aceita os mesmos query params de paginacao e filtro da listagem de units (page, limit, status, search, sortBy, sortDir) e retorna PaginatedResult de UnitListItemDto filtrado pela comunidade. O endpoint de exportacao GeoJSON retorna FeatureCollection contendo o boundary da comunidade e todas as unidades como Features com properties id, code, status e attendance_status.

## Autorizacao

Endpoints de leitura sao acessiveis por qualquer usuario autenticado. Criacao e atualizacao requerem role manager, admin ou super-admin. O isolamento por tenant garante que apenas comunidades do tenant do usuario sao retornadas.
