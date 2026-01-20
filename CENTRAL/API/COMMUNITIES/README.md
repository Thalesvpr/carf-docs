---
status: review
updated: 2026-01-15
---

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


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-create-community](./01-create-community.md) | Create Community |
| [02-list-communities](./02-list-communities.md) | List Communities |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/API/COMMUNITIES/01-create-community.md|Create Community]]
- ○ [[CENTRAL/API/COMMUNITIES/02-list-communities.md|List Communities]]

<!-- CARF-INDEX-END -->
