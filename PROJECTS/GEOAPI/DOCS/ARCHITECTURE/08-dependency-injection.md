---
type: leaf
status: review
updated: 2026-02-08
---

# Dependency Injection

Mapa completo de registro de servicos no container de DI da GEOAPI. O registro e organizado em extension methods por camada, invocados no `Program.cs`.

## Registro no Program.cs

```
var builder = WebApplication.CreateBuilder(args);

// Registro por camada
builder.Services.AddDomain();
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);
builder.Services.AddPresentation();

var app = builder.Build();
```

## Extension Methods por Camada

### AddDomain()

A camada de Domain e composta por POCOs puros (entidades, value objects, domain events). Nao requer nenhum registro no container de DI. O metodo existe por convencao e documentacao, mas seu corpo e vazio.

```
public static IServiceCollection AddDomain(this IServiceCollection services)
{
    // Domain e POCO puro — nenhum registro necessario
    return services;
}
```

### AddApplication()

Registra os servicos da camada de aplicacao: MediatR handlers, FluentValidation validators, AutoMapper profiles e pipeline behaviors.

| Registro | Metodo | Descricao |
|----------|--------|-----------|
| MediatR | AddMediatR(cfg => cfg.RegisterServicesFromAssembly(...)) | Registra todos os command/query handlers do assembly Application |
| FluentValidation | AddValidatorsFromAssembly(...) | Registra todos os validators do assembly Application |
| AutoMapper | AddAutoMapper(...) | Registra todos os profiles do assembly Application |
| ValidationBehavior | AddTransient(typeof(IPipelineBehavior<,>), typeof(ValidationBehavior<,>)) | Pipeline que executa validacao antes do handler |
| LoggingBehavior | AddTransient(typeof(IPipelineBehavior<,>), typeof(LoggingBehavior<,>)) | Pipeline que loga entrada/saida |
| TransactionBehavior | AddTransient(typeof(IPipelineBehavior<,>), typeof(TransactionBehavior<,>)) | Pipeline que wrapa commands em transacao |
| TenantBehavior | AddTransient(typeof(IPipelineBehavior<,>), typeof(TenantBehavior<,>)) | Pipeline que garante tenant context |

### AddInfrastructure(IConfiguration)

Registra DbContext, repositorios, servicos de integracao, cache e jobs. Recebe `IConfiguration` para binding de options.

### AddPresentation()

Registra controllers, filtros, Swagger, CORS, health checks e SignalR.

| Registro | Metodo | Descricao |
|----------|--------|-----------|
| Controllers | AddControllers() | Registra controllers do assembly Gateway |
| Swagger | AddEndpointsApiExplorer() + AddSwaggerGen() | Documentacao Swagger/OpenAPI |
| CORS | AddCors(options => ...) | Politica de CORS por ambiente |
| HealthChecks | AddHealthChecks().AddNpgSql().AddRedis().AddUrlGroup() | Checks de saude |
| SignalR | AddSignalR() | Hubs de notificacao real-time |
| Authentication | AddAuthentication().AddJwtBearer() | Autenticacao JWT via Keycloak |
| Authorization | AddAuthorization(options => ...) | Politicas de autorizacao por role |
| ValidationFilter | Configure<MvcOptions>(o => o.Filters.Add<ValidationFilter>()) | Filtro global de validacao |

## Tabela Completa de Servicos Registrados

### Infraestrutura — Persistencia

| Interface | Implementacao | Lifetime | Descricao |
|-----------|--------------|----------|-----------|
| CARFDbContext | CARFDbContext | Scoped | Entity Framework DbContext com PostgreSQL+PostGIS |
| IUnitRepository | UnitRepository | Scoped | Repositorio de unidades |
| IHolderRepository | HolderRepository | Scoped | Repositorio de titulares |
| ICommunityRepository | CommunityRepository | Scoped | Repositorio de comunidades |
| IDocumentRepository | DocumentRepository | Scoped | Repositorio de documentos |
| ITeamRepository | TeamRepository | Scoped | Repositorio de equipes |
| ILegitimationRepository | LegitimationRepository | Scoped | Repositorio de legitimacao fundiaria |
| IAccountRepository | AccountRepository | Scoped | Repositorio de contas de usuario |
| ITenantRepository | TenantRepository | Scoped | Repositorio de tenants |
| IUnitOfWork | UnitOfWork | Scoped | Transacao atomica (SaveChanges) |

### Infraestrutura — Contexto

| Interface | Implementacao | Lifetime | Descricao |
|-----------|--------------|----------|-----------|
| ITenantContext | TenantContext | Scoped | Contexto do tenant atual (extraido do token JWT) |
| ICurrentUser | CurrentUser | Scoped | Usuario autenticado atual (claims do token) |
| IDateTimeProvider | UtcDateTimeProvider | Singleton | Provedor de data/hora UTC (testavel) |

### Infraestrutura — Servicos Externos

| Interface | Implementacao | Lifetime | Descricao |
|-----------|--------------|----------|-----------|
| IFileStorage | S3FileStorage | Scoped | Upload/download de arquivos no S3/MinIO |
| ICacheService | RedisCacheService | Scoped | Cache distribuido Redis |
| IKeycloakService | KeycloakService | Scoped | Integracao com Keycloak Admin API |
| INotificationService | SignalRNotificationService | Scoped | Notificacoes real-time via SignalR |
| IPdfGenerator | QuestPdfGenerator | Scoped | Geracao de documentos PDF com QuestPDF |
| IDomainEventDispatcher | MediatRDomainEventDispatcher | Scoped | Despacho de domain events via MediatR |

### Infraestrutura — Singletons

| Interface | Implementacao | Lifetime | Descricao |
|-----------|--------------|----------|-----------|
| IConnectionMultiplexer | ConnectionMultiplexer | Singleton | Pool de conexoes Redis (StackExchange.Redis) |
| IAmazonS3 | AmazonS3Client | Singleton | Cliente AWS S3 |
| IHttpClientFactory | HttpClientFactory | Singleton | Factory de HttpClient para Keycloak |

### Aplicacao — MediatR e Pipeline

| Interface | Implementacao | Lifetime | Descricao |
|-----------|--------------|----------|-----------|
| IMediator | Mediator | Transient | MediatR mediator (despacho de commands/queries) |
| IPipelineBehavior<,> | ValidationBehavior<,> | Transient | Executa FluentValidation antes do handler |
| IPipelineBehavior<,> | LoggingBehavior<,> | Transient | Log estruturado de entrada/saida |
| IPipelineBehavior<,> | TransactionBehavior<,> | Transient | Wrapper transacional para commands |
| IPipelineBehavior<,> | TenantBehavior<,> | Transient | Garante tenant context no handler |

## Ordem de Execucao dos Pipeline Behaviors

Os behaviors MediatR sao executados em ordem de registro (FIFO). A ordem definida na GEOAPI:

```
1. LoggingBehavior      → Loga request de entrada
2. TenantBehavior       → Configura tenant context
3. ValidationBehavior   → Executa FluentValidation, retorna erro se invalido
4. TransactionBehavior  → Abre transacao (somente para Commands)
5. [Handler]            → Executa o handler real
6. TransactionBehavior  → Commit ou rollback
7. LoggingBehavior      → Loga response de saida
```

## Lifetime Guidelines

### Scoped (por requisicao HTTP)

Servicos que dependem do contexto da requisicao HTTP. Uma nova instancia e criada para cada request e compartilhada dentro dele.

- **Quando usar**: DbContext, repositorios, servicos que acessam dados do tenant/usuario atual
- **Exemplos**: CARFDbContext, UnitRepository, TenantContext, CurrentUser

### Singleton (vida da aplicacao)

Servicos stateless ou que gerenciam pools de conexao. Uma unica instancia compartilhada entre todas as requisicoes.

- **Quando usar**: connection pools, factories, provedores de data/hora
- **Exemplos**: IConnectionMultiplexer, IAmazonS3, IDateTimeProvider, IHttpClientFactory

### Transient (nova instancia por resolucao)

Servicos leves e stateless que podem ser criados frequentemente sem custo significativo.

- **Quando usar**: mediators, validators, pipeline behaviors
- **Exemplos**: IMediator, IPipelineBehavior<,>, IValidator<>

## Options Pattern

Configuracoes tipadas registradas via Options pattern:

| Options Class | Secao do appsettings | Propriedades Principais |
|--------------|---------------------|----------------------|
| DatabaseOptions | Database | ConnectionString, MaxPoolSize, CommandTimeout |
| RedisOptions | Redis | ConnectionString, InstanceName, DefaultTTL |
| S3Options | FileStorage | BucketName, Region, Endpoint, ForcePathStyle |
| KeycloakOptions | Keycloak | Authority, Realm, ClientId, ClientSecret, AdminApiUrl |
| HangfireOptions | Hangfire | ConnectionString, WorkerCount, Queues[] |
| CorsOptions | Cors | AllowedOrigins[], AllowedMethods[] |
| JwtOptions | Jwt | Authority, Audience, RequireHttpsMetadata |

Registro:

```
services.Configure<DatabaseOptions>(configuration.GetSection("Database"));
services.Configure<RedisOptions>(configuration.GetSection("Redis"));
services.Configure<S3Options>(configuration.GetSection("FileStorage"));
services.Configure<KeycloakOptions>(configuration.GetSection("Keycloak"));
services.Configure<HangfireOptions>(configuration.GetSection("Hangfire"));
```

## Decorators

O projeto utiliza o pattern Decorator para adicionar comportamento transversal sem alterar implementacoes:

| Interface Original | Decorator | Comportamento Adicionado |
|-------------------|-----------|------------------------|
| IUnitRepository | CachedUnitRepository | Cache Redis antes de consultar o banco |
| ICommunityRepository | CachedCommunityRepository | Cache Redis para comunidades e boundaries |

Registro via Scrutor:

```
services.AddScoped<IUnitRepository, UnitRepository>();
services.Decorate<IUnitRepository, CachedUnitRepository>();
```

A ordem importa: o decorator e registrado **apos** a implementacao concreta. Scrutor encadeia automaticamente a injecao.