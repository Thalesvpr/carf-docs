---
type: leaf
status: review
updated: 2026-02-08
---

# Estrutura do Projeto

Mapa completo da estrutura de pastas e namespaces do projeto GEOAPI, seguindo arquitetura DDD com separacao em quatro camadas: Domain, Application, Infrastructure e Gateway (Apresentacao).

## Arvore de Diretorios

```
src/
├── Carf.GeoApi.Domain/              # Camada de Dominio
│   ├── Entities/                     # Entidades e Aggregates
│   │   ├── Units/                    # Unit, UnitHolder
│   │   ├── Holders/                  # Holder
│   │   ├── Communities/              # Community, Block, Plot
│   │   ├── Documents/                # Document
│   │   ├── Teams/                    # Team, TeamMember
│   │   ├── Auth/                     # Session, ApiKey
│   │   ├── Accounts/                 # Account
│   │   ├── Tenants/                  # Tenant
│   │   ├── Legitimation/            # LegitimationRequest, DescriptiveMemorial, LegitimationPlan
│   │   ├── Surveying/               # Surveyor, SurveyPoint
│   │   └── Base/                    # BaseEntity, BaseAggregateRoot
│   ├── ValueObjects/                # CPF, Email, GeoPolygon, GeoPoint, Address, etc.
│   ├── Events/                      # Domain Events (IDomainEvent implementations)
│   ├── Exceptions/                  # DomainException, ValidationException, etc.
│   └── Contracts/                   # IRepository, IUnitOfWork, ITenantProvider, etc.
│
├── Carf.GeoApi.Application/         # Camada de Aplicacao
│   ├── Commands/                    # Command handlers (IRequest<Result>)
│   │   ├── Units/                   # CreateUnitCommand, UpdateUnitCommand, etc.
│   │   ├── Holders/                 # CreateHolderCommand, LinkHolderCommand, etc.
│   │   ├── Communities/             # CreateCommunityCommand, etc.
│   │   ├── Documents/               # UploadDocumentCommand, etc.
│   │   ├── Teams/                   # CreateTeamCommand, etc.
│   │   ├── Legitimation/           # SubmitRequestCommand, etc.
│   │   ├── Sync/                   # PushChangesCommand, PullChangesCommand
│   │   ├── Orthofotos/             # UploadOrtofotoCommand, etc.
│   │   └── AuthKeys/               # CreateApiKeyCommand, etc.
│   ├── Queries/                     # Query handlers (IRequest<Result<T>>)
│   │   ├── Units/                   # GetUnitByIdQuery, ListUnitsQuery, etc.
│   │   ├── Holders/                 # GetHolderByIdQuery, SearchHoldersQuery, etc.
│   │   ├── Communities/             # GetCommunityByIdQuery, etc.
│   │   ├── Documents/               # GetDocumentByIdQuery, etc.
│   │   ├── Teams/                   # GetTeamByIdQuery, etc.
│   │   ├── Legitimation/           # GetRequestByIdQuery, etc.
│   │   ├── Sync/                   # GetChangesSinceQuery
│   │   └── Orthofotos/             # GetOrtofotoByIdQuery, etc.
│   ├── DTOs/                        # Data Transfer Objects
│   │   ├── Units/                   # UnitDto, CreateUnitRequest, UnitListResponse
│   │   ├── Holders/                 # HolderDto, CreateHolderRequest
│   │   ├── Communities/             # CommunityDto, CommunityStatsDto
│   │   ├── Documents/               # DocumentDto, PresignedUploadResponse
│   │   ├── Teams/                   # TeamDto, TeamMemberDto
│   │   ├── Legitimation/           # LegitimationRequestDto, CertificateDto
│   │   ├── Sync/                   # SyncPackageDto, ChangeSetDto
│   │   ├── Orthofotos/             # OrtofotoDto, ProcessingStatusDto
│   │   └── Common/                  # PagedResult, ErrorResponse, Result<T>
│   ├── Validators/                  # FluentValidation validators
│   │   ├── Units/                   # CreateUnitValidator, UpdateUnitValidator
│   │   ├── Holders/                 # CreateHolderValidator
│   │   ├── Communities/             # CreateCommunityValidator
│   │   ├── Documents/               # UploadDocumentValidator
│   │   └── Legitimation/           # SubmitRequestValidator
│   ├── Mappers/                     # AutoMapper profiles
│   │   └── MappingProfile.cs       # Perfil unico com todos os mapeamentos
│   └── Behaviors/                   # MediatR pipeline behaviors
│       ├── ValidationBehavior.cs    # Executa FluentValidation antes do handler
│       ├── LoggingBehavior.cs       # Log de entrada/saida de commands/queries
│       ├── TransactionBehavior.cs   # Wrapper transacional para commands
│       └── TenantBehavior.cs        # Garante tenant context nos handlers
│
├── Carf.GeoApi.Infrastructure/      # Camada de Infraestrutura
│   ├── Persistence/                 # Entity Framework Core
│   │   ├── CARFDbContext.cs         # DbContext principal
│   │   ├── Configurations/          # EntityTypeConfiguration por entidade
│   │   │   ├── UnitConfiguration.cs
│   │   │   ├── HolderConfiguration.cs
│   │   │   ├── CommunityConfiguration.cs
│   │   │   ├── DocumentConfiguration.cs
│   │   │   ├── TeamConfiguration.cs
│   │   │   ├── TenantConfiguration.cs
│   │   │   ├── AccountConfiguration.cs
│   │   │   ├── SessionConfiguration.cs
│   │   │   ├── ApiKeyConfiguration.cs
│   │   │   └── LegitimationRequestConfiguration.cs
│   │   ├── Migrations/              # EF Core migrations
│   │   └── Interceptors/           # SaveChangesInterceptor para audit
│   ├── Repositories/                # Implementacoes de IRepository
│   │   ├── UnitRepository.cs
│   │   ├── HolderRepository.cs
│   │   ├── CommunityRepository.cs
│   │   ├── DocumentRepository.cs
│   │   ├── TeamRepository.cs
│   │   ├── LegitimationRepository.cs
│   │   └── UnitOfWork.cs
│   ├── Services/                    # Integracoes externas
│   │   ├── KeycloakService.cs       # Integracao com Keycloak Admin API
│   │   ├── S3FileStorage.cs         # Upload/download S3/MinIO
│   │   ├── QuestPdfGenerator.cs     # Geracao de PDFs com QuestPDF
│   │   ├── SignalRNotificationService.cs # Notificacoes real-time
│   │   └── MediatRDomainEventDispatcher.cs # Despacho de domain events
│   ├── Cache/                       # Cache distribuido
│   │   ├── RedisCacheService.cs     # Implementacao de ICacheService
│   │   └── CachedRepositories/      # Decorators de cache sobre repositorios
│   │       ├── CachedUnitRepository.cs
│   │       └── CachedCommunityRepository.cs
│   └── Jobs/                        # Hangfire jobs
│       ├── OrtophotoProcessingJob.cs
│       ├── ReportGenerationJob.cs
│       ├── NotificationJob.cs
│       ├── DataCleanupJob.cs
│       ├── SyncMonitorJob.cs
│       └── StatsRefreshJob.cs
│
└── Carf.GeoApi.Gateway/            # Camada de Apresentacao (API)
    ├── Controllers/                 # REST controllers
    │   ├── UnitsController.cs
    │   ├── HoldersController.cs
    │   ├── CommunitiesController.cs
    │   ├── DocumentsController.cs
    │   ├── TeamsController.cs
    │   ├── LegitimationController.cs
    │   ├── SyncController.cs
    │   ├── OrthofotosController.cs
    │   ├── AuthKeysController.cs
    │   ├── AdminController.cs
    │   ├── HealthController.cs
    │   └── PackagesController.cs
    ├── Middlewares/                 # Middlewares HTTP
    │   ├── ExceptionHandlingMiddleware.cs
    │   ├── TenantMiddleware.cs
    │   ├── CorrelationIdMiddleware.cs
    │   └── RequestLoggingMiddleware.cs
    ├── Filters/                    # Action filters
    │   └── ValidationFilter.cs
    ├── Hubs/                       # SignalR hubs
    │   └── NotificationHub.cs
    ├── Configuration/              # Registros de DI e options
    │   ├── DomainServiceRegistration.cs
    │   ├── ApplicationServiceRegistration.cs
    │   ├── InfrastructureServiceRegistration.cs
    │   └── PresentationServiceRegistration.cs
    └── Program.cs                  # Entry point e pipeline configuration
```

## Mapeamento Pasta / Namespace / Responsabilidade

| Pasta | Namespace | Responsabilidade | Exemplos de Classes |
|-------|-----------|-----------------|-------------------|
| Domain/Entities/Units | Carf.GeoApi.Domain.Entities.Units | Aggregate root Unit e entidade UnitHolder | Unit, UnitHolder |
| Domain/Entities/Holders | Carf.GeoApi.Domain.Entities.Holders | Entidade Holder (titular) | Holder |
| Domain/Entities/Communities | Carf.GeoApi.Domain.Entities.Communities | Aggregate Community com Block e Plot | Community, Block, Plot |
| Domain/Entities/Documents | Carf.GeoApi.Domain.Entities.Documents | Entidade Document | Document |
| Domain/Entities/Teams | Carf.GeoApi.Domain.Entities.Teams | Aggregate Team com TeamMember | Team, TeamMember |
| Domain/Entities/Auth | Carf.GeoApi.Domain.Entities.Auth | Session e ApiKey | Session, ApiKey |
| Domain/Entities/Accounts | Carf.GeoApi.Domain.Entities.Accounts | Conta de usuario | Account |
| Domain/Entities/Tenants | Carf.GeoApi.Domain.Entities.Tenants | Tenant (municipio) | Tenant |
| Domain/Entities/Legitimation | Carf.GeoApi.Domain.Entities.Legitimation | Fluxo de legitimacao fundiaria | LegitimationRequest, DescriptiveMemorial, LegitimationPlan |
| Domain/Entities/Surveying | Carf.GeoApi.Domain.Entities.Surveying | Topografia e medicoes | Surveyor, SurveyPoint |
| Domain/Entities/Base | Carf.GeoApi.Domain.Entities.Base | Classes base de entidades | BaseEntity, BaseAggregateRoot |
| Domain/ValueObjects | Carf.GeoApi.Domain.ValueObjects | Objetos de valor imutaveis | CPF, Email, GeoPolygon, GeoPoint, Address, PhoneNumber |
| Domain/Events | Carf.GeoApi.Domain.Events | Domain events para comunicacao entre aggregates | UnitCreatedEvent, HolderLinkedEvent |
| Domain/Exceptions | Carf.GeoApi.Domain.Exceptions | Excecoes de dominio tipadas | DomainException, ValidationException, NotFoundException |
| Domain/Contracts | Carf.GeoApi.Domain.Contracts | Interfaces (portas) do dominio | IRepository, IUnitOfWork, ITenantProvider |
| Application/Commands | Carf.GeoApi.Application.Commands | Handlers de commands (escrita) | CreateUnitCommand, CreateUnitHandler |
| Application/Queries | Carf.GeoApi.Application.Queries | Handlers de queries (leitura) | GetUnitByIdQuery, GetUnitByIdHandler |
| Application/DTOs | Carf.GeoApi.Application.DTOs | Objetos de transferencia de dados | UnitDto, CreateUnitRequest, PagedResult |
| Application/Validators | Carf.GeoApi.Application.Validators | Validadores FluentValidation | CreateUnitValidator |
| Application/Mappers | Carf.GeoApi.Application.Mappers | Perfis AutoMapper | MappingProfile |
| Application/Behaviors | Carf.GeoApi.Application.Behaviors | Pipeline behaviors MediatR | ValidationBehavior, LoggingBehavior |
| Infrastructure/Persistence | Carf.GeoApi.Infrastructure.Persistence | EF Core DbContext e configuracoes | CARFDbContext, UnitConfiguration |
| Infrastructure/Repositories | Carf.GeoApi.Infrastructure.Repositories | Implementacoes de repositorios | UnitRepository, UnitOfWork |
| Infrastructure/Services | Carf.GeoApi.Infrastructure.Services | Integracoes com servicos externos | KeycloakService, S3FileStorage |
| Infrastructure/Cache | Carf.GeoApi.Infrastructure.Cache | Cache Redis e decorators | RedisCacheService, CachedUnitRepository |
| Infrastructure/Jobs | Carf.GeoApi.Infrastructure.Jobs | Jobs assincronos Hangfire | OrtophotoProcessingJob, ReportGenerationJob |
| Gateway/Controllers | Carf.GeoApi.Gateway.Controllers | Endpoints REST | UnitsController, HoldersController |
| Gateway/Middlewares | Carf.GeoApi.Gateway.Middlewares | Pipeline HTTP | ExceptionHandlingMiddleware, TenantMiddleware |
| Gateway/Filters | Carf.GeoApi.Gateway.Filters | Filtros de action | ValidationFilter |
| Gateway/Hubs | Carf.GeoApi.Gateway.Hubs | SignalR hubs | NotificationHub |
| Gateway/Configuration | Carf.GeoApi.Gateway.Configuration | Registro de servicos DI | InfrastructureServiceRegistration |

## Dependencias entre Projetos

```
Gateway ──────► Application ──────► Domain
   │                │                  ▲
   │                │                  │
   └──► Infrastructure ───────────────┘
```

| Projeto | Depende de | Nao pode depender de |
|---------|-----------|---------------------|
| Domain | nenhum (projeto raiz) | Application, Infrastructure, Gateway |
| Application | Domain | Infrastructure, Gateway |
| Infrastructure | Domain | Application (exceto para registrar handlers), Gateway |
| Gateway | Application, Infrastructure | Domain diretamente (usa via Application) |

### Regra de Ouro

A camada de Domain nao possui **nenhuma** dependencia externa. Nao referencia pacotes NuGet alem de abstractions puras. Todas as interfaces de infraestrutura (IRepository, IFileStorage, ICacheService) sao definidas no Domain como contratos, e implementadas na camada Infrastructure.

## Arquivos de Configuracao na Raiz

```
├── Carf.GeoApi.sln                  # Solution file
├── Directory.Build.props            # Propriedades comuns (versao, nullable, etc.)
├── Directory.Packages.props         # Central Package Management (versoes NuGet)
├── docker-compose.yml               # Compose para dev local
├── docker-compose.override.yml      # Overrides de dev (ports, volumes)
├── Dockerfile                       # Multi-stage build
├── .editorconfig                    # Code style rules
├── .gitignore                       # Patterns de ignore
├── k8s/                             # Manifests Kubernetes
│   ├── staging/                     # Manifests de staging
│   └── production/                  # Manifests de producao
└── scripts/                         # Scripts auxiliares
    ├── seed-dev-data.sql            # Seed de dados para dev
    └── run-migrations.sh            # Script de execucao de migrations
```