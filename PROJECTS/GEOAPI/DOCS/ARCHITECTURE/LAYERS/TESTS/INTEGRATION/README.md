# INTEGRATION

Testes integração do GEOAPI validando interação entre múltiplas camadas usando infraestrutura real provisionada via Testcontainers garantindo EF Core queries, migrations, constraints e RLS policies funcionam corretamente contra PostgreSQL PostGIS real. Database integration tests usam PostgreSQL container executando migrations via EF Core verificando schema criado corretamente com indexes, foreign keys, spatial indexes GiST e RLS policies aplicadas, depois exercitam repositories testando queries complexas incluindo spatial operations (ST_Within, ST_Distance), eager loading de relacionamentos via Include() e soft delete filtering via global query filters. Redis integration tests verificam caching layer usando Redis container validando set/get operations, expiration policies, distributed locking via RedLock e pub/sub messaging para cache invalidation cross instances quando entity updated. S3 integration tests usando MinIO container local verificam file upload/download operations, presigned URL generation com expiration, multipart upload para arquivos grandes e cleanup de objetos órfãos quando entity deleted.

## Arquivos Principais (a criar)

**Database - Repositories:**
- 01-unit-repository-integration-tests.md - Queries espaciais ST_Within comunidade
- 02-holder-repository-integration-tests.md - Eager loading vinculos nested
- 03-community-repository-integration-tests.md - Agregações stats unidades
- 04-team-repository-integration-tests.md - Soft delete e query filters

**Database - Migrations:**
- 05-migrations-integration-tests.md - Apply/rollback migrations schema
- 06-rls-policies-integration-tests.md - Row-Level Security multi-tenancy

**Database - Spatial:**
- 07-postgis-integration-tests.md - Operações espaciais PostGIS functions
- 08-geometry-indexing-integration-tests.md - Performance GiST indexes

**Cache - Redis:**
- 09-redis-cache-integration-tests.md - Set/get/invalidate distributed cache
- 10-redis-pubsub-integration-tests.md - Pub/sub cross instances

**Storage - S3:**
- 11-s3-storage-integration-tests.md - Upload/download/delete objects
- 12-presigned-urls-integration-tests.md - Geração URLs temporárias

**External - Keycloak:**
- 13-keycloak-admin-integration-tests.md - User management via Admin API
- 14-keycloak-token-validation-tests.md - JWT validation real tokens

## Convenções

Integration tests usam Testcontainers para provisionar infraestrutura garantindo environment limpo isolado entre test runs sem poluir database desenvolvimento ou depender de serviços externos rodando. Cada test class implementa IAsyncLifetime inicializando containers em InitializeAsync() executado uma vez antes todos tests e disposing em DisposeAsync() garantindo cleanup resources. Database seeding via DbContext cria dados base necessários para testes (tenant padrão, roles, community teste) permitindo tests focar em cenário específico sem setup complexo duplicado. Assertions verificam não apenas resultado query mas também performance usando StopWatch verificando queries espaciais executam em tempo razoável (< 500ms) e explain plan via logging confirma indexes usados corretamente. Transaction rollback após cada test via TransactionScope garante isolation entre tests revertendo todas changes mantendo database em estado consistente conhecido evitando flaky tests por side effects.

---

**Última atualização:** 2026-01-12
