# PERSISTENCE

Implementações EF Core para persistência de dados do GEOAPI incluindo DbContext configurado com PostgreSQL PostGIS, repositories concretos implementando interfaces do Domain, migrations para versionamento schema, entity configurations fluent API e seeders de dados iniciais. GeoDbContext centraliza DbSets para todas entities, configura RLS multi-tenancy via HasQueryFilter injetando tenant_id automaticamente, mapeia value objects como owned entities ou conversions, e registra interceptors para audit logging e domain events dispatching. Repositories concretos como UnitRepository estendem GenericRepository<T> adicionando queries específicas da feature (busca espacial Within/Intersects, filtros por status, ordenação), acesso otimizado via IQueryable com Include para eager loading evitando N+1, e AsNoTracking para queries read-only. Migrations geradas via EF Core CLI documentam evolução schema ao longo tempo permitindo rollback seguro, EntityTypeConfigurations aplicam constraints, índices espaciais GiST PostGIS para geometries e índices compostos para queries frequentes. Seeders populam dados base (roles, permissions, tenant demo) para desenvolvimento e testes.

## Arquivos Principais (a criar)

**DbContext:**
- 01-geo-db-context.md - DbContext principal com DbSets e configuration

**Repositories:**
- 02-generic-repository.md - Repository base com CRUD genérico
- 03-unit-repository.md - Queries espaciais e filtros específicos
- 04-holder-repository.md - Busca por CPF e relacionamentos
- 05-community-repository.md - Stats e agregações
- 06-legitimation-repository.md - Workflow queries

**Migrations:**
- 07-migrations-overview.md - Estratégia de migrations
- 08-initial-schema.md - Migration inicial do schema
- 09-add-rls-policies.md - Migration RLS PostgreSQL

**Configurations:**
- 10-unit-configuration.md - Fluent API para Unit entity
- 11-value-objects-configuration.md - Mapeamento owned entities

**Seeders:**
- 12-roles-seeder.md - Dados iniciais roles/permissions
- 13-demo-tenant-seeder.md - Tenant demo para dev

---

**Última atualização:** 2026-01-12
