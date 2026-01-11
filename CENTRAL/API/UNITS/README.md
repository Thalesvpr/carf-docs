# UNITS

Schemas JSON para unidades habitacionais do CARF. UnitCreateRequest (address objeto com street/number/neighborhood/city/state/zip, coordinates objeto com latitude/longitude, area_m2 calculada ou manual, polygon GeoJSON para área, photos array de URLs, notes texto livre), UnitResponse (id UUID, address, coordinates, area_m2, polygon, status enum Rascunho/Pendente/Aprovado/Rejeitado, created_at, updated_at, created_by, tenant_id), UnitUpdateRequest (campos parciais permitindo PATCH), UnitListResponse (items array de UnitResponse, pagination objeto com page/page_size/total_count/total_pages), UnitFilterRequest (query params: status, city, neighborhood, area_min, area_max, created_after, created_before, sort_by, order asc/desc). CRUD completo: POST /api/units, GET /api/units/{id}, PATCH /api/units/{id}, DELETE /api/units/{id}, GET /api/units com filtros e paginação.

## Implementação e Uso

Endpoint de Unidades implementado pelo backend GEOAPI usando aggregate [UnitAggregate](../../DOMAIN-MODEL/AGGREGATES/01-unit-aggregate.md) conforme [ADR-008: Clean Architecture + DDD](../../ARCHITECTURE/ADRs/ADR-008-clean-architecture-ddd.md), persistido em PostgreSQL+PostGIS via [ADR-002: PostGIS](../../ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md) com multi-tenancy isolado por [ADR-005: RLS](../../ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md), consumido por GEOWEB para CRUD web com validações client-side via @carf/tscore e REURBCAD para coleta em campo offline sincronizando via @carf/geoapi-client, ambos renderizando UI com componentes de [@carf/ui UnitCard](../../../PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/README.md).

---

**Última atualização:** 2025-12-29
