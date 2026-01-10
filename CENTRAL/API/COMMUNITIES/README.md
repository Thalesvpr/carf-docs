# COMMUNITIES

Schemas JSON para comunidades do CARF. CommunityCreateRequest (name, description, polygon GeoJSON agregando múltiplas unidades, city, state, total_units calculado automaticamente), CommunityResponse (id UUID, name, description, polygon, city, state, total_units, total_holders agregado, units array de UnitResponse resumidos, demographics objeto com gender_distribution/age_distribution/income_range calculados, created_at, updated_at, tenant_id), CommunityUpdateRequest (campos parciais), CommunityListResponse (items, pagination), AddUnitToCommunityRequest (community_id, unit_id), RemoveUnitFromCommunityRequest (community_id, unit_id). Cálculos automáticos: total_units conta unidades vinculadas, demographics agrega dados de holders. Endpoints: POST /api/communities, GET /api/communities/{id}, PATCH /api/communities/{id}, DELETE /api/communities/{id}, POST /api/communities/add-unit, POST /api/communities/remove-unit.

## Implementação e Uso

Endpoint de Comunidades implementado pelo backend [GEOAPI](../../../PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-overview.md) usando aggregate [CommunityAggregate](../../DOMAIN-MODEL/AGGREGATES/02-community-aggregate.md) agrupando múltiplas unidades geográficas conforme [ADR-002: PostGIS](../../ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md), consumido por [GEOWEB](../../../PROJECTS/GEOWEB/DOCS/README.md) para visualização de mapas com layers WMS conforme [UC-010: Configurar Camadas WMS](../../REQUIREMENTS/USE-CASES/UC-010-configurar-camadas-wms.md) e [GEOGIS](../../../PROJECTS/GEOGIS/DOCS/README.md) para operações GIS avançadas, ambos via [@carf/geoapi-client](../../../PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/README.md).

---

**Última atualização:** 2025-12-29
