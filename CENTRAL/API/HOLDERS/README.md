# HOLDERS

Schemas JSON para titulares do CARF. HolderCreateRequest (name, cpf validado via dígito verificador, rg opcional, birth_date, phone, email, address objeto, is_main boolean para titular principal, unit_id UUID para vinculação), HolderResponse (id UUID, name, cpf mascarado XXX.XXX.XXX-XX, rg, birth_date, phone, email, address, is_main, unit relação com UnitResponse resumido, created_at, updated_at, tenant_id), HolderUpdateRequest (campos parciais), HolderListResponse (items, pagination), LinkHolderToUnitRequest (holder_id, unit_id, is_main), UnlinkHolderFromUnitRequest (holder_id, unit_id). Validações: CPF único por tenant, max 1 titular principal por unidade, max 3 co-titulares. Endpoints: POST /api/holders, GET /api/holders/{id}, PATCH /api/holders/{id}, DELETE /api/holders/{id}, POST /api/holders/link, POST /api/holders/unlink.

## Implementação e Uso

Endpoint de Posseiros implementado pelo backend GEOAPI usando entity [Holder](../../DOMAIN-MODEL/ENTITIES/03-holder.md) vinculada a [UnitAggregate](../../DOMAIN-MODEL/AGGREGATES/01-unit-aggregate.md) conforme regras de negócio validando máximo 1 titular principal por unidade habitacional e até 3 co-titulares adicionais, consumido por frontend GEOWEB para gestão interativa de vínculos titular-unidade com UI para adicionar remover promover co-titular a principal e mobile REURBCAD para cadastro em campo offline com validações client-side de CPF/CNPJ Email via @carf/tscore Value Objects, ambos usando cliente tipado @carf/geoapi-client para requisições HTTP type-safe e renderizando UI com componente [@carf/ui HolderCard](../../../PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/README.md) exibindo nome CPF mascarado e status de titular principal.

---

**Última atualização:** 2025-12-29
