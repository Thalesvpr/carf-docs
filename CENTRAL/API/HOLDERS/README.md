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

---

**Última atualização:** 2026-01-14
