# Fluxo de Dados - GEOAPI

## Visão Geral

Este documento descreve como os dados fluem através das camadas do GEOAPI conforme [arquitetura geral documentada](./01-overview.md) implementando [CQRS Pattern](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-009-cqrs-pattern.md), desde a requisição HTTP até a persistência no banco de dados via [endpoints especificados](../../../../CENTRAL/API/README.md) com [integrações externas](./04-integration.md) e retorno da resposta.

## Diagrama de Fluxo Geral

```
┌─────────────┐
│   CLIENT    │  (GEOWEB, REURBCAD, ADMIN, GEOGIS)
│   (HTTP)    │
└──────┬──────┘
       │
       │ POST /api/units
       │ { address, coordinates, area }
       │
       ▼
┌──────────────────────────────────────────────────────┐
│                  GATEWAY LAYER                       │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  1. AuthenticationMiddleware               │    │
│  │     - Validate JWT token (Keycloak)        │    │
│  │     - Extract user_id, tenant_id, roles    │    │
│  └──────────────┬─────────────────────────────┘    │
│                 │                                    │
│  ┌──────────────▼─────────────────────────────┐    │
│  │  2. TenantMiddleware                       │    │
│  │     - Set HttpContext.Items["TenantId"]    │    │
│  └──────────────┬─────────────────────────────┘    │
│                 │                                    │
│  ┌──────────────▼─────────────────────────────┐    │
│  │  3. UnitsController.CreateUnit()           │    │
│  │     - Receive CreateUnitDto                │    │
│  └──────────────┬─────────────────────────────┘    │
│                 │                                    │
│  ┌──────────────▼─────────────────────────────┐    │
│  │  4. ValidationFilter                       │    │
│  │     - FluentValidation on DTO              │    │
│  │     - Return 400 if invalid                │    │
│  └──────────────┬─────────────────────────────┘    │
└─────────────────┼──────────────────────────────────┘
                  │
                  │ Send CreateUnitCommand
                  │
                  ▼
┌──────────────────────────────────────────────────────┐
│              APPLICATION LAYER                       │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  5. MediatR sends to Handler               │    │
│  │     CreateUnitCommandHandler               │    │
│  └──────────────┬─────────────────────────────┘    │
│                 │                                    │
│  ┌──────────────▼─────────────────────────────┐    │
│  │  6. Handler logic                          │    │
│  │     - Map DTO → Domain Entity (Unit)       │    │
│  │     - Apply business rules                 │    │
│  │     - Validate domain invariants           │    │
│  └──────────────┬─────────────────────────────┘    │
└─────────────────┼──────────────────────────────────┘
                  │
                  │ Call Domain
                  │
                  ▼
┌──────────────────────────────────────────────────────┐
│                 DOMAIN LAYER                         │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  7. Unit.Create() factory method           │    │
│  │     - Validate coordinates (SIRGAS2000)    │    │
│  │     - Validate area > 0                    │    │
│  │     - Create Address value object          │    │
│  │     - Raise UnitCreatedEvent               │    │
│  └──────────────┬─────────────────────────────┘    │
└─────────────────┼──────────────────────────────────┘
                  │
                  │ Return Unit entity
                  │
                  ▼
┌──────────────────────────────────────────────────────┐
│              APPLICATION LAYER                       │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  8. Handler persists                       │    │
│  │     await _unitRepository.AddAsync(unit)   │    │
│  └──────────────┬─────────────────────────────┘    │
└─────────────────┼──────────────────────────────────┘
                  │
                  │ Call Repository
                  │
                  ▼
┌──────────────────────────────────────────────────────┐
│            INFRASTRUCTURE LAYER                      │
│                                                      │
│  ┌────────────────────────────────────────────┐    │
│  │  9. UnitRepository.AddAsync()              │    │
│  │     _context.Units.Add(unit)               │    │
│  │     await _context.SaveChangesAsync()      │    │
│  └──────────────┬─────────────────────────────┘    │
│                 │                                    │
│                 │ Execute SQL                        │
│                 │                                    │
│  ┌──────────────▼─────────────────────────────┐    │
│  │  10. PostgreSQL with RLS                   │    │
│  │      INSERT INTO units (...)               │    │
│  │      WHERE tenant_id = current_setting     │    │
│  │            ('app.tenant_id')               │    │
│  └──────────────┬─────────────────────────────┘    │
└─────────────────┼──────────────────────────────────┘
                  │
                  │ Return saved entity
                  │
                  ▼
        ┌─────────────────┐
        │   RESPONSE      │
        │   201 Created   │
        │   UnitDto       │
        └─────────────────┘
```

## Fluxo Detalhado por Operação

### 1. CREATE (POST) - Fluxo de Escrita

#### Request
```http
POST /api/units HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "address": "Rua Example, 123",
  "neighborhood": "Centro",
  "city": "São Paulo",
  "state": "SP",
  "zipCode": "01234-567",
  "coordinates": {
    "latitude": -23.5505,
    "longitude": -46.6333
  },
  "area": 250.5,
  "holders": [
    {
      "name": "João Silva",
      "cpf": "123.456.789-00",
      "email": "joao@example.com"
    }
  ]
}
```

#### Step-by-Step Flow

**1. Authentication Middleware**
```csharp
// Validate JWT token from Keycloak
var token = httpContext.Request.Headers["Authorization"];
var isValid = await _keycloakService.ValidateTokenAsync(token);

if (!isValid)
    return Unauthorized();

// Extract claims
var userId = token.Claims["sub"];
var tenantId = token.Claims["tenant_id"];
var roles = token.Claims["roles"];

// Set in HttpContext
httpContext.Items["UserId"] = userId;
httpContext.Items["TenantId"] = tenantId;
httpContext.Items["Roles"] = roles;
```

**2. Tenant Middleware**
```csharp
// Configure PostgreSQL session for RLS
var tenantId = httpContext.Items["TenantId"];
await _dbContext.Database.ExecuteSqlRawAsync(
    $"SET LOCAL app.tenant_id = '{tenantId}'"
);
```

**3. Controller receives request**
```csharp
[HttpPost]
[Authorize(Roles = "analyst,admin")]
public async Task<ActionResult<UnitDto>> CreateUnit([FromBody] CreateUnitDto dto)
{
    var command = new CreateUnitCommand(dto);
    var result = await _mediator.Send(command);
    return CreatedAtAction(nameof(GetUnit), new { id = result.Id }, result);
}
```

**4. Validation Filter**
```csharp
public class CreateUnitDtoValidator : AbstractValidator<CreateUnitDto>
{
    public CreateUnitDtoValidator()
    {
        RuleFor(x => x.Address).NotEmpty();
        RuleFor(x => x.Coordinates)
            .NotNull()
            .Must(BeValidCoordinates).WithMessage("Invalid SIRGAS2000 coordinates");
        RuleFor(x => x.Area)
            .GreaterThan(0).WithMessage("Area must be positive");
        RuleFor(x => x.Holders)
            .NotEmpty().WithMessage("At least one holder required");
    }
}
```

**5. MediatR dispatches to Handler**
```csharp
public class CreateUnitCommandHandler : IRequestHandler<CreateUnitCommand, UnitDto>
{
    private readonly IUnitRepository _repository;
    private readonly IMapper _mapper;

    public async Task<UnitDto> Handle(CreateUnitCommand request, CancellationToken ct)
    {
        // 6. Map DTO to Domain
        var unit = Unit.Create(
            address: Address.Create(request.Dto.Address, ...),
            coordinates: Coordinates.Create(request.Dto.Coordinates.Lat, request.Dto.Coordinates.Lng),
            area: new Area(request.Dto.Area)
        );

        // Add holders
        foreach (var holderDto in request.Dto.Holders)
        {
            var holder = Holder.Create(
                name: holderDto.Name,
                cpf: CPF.Create(holderDto.Cpf),
                email: Email.Create(holderDto.Email)
            );
            unit.AddHolder(holder);
        }

        // 7. Domain validation happens in constructors/factory methods
        // Unit.Create throws DomainException if invalid

        // 8. Persist
        await _repository.AddAsync(unit);

        // 9. Dispatch domain events
        await _domainEventDispatcher.DispatchAsync(unit.DomainEvents);

        // 10. Map to DTO and return
        return _mapper.Map<UnitDto>(unit);
    }
}
```

**6-7. Domain Layer**
```csharp
public class Unit : AggregateRoot<UnitId>
{
    public Address Address { get; private set; }
    public Coordinates Coordinates { get; private set; }
    public Area Area { get; private set; }
    private List<Holder> _holders = new();

    private Unit() { } // EF Core

    public static Unit Create(Address address, Coordinates coordinates, Area area)
    {
        // Domain validation
        if (coordinates.IsOutOfBrazil())
            throw new DomainException("Coordinates must be in Brazil");

        if (area.Value <= 0)
            throw new DomainException("Area must be positive");

        var unit = new Unit
        {
            Id = UnitId.New(),
            Address = address,
            Coordinates = coordinates,
            Area = area,
            CreatedAt = DateTime.UtcNow
        };

        // Raise domain event
        unit.RaiseDomainEvent(new UnitCreatedEvent(unit.Id));

        return unit;
    }

    public void AddHolder(Holder holder)
    {
        if (_holders.Count >= 5)
            throw new DomainException("Maximum 5 holders per unit");

        _holders.Add(holder);
    }
}
```

**8-9. Infrastructure Layer**
```csharp
public class UnitRepository : Repository<Unit>, IUnitRepository
{
    public UnitRepository(CarfDbContext context) : base(context) { }

    public async Task AddAsync(Unit unit)
    {
        await _context.Units.AddAsync(unit);
        await _context.SaveChangesAsync(); // Commit transaction
    }
}
```

**10. PostgreSQL with RLS**
```sql
-- RLS Policy automatically applied
INSERT INTO units (id, address, coordinates, area, tenant_id, created_at)
VALUES (
    'uuid-here',
    '{"street": "Rua Example", "number": "123", ...}',
    ST_SetSRID(ST_MakePoint(-46.6333, -23.5505), 4674), -- SIRGAS2000
    250.5,
    current_setting('app.tenant_id')::uuid, -- Tenant from session variable
    NOW()
)
RETURNING *;
```

#### Response
```http
HTTP/1.1 201 Created
Location: /api/units/d290f1ee-6c54-4b01-90e6-d701748f0851
Content-Type: application/json

{
  "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "address": "Rua Example, 123, Centro, São Paulo-SP, 01234-567",
  "coordinates": {
    "latitude": -23.5505,
    "longitude": -46.6333
  },
  "area": 250.5,
  "holders": [
    {
      "id": "holder-uuid",
      "name": "João Silva",
      "cpf": "123.456.789-00"
    }
  ],
  "createdAt": "2026-01-09T15:30:00Z"
}
```

---

### 2. READ (GET) - Fluxo de Leitura

#### Request
```http
GET /api/units/d290f1ee-6c54-4b01-90e6-d701748f0851 HTTP/1.1
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Flow (Simplified via Query)

**1-2. Authentication + Tenant Middleware** (same as CREATE)

**3. Controller**
```csharp
[HttpGet("{id}")]
public async Task<ActionResult<UnitDto>> GetUnit(Guid id)
{
    var query = new GetUnitByIdQuery(id);
    var result = await _mediator.Send(query);

    if (result == null)
        return NotFound();

    return Ok(result);
}
```

**4. Query Handler**
```csharp
public class GetUnitByIdQueryHandler : IRequestHandler<GetUnitByIdQuery, UnitDto>
{
    private readonly IUnitRepository _repository;
    private readonly IMapper _mapper;

    public async Task<UnitDto?> Handle(GetUnitByIdQuery request, CancellationToken ct)
    {
        var unit = await _repository.GetByIdAsync(new UnitId(request.Id));

        if (unit == null)
            return null;

        return _mapper.Map<UnitDto>(unit);
    }
}
```

**5. Repository Query**
```csharp
public async Task<Unit?> GetByIdAsync(UnitId id)
{
    return await _context.Units
        .Include(u => u.Holders)
        .Include(u => u.Community)
        .FirstOrDefaultAsync(u => u.Id == id);
}
```

**6. PostgreSQL with RLS**
```sql
-- RLS Policy automatically filters by tenant
SELECT u.*, h.*
FROM units u
LEFT JOIN holders h ON h.unit_id = u.id
WHERE u.id = 'd290f1ee-6c54-4b01-90e6-d701748f0851'
  AND u.tenant_id = current_setting('app.tenant_id')::uuid; -- RLS enforced
```

#### Response
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "address": "Rua Example, 123, Centro, São Paulo-SP",
  "coordinates": { "latitude": -23.5505, "longitude": -46.6333 },
  "area": 250.5,
  "holders": [...]
}
```

---

## Transformações de Dados

### DTO → Domain Entity

```csharp
// DTO (Gateway layer)
CreateUnitDto dto = {
    Address = "Rua Example, 123",
    Coordinates = { Latitude = -23.5505, Longitude = -46.6333 },
    Area = 250.5
};

// Transform to Domain Entity (Application layer)
Unit unit = Unit.Create(
    address: Address.Create(dto.Address, dto.Neighborhood, dto.City, dto.State, dto.ZipCode),
    coordinates: Coordinates.Create(dto.Coordinates.Latitude, dto.Coordinates.Longitude),
    area: new Area(dto.Area)
);

// Domain Entity (Domain layer)
public class Unit
{
    public UnitId Id { get; private set; }
    public Address Address { get; private set; } // Value Object
    public Coordinates Coordinates { get; private set; } // Value Object
    public Area Area { get; private set; } // Value Object
}
```

### Domain Entity → DTO

```csharp
// Domain Entity
Unit unit = await _repository.GetByIdAsync(unitId);

// AutoMapper configuration
CreateMap<Unit, UnitDto>()
    .ForMember(dest => dest.Address, opt => opt.MapFrom(src => src.Address.ToString()))
    .ForMember(dest => dest.Coordinates, opt => opt.MapFrom(src => new CoordinatesDto
    {
        Latitude = src.Coordinates.Latitude,
        Longitude = src.Coordinates.Longitude
    }))
    .ForMember(dest => dest.Area, opt => opt.MapFrom(src => src.Area.Value));

// Result DTO
UnitDto dto = _mapper.Map<UnitDto>(unit);
```

---

## Validação de Dados em Múltiplas Camadas

### 1. Gateway Layer (DTOs)
```csharp
// FluentValidation
RuleFor(x => x.Coordinates).NotNull();
RuleFor(x => x.Area).GreaterThan(0);
```
**Valida:** Formato, presença, tipos básicos

### 2. Application Layer (Handlers)
```csharp
// Business validation
if (await _unitRepository.ExistsByCoordinatesAsync(coordinates))
    throw new BusinessException("Unit already exists at these coordinates");
```
**Valida:** Regras de negócio, duplicação

### 3. Domain Layer (Entities/Value Objects)
```csharp
// Domain invariants
public Coordinates(decimal latitude, decimal longitude)
{
    if (latitude < -90 || latitude > 90)
        throw new DomainException("Invalid latitude");

    if (longitude < -180 || longitude > 180)
        throw new DomainException("Invalid longitude");

    Latitude = latitude;
    Longitude = longitude;
}
```
**Valida:** Invariantes de domínio, consistência interna

### 4. Infrastructure Layer (Database)
```sql
-- Database constraints
ALTER TABLE units
ADD CONSTRAINT area_positive CHECK (area > 0);

CREATE INDEX idx_units_coordinates ON units USING GIST (coordinates);
```
**Valida:** Constraints de integridade, uniqueness

---

## Multi-tenancy Data Isolation

### Flow com RLS

```
1. JWT Token contém tenant_id claim
   { "tenant_id": "municipality-sp-123" }

2. Tenant Middleware extrai e configura sessão PostgreSQL
   SET LOCAL app.tenant_id = 'municipality-sp-123';

3. RLS Policy filtra automaticamente todas as queries
   CREATE POLICY tenant_isolation_policy ON units
   FOR ALL
   USING (tenant_id = current_setting('app.tenant_id')::uuid);

4. Queries automáticas SEM código adicional
   SELECT * FROM units; -- Only returns units for tenant-sp-123

5. Inserts automáticos COM tenant_id
   INSERT INTO units (...) VALUES (..., current_setting('app.tenant_id'));
```

**Benefício:** Isolamento garantido pelo banco de dados, impossível vazar dados entre tenants.

---

## Fluxo de Domain Events

```
1. Unit.Create() → RaiseDomainEvent(new UnitCreatedEvent())
2. Handler calls _repository.AddAsync(unit)
3. After SaveChangesAsync(), dispatch events
4. Event Handlers process:
   - Send notification email
   - Update statistics
   - Trigger workflow
   - Publish to message bus (future)
```
