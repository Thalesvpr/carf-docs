# UNITS

Schemas JSON para unidades habitacionais do CARF.

O UnitCreateRequest contém address (street, number, neighborhood, city, state, zip), coordinates (latitude, longitude), area_m2, polygon GeoJSON e photos. O UnitResponse inclui id UUID, status (Rascunho, Pendente, Aprovado, Rejeitado), timestamps e tenant_id.

O UnitFilterRequest permite filtros por status, city, neighborhood, área mínima/máxima, datas e ordenação.

## Endpoints

- POST /api/units - Criar unidade
- GET /api/units/{id} - Obter unidade
- PATCH /api/units/{id} - Atualizar parcialmente
- DELETE /api/units/{id} - Remover unidade
- GET /api/units - Listar com filtros e paginação

## Schemas

- UnitCreateRequest / UnitResponse
- UnitUpdateRequest
- UnitListResponse
- UnitFilterRequest

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: o ramo inteiro esta incompleto. Precisa de supervisão para corrigir.
