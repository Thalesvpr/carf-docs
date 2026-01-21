---
status: rejected
description: "Stub incompleto. Spec de API deve ter request/response schemas, exemplos, erros. Mover implementacao para PROJECTS/GEOAPI."
updated: 2026-01-15
---

# HOLDERS

Schemas JSON para titulares do CARF.

O HolderCreateRequest contém name, cpf validado via dígito verificador, rg opcional, birth_date, phone, email, address e is_main para indicar titular principal. O HolderResponse retorna cpf mascarado e relação com a unidade.

Validações: CPF único por tenant, máximo 1 titular principal por unidade, máximo 3 co-titulares.

## Endpoints

- POST /api/holders - Criar titular
- GET /api/holders/{id} - Obter titular
- PATCH /api/holders/{id} - Atualizar parcialmente
- DELETE /api/holders/{id} - Remover titular
- POST /api/holders/link - Vincular titular a unidade
- POST /api/holders/unlink - Desvincular titular

## Schemas

- HolderCreateRequest / HolderResponse
- HolderUpdateRequest
- HolderListResponse
- LinkHolderToUnitRequest / UnlinkHolderFromUnitRequest


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-create-holder](./01-create-holder.md) | Create Holder |
| [02-list-holders](./02-list-holders.md) | List Holders |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/API/HOLDERS/01-create-holder.md|Create Holder]]
- ○ [[CENTRAL/API/HOLDERS/02-list-holders.md|List Holders]]

<!-- CARF-INDEX-END -->
