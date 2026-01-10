# Design Principles - GEOAPI

## Princípios de Design

### 1. SOLID Principles

#### Single Responsibility Principle (SRP)

Cada classe tem uma única razão para mudar. Controllers apenas recebem requests e retornam responses. Handlers processam lógica de negócio. Repositories acessam dados.

```csharp
// ✅ CORRETO - Responsabilidades separadas
public class UnitsController : ControllerBase
{
    public async Task<IActionResult> Create([FromBody] CreateUnitCommand cmd)
    {
        var result = await _mediator.Send(cmd);
        return CreatedAtAction(nameof(GetById), new { id = result.Id }, result);
    }
}

public class CreateUnitHandler : IRequestHandler<CreateUnitCommand, UnitDto>
{
    public async Task<UnitDto> Handle(CreateUnitCommand cmd, CancellationToken ct)
    {
        // Lógica de negócio aqui
    }
}

// ❌ INCORRETO - Controller com lógica de negócio
public class UnitsController : ControllerBase
{
    public async Task<IActionResult> Create([FromBody] CreateUnitDto dto)
    {
        // Validar aqui - ERRADO
        if (dto.Area <= 0) return BadRequest();

        // Criar entity aqui - ERRADO
        var unit = new Unit { Code = dto.Code, Area = dto.Area };

        // Salvar aqui - ERRADO
        await _context.Units.AddAsync(unit);
        await _context.SaveChangesAsync();

        return Ok(unit);
    }
}
```

#### Open/Closed Principle (OCP)

Extensível via novos handlers/events sem modificar código existente.

```csharp
// Adicionar nova funcionalidade via novo handler
public class SendEmailOnUnitCreatedHandler : INotificationHandler<UnitCreatedEvent>
{
    // Sem modificar código existente
}
```

#### Liskov Substitution Principle (LSP)

Interfaces IRepository são substituíveis por qualquer implementação (EF Core, Dapper, mock).

```csharp
public interface IUnitRepository
{
    Task<Unit?> GetByIdAsync(Guid id, CancellationToken ct);
}

// Implementação real
public class UnitRepository : IUnitRepository { }

// Mock para testes
public class MockUnitRepository : IUnitRepository { }
```

#### Interface Segregation Principle (ISP)

Interfaces pequenas e específicas ao invés de uma grande interface genérica.

```csharp
// ✅ CORRETO - Interfaces segregadas
public interface IUnitReader
{
    Task<Unit?> GetByIdAsync(Guid id);
}

public interface IUnitWriter
{
    Task AddAsync(Unit unit);
    Task UpdateAsync(Unit unit);
}

// ❌ INCORRETO - Interface grande
public interface IUnitRepository
{
    Task<Unit?> GetByIdAsync(Guid id);
    Task<List<Unit>> GetAllAsync();
    Task<List<Unit>> SearchAsync(string query);
    Task AddAsync(Unit unit);
    Task UpdateAsync(Unit unit);
    Task DeleteAsync(Guid id);
    Task<int> CountAsync();
    Task<bool> ExistsAsync(Guid id);
    // ... 20 métodos
}
```

#### Dependency Inversion Principle (DIP)

Domain depende de abstrações (IRepository), Infrastructure implementa concreções (UnitRepository).

```csharp
// Domain Layer define abstração
namespace Carf.GEOAPI.Domain.Repositories
{
    public interface IUnitRepository { }
}

// Infrastructure implementa
namespace Carf.GEOAPI.Infrastructure.Repositories
{
    public class UnitRepository : IUnitRepository { }
}

// Application depende da abstração
public class CreateUnitHandler
{
    private readonly IUnitRepository _repository;  // Interface, não concreção
}
```

### 2. DRY (Don't Repeat Yourself)

Evitar duplicação via base classes, métodos compartilhados, extensions.

```csharp
// ✅ CORRETO - Base class reutilizável
public abstract class Entity<TId>
{
    public TId Id { get; protected set; }
    public DateTime CreatedAt { get; protected set; }
    public DateTime UpdatedAt { get; protected set; }

    protected Entity()
    {
        CreatedAt = DateTime.UtcNow;
        UpdatedAt = DateTime.UtcNow;
    }
}

public class Unit : Entity<Guid> { }
public class Holder : Entity<Guid> { }

// ❌ INCORRETO - Propriedades duplicadas
public class Unit
{
    public Guid Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}

public class Holder
{
    public Guid Id { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}
```

### 3. KISS (Keep It Simple, Stupid)

Use cases simples não precisam de CQRS completo. Queries diretas quando não há lógica complexa.

```csharp
// ✅ CORRETO - Query simples sem handler
[HttpGet("{id}")]
public async Task<UnitDto> GetById(Guid id)
{
    // Lógica trivial, não precisa de handler separado
    return await _context.Units
        .AsNoTracking()
        .Where(u => u.Id == id)
        .ProjectTo<UnitDto>()
        .FirstOrDefaultAsync();
}

// ❌ OVER-ENGINEERING - Handler para query trivial
public record GetUnitByIdQuery(Guid Id) : IRequest<UnitDto>;
public class GetUnitByIdHandler : IRequestHandler<GetUnitByIdQuery, UnitDto> { }
```

### 4. YAGNI (You Aren't Gonna Need It)

Features implementadas quando necessário. Evitar abstrações prematuras.

```csharp
// ❌ INCORRETO - Abstrações que nunca serão usadas
public interface IUnitFactory { }
public interface IUnitValidator { }
public interface IUnitMapper { }
public interface IUnitCache { }
// ... todos implementando uma única classe cada

// ✅ CORRETO - Implementação direta até ser necessário
public class CreateUnitHandler
{
    // Criar unit diretamente, factory quando houver variantes
    var unit = new Unit(code, address, area);
}
```

### 5. Separation of Concerns

Cada layer tem responsabilidade única. Domain isolado de frameworks.

```
Domain: Regras de negócio puras (sem EF Core, ASP.NET)
Application: Orquestração de use cases
Infrastructure: Detalhes técnicos (banco, APIs externas)
Gateway: HTTP, serialização, autenticação
```

### 6. Fail Fast

Validações no construtor de Value Objects. FluentValidation em DTOs antes de chegar Domain.

```csharp
// Value Object valida no construtor
public record CPF
{
    public CPF(string value)
    {
        if (!IsValid(value))
            throw new InvalidCPFException($"CPF inválido: {value}");
    }
}

// FluentValidation em Commands
public class CreateUnitCommandValidator : AbstractValidator<CreateUnitCommand>
{
    public CreateUnitCommandValidator()
    {
        RuleFor(x => x.Code)
            .NotEmpty()
            .MaximLength(20);

        RuleFor(x => x.Area)
            .GreaterThan(0)
            .LessThanOrEqualTo(100000);
    }
}
```

### 7. Explicit Over Implicit

Preferir verbosidade clara a magia implícita. DTOs explícitos ao invés de automapper global.

```csharp
// ✅ CORRETO - Mapeamento explícito
public static UnitDto ToDto(this Unit unit)
{
    return new UnitDto
    {
        Id = unit.Id,
        Code = unit.Code,
        Area = unit.Area,
        // Explícito quais campos são mapeados
    };
}

// ❌ INCORRETO - Automapper mágico
// _mapper.Map<UnitDto>(unit)
// Dificulta entender transformações, debug, performance
```

### 8. Database-Agnostic Domain

Domain layer não sabe que existe database. Apenas interfaces.

```csharp
// ✅ CORRETO - Domain depende de abstração
namespace Carf.GEOAPI.Domain
{
    public interface IUnitRepository
    {
        Task<Unit?> GetByIdAsync(Guid id);
    }
}

// ❌ INCORRETO - Domain dependendo de EF Core
namespace Carf.GEOAPI.Domain
{
    using Microsoft.EntityFrameworkCore;  // ERRADO

    public class UnitService
    {
        private readonly DbContext _context;  // ERRADO
    }
}
```

### 9. Test-Driven Design

Código escrito pensando em testabilidade. Dependências injetadas via construtor.

```csharp
// ✅ TESTÁVEL - Dependências via construtor
public class CreateUnitHandler
{
    private readonly IUnitRepository _repository;
    private readonly IEventPublisher _eventPublisher;

    public CreateUnitHandler(IUnitRepository repository, IEventPublisher eventPublisher)
    {
        _repository = repository;
        _eventPublisher = eventPublisher;
    }
}

// Teste fácil com mocks
var mockRepo = new Mock<IUnitRepository>();
var handler = new CreateUnitHandler(mockRepo.Object, ...);
```

### 10. Performance Awareness

Usar `AsNoTracking()` em queries read-only. Projeções ao invés de carregar entidades completas.

```csharp
// ✅ PERFORMANCE - Projeção otimizada
var units = await _context.Units
    .AsNoTracking()  // Sem change tracking
    .Select(u => new UnitDto {
        Id = u.Id,
        Code = u.Code
        // Apenas campos necessários
    })
    .ToListAsync();

// ❌ LENTO - Carrega entidade completa com includes
var units = await _context.Units
    .Include(u => u.Holders)
    .Include(u => u.Documents)
    .ToListAsync();
```

