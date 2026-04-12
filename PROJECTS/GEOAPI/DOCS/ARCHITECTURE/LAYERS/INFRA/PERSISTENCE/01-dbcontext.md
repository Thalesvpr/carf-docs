---
type: leaf
status: active
updated: 2026-02-07
---

# DbContext

O CARFDbContext e a classe central do Entity Framework Core na GEOAPI, configurando mapeamentos, extensoes PostGIS e isolamento multi-tenant via global query filters.

## Estrutura do DbContext

O CARFDbContext herda de DbContext e recebe ITenantContext por injecao no construtor. Expoe DbSets para todas as entidades implementadas no sistema.

| DbSet | Entidade | Tabela | Configuration dedicada |
|-------|----------|--------|----------------------|
| Units | Unit | units | sim (UnitConfiguration) |
| Holders | Holder | holders | sim (HolderConfiguration) |
| Communities | Community | communities | sim (CommunityConfiguration) |
| UnitHolders | UnitHolder | unit_holders | sim (UnitHolderConfiguration) |
| Documents | Document | documents | sim (DocumentConfiguration) |
| Teams | Team | teams | sim (TeamConfiguration) |
| TeamMembers | TeamMember | team_members | nao (convencoes EF Core) |
| CommunityAuthorizations | CommunityAuthorization | community_authorizations | nao (convencoes EF Core) |
| SyncLogs | SyncLog | sync_logs | sim (SyncLogConfiguration) |
| Accounts | Account | accounts | sim (AccountConfiguration) |
| Tenants | Tenant | tenants | sim (TenantConfiguration) |

> **Nota**: TeamMember e CommunityAuthorization nao possuem arquivos IEntityTypeConfiguration dedicados. Seus mapeamentos dependem das convencoes default do EF Core. Indices e constraints especificos para essas entidades devem ser adicionados via configurations futuras ou migrations manuais.

No metodo OnModelCreating, aplica todas as configuracoes de entidade do assembly automaticamente, habilita a extensao postgis e registra global query filters para Unit, Holder e Community, filtrando por TenantId do contexto atual.

## Configuracao da Entidade Unit

A classe UnitConfiguration implementa IEntityTypeConfiguration e mapeia a entidade Unit para a tabela "units". A chave primaria e o Id. O campo Code tem tamanho maximo 50, e obrigatorio e possui indice unico composto com TenantId. As propriedades espaciais Boundary e Centroid sao mapeadas para geometry(Polygon, 4326) e geometry(Point, 4326) respectivamente. O value object Address e mapeado via OwnsOne com colunas prefixadas por "address_". O relacionamento com UnitHolders e um-para-muitos via UnitId. O relacionamento com Community e muitos-para-um via CommunityId.

## Registro no DI

O DbContext e registrado com Npgsql utilizando UseNetTopologySuite para suporte a tipos espaciais e MigrationsAssembly apontando para o projeto GEOAPI.Infrastructure.
