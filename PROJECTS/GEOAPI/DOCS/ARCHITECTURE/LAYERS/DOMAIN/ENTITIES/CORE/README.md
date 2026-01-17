# CORE

Entities core multi-tenancy do GEOAPI implementando isolamento dados por tenant e integração com Keycloak. Account representa usuário sistema vinculado a Tenant via TenantId aplicando RLS PostgreSQL isolando dados, KeycloakUserId Guid identificando usuário no Keycloak sincronizado via Admin API quando usuário criado/atualizado, Email e Name básicos duplicando claims JWT para queries rápidas evitando roundtrip Keycloak, IsActive boolean permitindo desativação lógica e Roles lista strings cacheadas do Keycloak verificadas em authorization policies. Tenant representa organização município cliente isolado logicamente via tenant_id propagado automaticamente em todas queries através EF Core query filters, Name e Slug identificadores únicos, Settings JSONB armazenando configurações específicas (logo URL, cores tema, limites geográficos operação) e IsActive controlando acesso durante inadimplência ou migração sem deletar dados históricos.

## Arquivos

- **[06-account.md](./06-account.md)** - Usuário sistema vinculado tenant Keycloak
- **[07-tenant.md](./07-tenant.md)** - Tenant multi-tenancy organização município

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [06-account](./06-account.md) | Account |
| [07-tenant](./07-tenant.md) | Tenant |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
