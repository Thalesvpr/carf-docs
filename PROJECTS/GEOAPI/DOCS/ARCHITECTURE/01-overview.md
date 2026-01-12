# Overview da Arquitetura - GEOAPI

## Visão Geral

GEOAPI é o backend REST API do ecossistema CARF, responsável por toda a lógica de negócio, persistência de dados e integrações externas conforme domain model documentado em . Construído em **.NET 9** seguindo **[Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)** via , **[Domain-Driven Design (DDD)](https://domainlanguage.com/ddd/)** e **[CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)** via .

## Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────────────────┐
│                          CLIENTS (Consumidores)                        │
│                                                                        │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│   │  GEOWEB  │  │ REURBCAD │  │  ADMIN   │  │  GEOGIS  │           │
│   │  (React) │  │(R.Native)│  │  (React) │  │ (Python) │           │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│        │             │              │              │                  │
│        └─────────────┴──────────────┴──────────────┘                  │
│                          │                                            │
│                    HTTPS/REST                                         │
└────────────────────────────┬───────────────────────────────────────────┘
                             │
             ┌───────────────▼────────────────┐
             │      API Gateway (Nginx)       │ Load Balancer
             └───────────────┬────────────────┘
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
┌───────▼────────┐                       ┌───────▼────────┐
│  GEOAPI Pod 1  │                       │  GEOAPI Pod 2  │
│                │                       │                │
│  ┌──────────┐  │                       │  ┌──────────┐  │
│  │ Gateway  │  │                       │  │ Gateway  │  │
│  │  Layer   │  │                       │  │  Layer   │  │
│  └────┬─────┘  │                       │  └────┬─────┘  │
│       │        │                       │       │        │
│  ┌────▼──────┐ │                       │  ┌────▼──────┐ │
│  │Application│ │                       │  │Application│ │
│  │  Layer    │ │                       │  │  Layer    │ │
│  └────┬──────┘ │                       │  └────┬──────┘ │
│       │        │                       │       │        │
│  ┌────▼──────┐ │                       │  ┌────▼──────┐ │
│  │  Domain   │ │                       │  │  Domain   │ │
│  │   Layer   │ │                       │  │   Layer   │ │
│  └────┬──────┘ │                       │  └────┬──────┘ │
│       │        │                       │       │        │
│  ┌────▼──────┐ │                       │  ┌────▼──────┐ │
│  │Infra-     │ │                       │  │Infra-     │ │
│  │structure  │ │                       │  │structure  │ │
│  └────┬──────┘ │                       │  └────┬──────┘ │
└───────┼────────┘                       └───────┼────────┘
        │                                         │
        └─────────────────┬───────────────────────┘
                          │
              ┌───────────▼───────────┐
              │   PostgreSQL 16       │
              │   + PostGIS 3.4       │
              │   + RLS (Multi-tenant)│
              └───────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                    EXTERNAL INTEGRATIONS                       │
│                                                                │
│  ┌────────────┐                                               │
│  │ Keycloak   │  OAuth2/OIDC Authentication                   │
│  │ (OAuth2)   │  JWT Token Validation                         │
│  └────────────┘  RBAC + Multi-tenancy                         │
│                                                                │
│  ┌────────────┐                                               │
│  │  Email     │  Notifications (SendGrid/SMTP)                │
│  │  Service   │                                               │
│  └────────────┘                                               │
└────────────────────────────────────────────────────────────────┘
```

## Componentes Principais

### 1. Gateway Layer (API)

**Responsabilidade:** Expor endpoints REST, autenticação, validação de entrada.

**Componentes:**
- **Controllers:** Recebem requisições HTTP, validam DTOs, delegam para Application
  - `UnitsController` - CRUD de unidades
  - `HoldersController` - CRUD de posseiros
  - `CommunitiesController` - CRUD de comunidades
  - `LegitimationController` - Processos de legitimação
  - `ReportsController` - Geração de relatórios
  - `AuthenticationController` - Login, refresh, logout

- **Middleware:**
  - `AuthenticationMiddleware` - Valida JWT do Keycloak
  - `TenantMiddleware` - Extrai tenant_id do token
  - `ExceptionHandlerMiddleware` - Tratamento global de erros
  - `LoggingMiddleware` - Logs estruturados de requisições

- **Filters:**
  - `ValidationFilter` - Validação de DTOs com FluentValidation
  - `AuthorizationFilter` - RBAC (roles e permissions)

**Tecnologias:** ASP.NET Core 9, Minimal APIs ou Controllers

---

### 2. Application Layer (Use Cases)

**Responsabilidade:** Orquestrar lógica de negócio, implementar use cases via CQRS.

**Componentes:**

#### Commands (Escrita)
```csharp
CreateUnitCommand
UpdateUnitCommand
DeleteUnitCommand
CreateHolderCommand
UpdateHolderCommand
DeleteHolderCommand
StartLegitimationCommand
ApproveLegitimationCommand
RejectLegitimationCommand
```

#### Queries (Leitura)
```csharp
GetUnitByIdQuery
ListUnitsQuery
SearchUnitsQuery
GetHolderByIdQuery
ListHoldersQuery
GetCommunityByIdQuery
ListCommunitiesQuery
GetLegitimationByIdQuery
ListLegitimationsQuery
```

#### Handlers (MediatR)
```csharp
CreateUnitCommandHandler : IRequestHandler<CreateUnitCommand, UnitDto>
GetUnitByIdQueryHandler : IRequestHandler<GetUnitByIdQuery, UnitDto>
```

#### DTOs (Data Transfer Objects)
```csharp
CreateUnitDto
UpdateUnitDto
UnitDto
HolderDto
CommunityDto
LegitimationDto
```

#### Validators (FluentValidation)
```csharp
CreateUnitDtoValidator : AbstractValidator<CreateUnitDto>
{
    RuleFor(x => x.Address).NotEmpty();
    RuleFor(x => x.Coordinates).NotNull();
    RuleFor(x => x.Area).GreaterThan(0);
}
```

**Tecnologias:** MediatR, FluentValidation, AutoMapper

---

### 3. Domain Layer (Business Logic)

**Responsabilidade:** Lógica de negócio pura, sem dependências externas.

**Componentes:**

#### Aggregates
```csharp
UnitAggregate
  - Unit (root entity)
  - Holder (entity)
  - Documents (value objects)
  - Coordinates (value object)

CommunityAggregate
  - Community (root entity)
  - List<Unit> (entities)

LegitimationRequestAggregate
  - LegitimationRequest (root entity)
  - Unit (entity reference)
  - Holder (entity reference)
  - Documents (value objects)
  - Contestations (entities)
```

#### Entities
```csharp
Unit : Entity<UnitId>
Holder : Entity<HolderId>
Community : Entity<CommunityId>
LegitimationRequest : Entity<LegitimationRequestId>
Tenant : Entity<TenantId>
Account : Entity<AccountId>
Contestation : Entity<ContestationId>
```

#### Value Objects
```csharp
CPF : ValueObject (11 dígitos, validação)
CNPJ : ValueObject (14 dígitos, validação)
Email : ValueObject (RFC 5322 validation)
PhoneNumber : ValueObject (formato BR)
Coordinates : ValueObject (lat, lng, SIRGAS2000)
Address : ValueObject (street, number, neighborhood, city, state, zip)
Area : ValueObject (decimal, sempre > 0)
```

#### Domain Events
```csharp
UnitCreatedEvent : IDomainEvent
HolderRegisteredEvent : IDomainEvent
LegitimationStartedEvent : IDomainEvent
LegitimationApprovedEvent : IDomainEvent
```

#### Specifications (Business Rules)
```csharp
UnitMustHaveValidCoordinatesSpec : ISpecification<Unit>
HolderMustHaveValidCPFSpec : ISpecification<Holder>
LegitimationMustHaveAllDocumentsSpec : ISpecification<LegitimationRequest>
```

#### Repository Interfaces
```csharp
IUnitRepository : IRepository<Unit>
IHolderRepository : IRepository<Holder>
ICommunityRepository : IRepository<Community>
ILegitimationRepository : IRepository<LegitimationRequest>
```

**Tecnologias:** C# puro, sem frameworks externos

---

### 4. Infrastructure Layer (External Concerns)

**Responsabilidade:** Implementações de repositórios, acesso a dados, integrações externas.

**Componentes:**

#### Repositories (EF Core)
```csharp
UnitRepository : Repository<Unit>, IUnitRepository
{
    // EF Core DbSet<Unit>
    // Métodos CRUD + queries customizadas
}
```

#### Database Context
```csharp
CarfDbContext : DbContext
{
    DbSet<Unit> Units { get; set; }
    DbSet<Holder> Holders { get; set; }
    DbSet<Community> Communities { get; set; }
    DbSet<LegitimationRequest> Legitimations { get; set; }

    // OnModelCreating: Entity configurations, RLS policies
}
```

#### Entity Configurations
```csharp
UnitConfiguration : IEntityTypeConfiguration<Unit>
{
    builder.ToTable("units");
    builder.HasKey(u => u.Id);
    builder.OwnsOne(u => u.Coordinates);
    builder.OwnsOne(u => u.Address);
    // RLS Policy: CREATE POLICY tenant_isolation ON units ...
}
```

#### Migrations
```bash
dotnet ef migrations add InitialCreate
dotnet ef database update
```

#### External Services
```csharp
IKeycloakService - Valida JWT, busca user info
IEmailService - Envia notificações
ISMSService - Envia SMS (opcional)
IPDFGeneratorService - Gera PDF de relatórios
```

**Tecnologias:** Entity Framework Core, PostgreSQL, PostGIS, Npgsql

---

## Padrões Arquiteturais Utilizados

### 1. Clean Architecture (Hexagonal Architecture)

**Princípio:** Dependências apontam para dentro. Domain é o núcleo, sem dependências externas.

```
Gateway → Application → Domain ← Infrastructure
```

**Benefícios:**
- Domain isolado e testável
- Fácil troca de frameworks (ex: EF Core → Dapper)
- Regras de negócio protegidas

### 2. Domain-Driven Design (DDD)

**Conceitos aplicados:**
- **Ubiquitous Language:** Linguagem compartilhada entre dev e negócio
- **Bounded Contexts:** Contexto de REURB (regularização fundiária)
- **Aggregates:** Garantem consistência transacional
- **Value Objects:** Imutáveis, validação no construtor
- **Domain Events:** Comunicação entre aggregates

### 3. CQRS (Command Query Responsibility Segregation)

**Separação de escrita e leitura:**

**Commands** (escrita):
- Modificam estado
- Validação complexa
- Disparam domain events
- Retornam DTO ou void

**Queries** (leitura):
- Não modificam estado
- Retornam DTOs diretamente
- Podem usar projeções otimizadas
- Cacheable

**Implementação:** MediatR para despachar commands/queries para handlers

### 4. Repository Pattern

**Abstração de persistência:**

```csharp
public interface IUnitRepository
{
    Task<Unit?> GetByIdAsync(UnitId id);
    Task<List<Unit>> ListAsync(FilterParams filters);
    Task AddAsync(Unit unit);
    Task UpdateAsync(Unit unit);
    Task DeleteAsync(UnitId id);
}
```

**Implementação:**
- EF Core no Infrastructure layer
- Domain layer depende apenas da interface

### 5. Unit of Work

**Gerenciamento de transações:**

```csharp
using var transaction = await _context.Database.BeginTransactionAsync();
try
{
    await _unitRepository.AddAsync(unit);
    await _holderRepository.AddAsync(holder);
    await _context.SaveChangesAsync();
    await transaction.CommitAsync();
}
catch
{
    await transaction.RollbackAsync();
    throw;
}
```

**Implementação:** DbContext do EF Core atua como Unit of Work

### 6. Dependency Injection

**Configuração (Program.cs):**

```csharp
// Domain services
builder.Services.AddScoped<IUnitRepository, UnitRepository>();

// Application services
builder.Services.AddMediatR(typeof(CreateUnitCommandHandler).Assembly);
builder.Services.AddValidatorsFromAssembly(typeof(CreateUnitDtoValidator).Assembly);

// Infrastructure services
builder.Services.AddDbContext<CarfDbContext>(options =>
    options.UseNpgsql(connectionString, b => b.UseNetTopologySuite()));
```

---

## Princípios de Design

### SOLID

1. **Single Responsibility Principle (SRP)**
   - Cada classe tem uma única responsabilidade
   - Controllers apenas recebem requisições
   - Handlers apenas processam lógica de negócio

2. **Open/Closed Principle (OCP)**
   - Extensível via herança e interfaces
   - Domain events permitem adicionar comportamentos sem modificar código existente

3. **Liskov Substitution Principle (LSP)**
   - Interfaces bem definidas (IRepository, IHandler)
   - Subtipos substituíveis

4. **Interface Segregation Principle (ISP)**
   - Interfaces pequenas e específicas
   - IUnitRepository, IHolderRepository (não um IGenericRepository enorme)

5. **Dependency Inversion Principle (DIP)**
   - Domain depende de abstrações (interfaces)
   - Infrastructure implementa as interfaces

### DRY (Don't Repeat Yourself)

- Base classes: `Entity<TId>`, `ValueObject`, `Repository<T>`
- Extension methods: `StringExtensions.ToCPF()`, `CoordinatesExtensions.ToGeoPoint()`
- Shared validators: `CPFValidator`, `CoordinatesValidator`

### KISS (Keep It Simple, Stupid)

- Evitar over-engineering
- Use cases simples não precisam de CQRS completo
- Queries diretas quando não há lógica complexa

### YAGNI (You Aren't Gonna Need It)

- Implementar features quando necessário
- Evitar abstrações prematuras
- Domain events: só adicionar quando houver necessidade real

---

## Decisões Técnicas Chave

### 1. .NET 9 vs Node.js

**Escolhido:** .NET 9

**Justificativa:**
- Performance superior (async/await, compilado)
- Type safety (C# estático)
- Ecossistema maduro (EF Core, MediatR, FluentValidation)
- Integração nativa com PostgreSQL (Npgsql)
- PostGIS support via NetTopologySuite

**Ver:** 

### 2. PostgreSQL + PostGIS vs MongoDB

**Escolhido:** PostgreSQL 16 + PostGIS 3.4

**Justificativa:**
- Dados relacionais (Unit ↔ Holder ↔ Community)
- Suporte geoespacial nativo (PostGIS)
- ACID transactions
- Row-Level Security (multi-tenancy)
- Maturidade e confiabilidade

**Ver:** 

### 3. Keycloak vs Auth0

**Escolhido:** Keycloak

**Justificativa:**
- Open-source, self-hosted
- Multi-tenancy nativo
- OAuth2/OIDC compliant
- RBAC granular
- Customizável (themes, SPIs)
- Sem custos de licença

**Ver:** 

### 4. CQRS com MediatR vs Services Tradicionais

**Escolhido:** CQRS com MediatR

**Justificativa:**
- Separação clara de comandos e queries
- Handlers testáveis individualmente
- Pipeline de validação e logging
- Escalabilidade (futuramente: event sourcing)

**Ver:** 

### 5. Multi-tenancy via RLS vs Schema-per-tenant

**Escolhido:** Row-Level Security (RLS)

**Justificativa:**
- Single database, single schema
- Isolamento garantido pelo PostgreSQL
- Queries não precisam filtrar por tenant (RLS faz automaticamente)
- Migrations unificadas
- Backup/restore simplificado

**Ver:** 

---

## Stack Tecnológico Completo

| Camada | Tecnologia | Versão | Justificativa |
|--------|------------|--------|---------------|
| **Framework** | .NET | 9.0 | Performance, async/await, type safety |
| **ORM** | Entity Framework Core | 9.0 | Migrations, LINQ, Change Tracking |
| **Database** | PostgreSQL | 16 | ACID, relacionais, maturidade |
| **Geospatial** | PostGIS | 3.4 | Spatial queries, SIRGAS2000 |
| **CQRS** | MediatR | 13.0 | Despachar commands/queries |
| **Validation** | FluentValidation | 12.0 | Validação expressiva e testável |
| **Logging** | Serilog | 4.0 | Structured logging |
| **Testing** | xUnit | 2.6 | Unit + integration tests |
| **Mocking** | Moq | 4.20 | Mocks para testes |
| **Auth** | Keycloak | 24.0 | OAuth2/OIDC |
| **HTTP Client** | HttpClient | Built-in | Integração com Keycloak |
| **JSON** | System.Text.Json | Built-in | Serialização/deserialização |
