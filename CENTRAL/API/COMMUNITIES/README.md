# COMMUNITIES

Schemas JSON para comunidades do CARF.

O CommunityCreateRequest contém name, description, polygon GeoJSON agregando múltiplas unidades, city e state. O CommunityResponse inclui total_units calculado automaticamente, total_holders agregado e demographics com distribuição por gênero, idade e renda.

## Endpoints

- POST /api/communities - Criar comunidade
- GET /api/communities/{id} - Obter comunidade com agregações
- PATCH /api/communities/{id} - Atualizar parcialmente
- DELETE /api/communities/{id} - Remover comunidade
- POST /api/communities/add-unit - Adicionar unidade
- POST /api/communities/remove-unit - Remover unidade

## Schemas

- CommunityCreateRequest / CommunityResponse
- CommunityUpdateRequest
- CommunityListResponse
- AddUnitToCommunityRequest / RemoveUnitFromCommunityRequest

---

**Última atualização:** 2026-01-14
