# UNITS

Schemas JSON para unidades habitacionais do CARF. UnitCreateRequest (address objeto com street/number/neighborhood/city/state/zip, coordinates objeto com latitude/longitude, area_m2 calculada ou manual, polygon GeoJSON para área, photos array de URLs, notes texto livre), UnitResponse (id UUID, address, coordinates, area_m2, polygon, status enum Rascunho/Pendente/Aprovado/Rejeitado, created_at, updated_at, created_by, tenant_id), UnitUpdateRequest (campos parciais permitindo PATCH), UnitListResponse (items array de UnitResponse, pagination objeto com page/page_size/total_count/total_pages), UnitFilterRequest (query params: status, city, neighborhood, area_min, area_max, created_after, created_before, sort_by, order asc/desc). CRUD completo: POST /api/units, GET /api/units/{id}, PATCH /api/units/{id}, DELETE /api/units/{id}, GET /api/units com filtros e paginação.

---

**Última atualização:** 2025-12-29
