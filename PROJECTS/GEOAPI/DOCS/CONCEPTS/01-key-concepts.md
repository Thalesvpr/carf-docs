# Key Concepts - GEOAPI

## Conceitos-Chave

Conceitos-chave do GEOAPI incluem **(1) Clean Architecture** - dependências apontam para dentro (Gateway → Application → Domain ← Infrastructure) com Domain layer puro sem frameworks externos contendo apenas regras de negócio em C# puro, **(2) Domain-Driven Design (DDD)** - Ubiquitous Language compartilhado entre devs e stakeholders, Bounded Context de regularização fundiária (REURB), Aggregates (UnitAggregate, CommunityAggregate, LegitimationRequestAggregate) garantindo consistência transacional, Value Objects (CPF, CNPJ, Coordinates) imutáveis com validação no construtor, e Domain Events (UnitCreatedEvent, LegitimationApprovedEvent) para comunicação assíncrona entre aggregates, **(3) CQRS** - Commands modificam estado com validação complexa retornando DTOs, Queries leem estado sem side effects usando projeções otimizadas e cache, ambos despachados via MediatR para handlers isolados e testáveis, **(4) Repository Pattern** - abstração de persistência onde Domain layer depende de IUnitRepository interface implementada por Infrastructure layer com EF Core, **(5) Row-Level Security (RLS)** - isolamento multi-tenant garantido pelo PostgreSQL via policies aplicadas em nível de database, queries automáticas sem precisar filtrar por tenant_id no código.

## Clean Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Gateway Layer                     │  ← Controllers, Middleware
│         (HTTP Requests, Dependency Injection)       │
└─────────────┬───────────────────────────────────────┘
              │ Dependencies flow inward →
┌─────────────▼───────────────────────────────────────┐
│                Application Layer                    │  ← Use Cases
│        (Commands, Queries, Handlers, DTOs)          │
└─────────────┬───────────────────────────────────────┘
              │
┌─────────────▼───────────────────────────────────────┐
│                  Domain Layer                       │  ← Pure Business Logic
│    (Entities, Aggregates, Value Objects, Rules)     │  ← NO external dependencies
└─────────────▲───────────────────────────────────────┘
              │ Implements abstractions ←
┌─────────────┴───────────────────────────────────────┐
│              Infrastructure Layer                    │  ← External Concerns
│     (EF Core, PostgreSQL, Keycloak, File System)    │
└─────────────────────────────────────────────────────┘
```

## Domain-Driven Design

### Aggregates

**UnitAggregate:**
- Root: Unit entity
- Children: Holders, Documents, History
- Invariant: Uma unidade deve ter pelo menos 1 holder
- Transaction boundary: Todas mudanças commitadas juntas

**CommunityAggregate:**
- Root: Community entity
- Children: Units (references), Metadata
- Invariant: Community ativa deve ter coordenadas válidas

**LegitimationRequestAggregate:**
- Root: LegitimationRequest entity
- Children: ApprovalSteps, Documents, Comments
- Invariant: Request aprovado não pode ser editado

### Value Objects

```csharp
// Imutável, validação no construtor
public record CPF
{
    public string Value { get; }

    public CPF(string value)
    {
        if (!IsValid(value))
            throw new InvalidCPFException();

        Value = CleanFormat(value);
    }

    private static bool IsValid(string cpf) { /* ... */ }
}
```

### Domain Events

```csharp
public record UnitCreatedEvent(Guid UnitId, string Code, Guid TenantId) : IDomainEvent;

// Handler
public class NotifyMunicipalityHandler : INotificationHandler<UnitCreatedEvent>
{
    public async Task Handle(UnitCreatedEvent evt, CancellationToken ct)
    {
        await _emailService.SendAsync($"Nova unidade {evt.Code} criada");
    }
}
```

## CQRS Pattern

### Command (Escrita)

```csharp
public record CreateUnitCommand(
    string Code,
    AddressDto Address,
    decimal Area,
    List<HolderDto> Holders
) : IRequest<UnitDto>;

public class CreateUnitHandler : IRequestHandler<CreateUnitCommand, UnitDto>
{
    public async Task<UnitDto> Handle(CreateUnitCommand cmd, CancellationToken ct)
    {
        // 1. Validar (FluentValidation)
        // 2. Criar aggregate
        var unit = Unit.Create(cmd.Code, cmd.Address, cmd.Area);

        // 3. Adicionar holders
        foreach (var h in cmd.Holders)
            unit.AddHolder(h.Name, new CPF(h.Cpf));

        // 4. Salvar
        await _unitRepository.AddAsync(unit, ct);
        await _unitOfWork.CommitAsync(ct);

        // 5. Publicar evento
        await _mediator.Publish(new UnitCreatedEvent(unit.Id, unit.Code));

        return unit.ToDto();
    }
}
```

### Query (Leitura)

```csharp
public record GetUnitByIdQuery(Guid Id) : IRequest<UnitDto>;

public class GetUnitByIdHandler : IRequestHandler<GetUnitByIdQuery, UnitDto>
{
    public async Task<UnitDto> Handle(GetUnitByIdQuery query, CancellationToken ct)
    {
        // Projeção otimizada (sem carrega children desnecessários)
        var unit = await _dbContext.Units
            .AsNoTracking()  // Performance
            .Where(u => u.Id == query.Id)
            .Select(u => new UnitDto {
                Id = u.Id,
                Code = u.Code,
                // ... apenas campos necessários
            })
            .FirstOrDefaultAsync(ct);

        return unit ?? throw new UnitNotFoundException();
    }
}
```

## Repository Pattern

```csharp
// Interface no Domain
public interface IUnitRepository
{
    Task<Unit?> GetByIdAsync(Guid id, CancellationToken ct);
    Task AddAsync(Unit unit, CancellationToken ct);
    Task UpdateAsync(Unit unit, CancellationToken ct);
}

// Implementação no Infrastructure
public class UnitRepository : IUnitRepository
{
    private readonly AppDbContext _context;

    public async Task<Unit?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        return await _context.Units
            .Include(u => u.Holders)
            .FirstOrDefaultAsync(u => u.Id == id, ct);
    }
}
```

## Row-Level Security (RLS)

### Policy PostgreSQL

```sql
-- Aplicada automaticamente em TODAS as queries
CREATE POLICY tenant_isolation ON units
    USING (tenant_id = current_setting('app.tenant_id')::uuid);

ALTER TABLE units ENABLE ROW LEVEL SECURITY;
```

### Configuração no EF Core

```csharp
// Antes de cada query, seta tenant_id
_dbContext.Database.ExecuteSqlRaw(
    "SET LOCAL app.tenant_id = @p0",
    currentUser.TenantId
);

// Query normal - RLS filtra automaticamente
var units = await _dbContext.Units.ToListAsync();
// PostgreSQL adiciona: WHERE tenant_id = 'xxx' automaticamente
```

