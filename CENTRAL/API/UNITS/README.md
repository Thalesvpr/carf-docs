---
status: review
updated: 2026-01-15
---

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


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-create-unit](./01-create-unit.md) | Create Unit |
| [02-get-unit](./02-get-unit.md) | Get Unit |
| [03-list-units](./03-list-units.md) | List Units |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/API/UNITS/01-create-unit.md|Create Unit]]
- ○ [[CENTRAL/API/UNITS/02-get-unit.md|Get Unit]]
- ○ [[CENTRAL/API/UNITS/03-list-units.md|List Units]]

<!-- CARF-INDEX-END -->
