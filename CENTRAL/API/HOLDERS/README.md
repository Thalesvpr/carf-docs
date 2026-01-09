# HOLDERS

Schemas JSON para titulares do CARF. HolderCreateRequest (name, cpf validado via dígito verificador, rg opcional, birth_date, phone, email, address objeto, is_main boolean para titular principal, unit_id UUID para vinculação), HolderResponse (id UUID, name, cpf mascarado XXX.XXX.XXX-XX, rg, birth_date, phone, email, address, is_main, unit relação com UnitResponse resumido, created_at, updated_at, tenant_id), HolderUpdateRequest (campos parciais), HolderListResponse (items, pagination), LinkHolderToUnitRequest (holder_id, unit_id, is_main), UnlinkHolderFromUnitRequest (holder_id, unit_id). Validações: CPF único por tenant, max 1 titular principal por unidade, max 3 co-titulares. Endpoints: POST /api/holders, GET /api/holders/{id}, PATCH /api/holders/{id}, DELETE /api/holders/{id}, POST /api/holders/link, POST /api/holders/unlink.

---

**Última atualização:** 2025-12-29
