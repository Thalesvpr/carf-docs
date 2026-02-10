---
type: leaf
status: review
updated: 2026-02-08
---

# Adicionar Nova Feature - GEOAPI

Guia completo end-to-end para adicionar uma nova funcionalidade no GEOAPI seguindo os patterns DDD/CQRS com MediatR. Este guia usa um exemplo concreto: **adicionar campo `PhoneNumber` na entity `Holder`**.

---

## Visao Geral do Fluxo

```
1. Migration (DB)
2. Entity (Domain)
3. EF Configuration (Infrastructure)
4. Command/Query (Application)
5. Validator (Application)
6. DTO (Application)
7. Mapper (Application)
8. Controller (Presentation)
9. Testes Unitarios
10. Testes Integracao
11. Teste E2E
12. Commit e PR
```

Cada passo e executado na camada correspondente da Clean Architecture, de dentro para fora: Domain → Application → Infrastructure → Presentation.

---

## Passo 1: Criar Migration

**O que fazer:** Adicionar coluna `phone_number` na tabela `holders` no PostgreSQL.

**Onde:** Raiz do repositorio (CLI).

### Comando

```bash
dotnet ef migrations add 2024_06_01_AddHolderPhoneNumberColumn \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

### Editar migration gerada

**Arquivo:** `src/Carf.GeoApi.Infrastructure/Persistence/Migrations/XXXXXXXX_2024_06_01_AddHolderPhoneNumberColumn.cs`

```csharp
protected override void Up(MigrationBuilder migrationBuilder)
{
    migrationBuilder.AddColumn<string>(
        name: "phone_number",
        table: "holders",
        type: "varchar(20)",
        maxLength: 20,
        nullable: true);
}

protected override void Down(MigrationBuilder migrationBuilder)
{
    migrationBuilder.DropColumn(
        name: "phone_number",
        table: "holders");
}
```

### Aplicar migration

```bash
dotnet ef database update \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

### Verificacao

```bash
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev \
  -c "\d holders" | grep phone_number
# Esperado: phone_number | character varying(20) |
```

---

## Passo 2: Atualizar Entity (Domain Layer)

**O que fazer:** Adicionar propriedade `PhoneNumber` (Value Object) na entity `Holder`.

**Onde:** `src/Carf.GeoApi.Domain/Entities/Holder.cs`

### Antes

```csharp
public class Holder : BaseAggregateRoot
{
    public string FullName { get; private set; }
    public Cpf Cpf { get; private set; }
    public Email? Email { get; private set; }
    public Address? Address { get; private set; }
    // ...
}
```

### Depois

```csharp
public class Holder : BaseAggregateRoot
{
    public string FullName { get; private set; }
    public Cpf Cpf { get; private set; }
    public Email? Email { get; private set; }
    public PhoneNumber? PhoneNumber { get; private set; }  // ← NOVO
    public Address? Address { get; private set; }
    // ...

    // Metodo de dominio para atualizar telefone
    public void UpdatePhoneNumber(PhoneNumber? phoneNumber)
    {
        PhoneNumber = phoneNumber;
        UpdatedAt = DateTime.UtcNow;
    }
}
```

### Pattern a seguir

- Propriedades com `private set` (encapsulamento DDD)
- Usar Value Object `PhoneNumber` ao inves de `string` diretamente
- Criar metodo de dominio para mutacao (nao expor setter)
- Nullable (`?`) se o campo e opcional

### Verificacao

```bash
dotnet build src/Carf.GeoApi.Domain/
# Esperado: Build succeeded. 0 Warning(s) 0 Error(s)
```

---

## Passo 3: Atualizar EF Configuration (Infrastructure Layer)

**O que fazer:** Mapear a nova propriedade para a coluna no banco.

**Onde:** `src/Carf.GeoApi.Infrastructure/Persistence/Configurations/HolderConfiguration.cs`

### Adicionar mapeamento

```csharp
public class HolderConfiguration : IEntityTypeConfiguration<Holder>
{
    public void Configure(EntityTypeBuilder<Holder> builder)
    {
        // ... configuracoes existentes ...

        // NOVO: Mapear PhoneNumber (Value Object → coluna)
        builder.OwnsOne(h => h.PhoneNumber, phone =>
        {
            phone.Property(p => p.Value)
                .HasColumnName("phone_number")
                .HasMaxLength(20)
                .IsRequired(false);
        });
    }
}
```

### Pattern a seguir

- Value Objects mapeados com `OwnsOne()` (padrao EF Core DDD)
- `HasColumnName()` deve corresponder ao nome da coluna na migration
- `HasMaxLength()` deve corresponder ao `maxLength` da migration
- `IsRequired()` deve corresponder ao `nullable` da migration

### Verificacao

```bash
dotnet build src/Carf.GeoApi.Infrastructure/
# Esperado: Build succeeded.
```

---

## Passo 4: Criar/Atualizar Command (Application Layer)

**O que fazer:** Adicionar campo `PhoneNumber` no `UpdateHolderCommand`.

**Onde:** `src/Carf.GeoApi.Application/Commands/Holders/UpdateHolderCommand.cs`

### Command

```csharp
public record UpdateHolderCommand : IRequest<HolderDto>
{
    public Guid Id { get; init; }
    public string FullName { get; init; }
    public string Cpf { get; init; }
    public string? Email { get; init; }
    public string? PhoneNumber { get; init; }  // ← NOVO
    public UpdateAddressRequest? Address { get; init; }
}
```

### Handler

**Onde:** `src/Carf.GeoApi.Application/Commands/Holders/UpdateHolderCommandHandler.cs`

```csharp
public class UpdateHolderCommandHandler : IRequestHandler<UpdateHolderCommand, HolderDto>
{
    // ... injecao de dependencias ...

    public async Task<HolderDto> Handle(UpdateHolderCommand request, CancellationToken ct)
    {
        var holder = await _holderRepository.GetByIdAsync(request.Id, ct)
            ?? throw new NotFoundException(nameof(Holder), request.Id);

        holder.UpdateFullName(request.FullName);
        holder.UpdateCpf(new Cpf(request.Cpf));
        holder.UpdateEmail(request.Email != null ? new Email(request.Email) : null);

        // NOVO: Atualizar telefone
        holder.UpdatePhoneNumber(
            request.PhoneNumber != null
                ? new PhoneNumber(request.PhoneNumber)
                : null);

        await _holderRepository.UpdateAsync(holder, ct);
        await _unitOfWork.CommitAsync(ct);

        return _mapper.Map<HolderDto>(holder);
    }
}
```

### Pattern a seguir

- Commands sao `record` imutaveis com `IRequest<TResponse>`
- Handler recebe Command via MediatR, carrega entity, chama metodos de dominio, persiste
- Conversao de `string` para Value Object acontece no Handler
- Throw `NotFoundException` se entity nao encontrada

### Verificacao

```bash
dotnet build src/Carf.GeoApi.Application/
# Esperado: Build succeeded.
```

---

## Passo 5: Criar/Atualizar Validator (Application Layer)

**O que fazer:** Adicionar validacao de formato de telefone no `UpdateHolderCommandValidator`.

**Onde:** `src/Carf.GeoApi.Application/Commands/Holders/UpdateHolderCommandValidator.cs`

```csharp
public class UpdateHolderCommandValidator : AbstractValidator<UpdateHolderCommand>
{
    public UpdateHolderCommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty().WithMessage("Id e obrigatorio.");

        RuleFor(x => x.FullName)
            .NotEmpty().WithMessage("Nome completo e obrigatorio.")
            .MaximumLength(200);

        RuleFor(x => x.Cpf)
            .NotEmpty().WithMessage("CPF e obrigatorio.")
            .Must(BeValidCpf).WithMessage("CPF invalido.");

        // NOVO: Validacao de telefone
        RuleFor(x => x.PhoneNumber)
            .Matches(@"^\+?[1-9]\d{1,14}$")
            .When(x => x.PhoneNumber != null)
            .WithMessage("Telefone deve estar no formato E.164 (ex: +5511999998888).");

        RuleFor(x => x.PhoneNumber)
            .MaximumLength(20)
            .When(x => x.PhoneNumber != null);
    }

    private static bool BeValidCpf(string cpf)
    {
        return Cpf.IsValid(cpf);
    }
}
```

### Pattern a seguir

- Um validator por Command (mesma pasta)
- Usar `AbstractValidator<TCommand>` do FluentValidation
- Regras condicionais com `.When()` para campos opcionais
- Mensagens de erro em portugues
- Validators sao descobertos automaticamente via assembly scanning

### Verificacao

```bash
dotnet build src/Carf.GeoApi.Application/
# Esperado: Build succeeded.
```

---

## Passo 6: Criar/Atualizar DTOs (Application Layer)

**O que fazer:** Adicionar campo `PhoneNumber` nos DTOs de resposta e request.

### DTO de Resposta

**Onde:** `src/Carf.GeoApi.Application/DTOs/Holders/HolderDto.cs`

```csharp
public record HolderDto
{
    public Guid Id { get; init; }
    public string FullName { get; init; }
    public string Cpf { get; init; }
    public string? Email { get; init; }
    public string? PhoneNumber { get; init; }  // ← NOVO
    public AddressDto? Address { get; init; }
    public DateTime CreatedAt { get; init; }
    public DateTime UpdatedAt { get; init; }
}
```

### DTO de Request (se separado do Command)

**Onde:** `src/Carf.GeoApi.Application/DTOs/Holders/UpdateHolderRequest.cs`

```csharp
public record UpdateHolderRequest
{
    public string FullName { get; init; }
    public string Cpf { get; init; }
    public string? Email { get; init; }
    public string? PhoneNumber { get; init; }  // ← NOVO
    public UpdateAddressRequest? Address { get; init; }
}
```

### Pattern a seguir

- DTOs sao `record` imutaveis
- Nao conter logica de negocio
- Propriedades correspondem 1:1 com os campos do Command/Response
- Value Objects sao "achatados" para `string` nos DTOs (conversao no mapper)

### Verificacao

```bash
dotnet build src/Carf.GeoApi.Application/
# Esperado: Build succeeded.
```

---

## Passo 7: Atualizar Mapper (Application Layer)

**O que fazer:** Configurar mapeamento Entity → DTO para o novo campo.

**Onde:** `src/Carf.GeoApi.Application/Mappers/HolderProfile.cs`

```csharp
public class HolderProfile : Profile
{
    public HolderProfile()
    {
        CreateMap<Holder, HolderDto>()
            .ForMember(dest => dest.Cpf, opt => opt.MapFrom(src => src.Cpf.Value))
            .ForMember(dest => dest.Email, opt => opt.MapFrom(src => src.Email != null ? src.Email.Value : null))
            // NOVO: Mapear PhoneNumber (Value Object → string)
            .ForMember(dest => dest.PhoneNumber, opt => opt.MapFrom(src => src.PhoneNumber != null ? src.PhoneNumber.Value : null));

        CreateMap<UpdateHolderRequest, UpdateHolderCommand>();
    }
}
```

### Pattern a seguir

- Um Profile por aggregate/entity
- Value Objects mapeados extraindo `.Value`
- Nullable Value Objects verificados com ternario
- `CreateMap<Request, Command>()` para controller → MediatR

### Verificacao

```bash
dotnet build src/Carf.GeoApi.Application/
# Esperado: Build succeeded.
```

---

## Passo 8: Atualizar Controller (Presentation Layer)

**O que fazer:** Verificar se o endpoint existente ja suporta o novo campo (geralmente nao precisa alterar nada se o DTO foi atualizado). Se um novo endpoint for necessario, criar aqui.

**Onde:** `src/Carf.GeoApi.Gateway/Controllers/HoldersController.cs`

### Verificar endpoint existente

```csharp
[HttpPut("{id:guid}")]
[Authorize(Roles = "coordinator,admin")]
[ProducesResponseType(typeof(HolderDto), StatusCodes.Status200OK)]
[ProducesResponseType(StatusCodes.Status404NotFound)]
[ProducesResponseType(StatusCodes.Status400BadRequest)]
public async Task<IActionResult> Update(Guid id, [FromBody] UpdateHolderRequest request)
{
    var command = _mapper.Map<UpdateHolderCommand>(request);
    command = command with { Id = id };  // setar Id do route param

    var result = await _mediator.Send(command);
    return Ok(result);
}
```

> **Neste caso nao e necessario alterar o controller.** O campo `PhoneNumber` ja flui automaticamente via `UpdateHolderRequest` → `UpdateHolderCommand` → Handler → Entity → `HolderDto`.

### Quando criar novo endpoint

Se a feature requer um endpoint completamente novo (ex: `POST /api/v1/holders/{id}/verify-phone`), seguir o pattern:

```csharp
[HttpPost("{id:guid}/verify-phone")]
[Authorize(Roles = "coordinator,admin")]
[ProducesResponseType(StatusCodes.Status204NoContent)]
public async Task<IActionResult> VerifyPhone(Guid id, [FromBody] VerifyPhoneRequest request)
{
    var command = new VerifyHolderPhoneCommand { HolderId = id, Code = request.Code };
    await _mediator.Send(command);
    return NoContent();
}
```

### Pattern a seguir

- Um controller por aggregate root
- Atributos `[Authorize(Roles = "...")]` para RBAC
- `[ProducesResponseType]` para documentacao Swagger
- Delegar toda logica para MediatR (controller e thin)
- Route convention: `/api/v1/{resource}/{id}/{sub-resource}`

### Verificacao

```bash
dotnet build src/Carf.GeoApi.Gateway/
# Esperado: Build succeeded.

dotnet run --project src/Carf.GeoApi.Gateway/
# Abrir Swagger: https://localhost:7001/swagger
# Verificar que PUT /api/v1/holders/{id} agora mostra PhoneNumber no schema
```

---

## Passo 9: Escrever Testes Unitarios

### 9.1 Teste do Handler

**Onde:** `tests/Carf.GeoApi.Application.Tests/Commands/Holders/UpdateHolderCommandHandlerTests.cs`

```csharp
public class UpdateHolderCommandHandlerTests
{
    private readonly Mock<IHolderRepository> _repositoryMock;
    private readonly Mock<IUnitOfWork> _unitOfWorkMock;
    private readonly Mock<IMapper> _mapperMock;
    private readonly UpdateHolderCommandHandler _handler;

    public UpdateHolderCommandHandlerTests()
    {
        _repositoryMock = new Mock<IHolderRepository>();
        _unitOfWorkMock = new Mock<IUnitOfWork>();
        _mapperMock = new Mock<IMapper>();
        _handler = new UpdateHolderCommandHandler(
            _repositoryMock.Object,
            _unitOfWorkMock.Object,
            _mapperMock.Object);
    }

    [Fact]
    public async Task Handle_WithValidPhoneNumber_ShouldUpdateHolder()
    {
        // Arrange
        var holderId = Guid.NewGuid();
        var holder = HolderFactory.Create(holderId);
        var command = new UpdateHolderCommand
        {
            Id = holderId,
            FullName = "Joao Silva",
            Cpf = "12345678901",
            PhoneNumber = "+5511999998888"
        };

        _repositoryMock.Setup(r => r.GetByIdAsync(holderId, It.IsAny<CancellationToken>()))
            .ReturnsAsync(holder);
        _mapperMock.Setup(m => m.Map<HolderDto>(It.IsAny<Holder>()))
            .Returns(new HolderDto { Id = holderId, PhoneNumber = "+5511999998888" });

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.PhoneNumber.Should().Be("+5511999998888");
        _repositoryMock.Verify(r => r.UpdateAsync(It.IsAny<Holder>(), It.IsAny<CancellationToken>()), Times.Once);
        _unitOfWorkMock.Verify(u => u.CommitAsync(It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task Handle_WithNullPhoneNumber_ShouldClearPhoneNumber()
    {
        // Arrange
        var holderId = Guid.NewGuid();
        var holder = HolderFactory.CreateWithPhone(holderId, "+5511999998888");
        var command = new UpdateHolderCommand
        {
            Id = holderId,
            FullName = "Joao Silva",
            Cpf = "12345678901",
            PhoneNumber = null  // limpar telefone
        };

        _repositoryMock.Setup(r => r.GetByIdAsync(holderId, It.IsAny<CancellationToken>()))
            .ReturnsAsync(holder);
        _mapperMock.Setup(m => m.Map<HolderDto>(It.IsAny<Holder>()))
            .Returns(new HolderDto { Id = holderId, PhoneNumber = null });

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.PhoneNumber.Should().BeNull();
    }
}
```

### 9.2 Teste do Validator

**Onde:** `tests/Carf.GeoApi.Application.Tests/Validators/Holders/UpdateHolderCommandValidatorTests.cs`

```csharp
public class UpdateHolderCommandValidatorTests
{
    private readonly UpdateHolderCommandValidator _validator = new();

    [Theory]
    [InlineData("+5511999998888")]
    [InlineData("+1234567890")]
    [InlineData("+553199887766")]
    public void Validate_ValidPhoneNumber_ShouldPass(string phone)
    {
        var command = ValidCommandWith(phone: phone);
        var result = _validator.Validate(command);
        result.IsValid.Should().BeTrue();
    }

    [Theory]
    [InlineData("abc")]
    [InlineData("11999998888")]     // sem codigo pais
    [InlineData("+0111234567")]     // comeca com 0
    [InlineData("")]
    public void Validate_InvalidPhoneNumber_ShouldFail(string phone)
    {
        var command = ValidCommandWith(phone: phone);
        var result = _validator.Validate(command);
        result.IsValid.Should().BeFalse();
        result.Errors.Should().Contain(e => e.PropertyName == "PhoneNumber");
    }

    [Fact]
    public void Validate_NullPhoneNumber_ShouldPass()
    {
        var command = ValidCommandWith(phone: null);
        var result = _validator.Validate(command);
        // PhoneNumber e opcional, null deve ser valido
        result.Errors.Should().NotContain(e => e.PropertyName == "PhoneNumber");
    }

    private static UpdateHolderCommand ValidCommandWith(string? phone) => new()
    {
        Id = Guid.NewGuid(),
        FullName = "Joao Silva",
        Cpf = "12345678901",
        PhoneNumber = phone
    };
}
```

### Pattern a seguir

- Um arquivo de teste por classe testada
- Nome: `{ClasseTestada}Tests.cs`
- Usar `Fact` para cenarios unicos, `Theory` + `InlineData` para multiplos inputs
- Arrange/Act/Assert com FluentAssertions (`.Should()`)
- Mocks com Moq para dependencias

### Verificacao

```bash
dotnet test tests/Carf.GeoApi.Application.Tests/ --filter "Holder"
# Esperado: todos os testes passam
```

---

## Passo 10: Escrever Testes de Integracao

**O que fazer:** Testar que o campo e persistido corretamente no banco real.

**Onde:** `tests/Carf.GeoApi.Infrastructure.Tests/Repositories/HolderRepositoryTests.cs`

```csharp
public class HolderRepositoryTests : IntegrationTestBase
{
    [Fact]
    public async Task UpdateAsync_WithPhoneNumber_ShouldPersistPhoneNumber()
    {
        // Arrange
        var holder = HolderFactory.Create();
        await _repository.AddAsync(holder, CancellationToken.None);
        await _unitOfWork.CommitAsync(CancellationToken.None);

        // Act
        holder.UpdatePhoneNumber(new PhoneNumber("+5511999998888"));
        await _repository.UpdateAsync(holder, CancellationToken.None);
        await _unitOfWork.CommitAsync(CancellationToken.None);

        // Assert - recarregar do banco
        var saved = await _repository.GetByIdAsync(holder.Id, CancellationToken.None);
        saved.Should().NotBeNull();
        saved!.PhoneNumber.Should().NotBeNull();
        saved.PhoneNumber!.Value.Should().Be("+5511999998888");
    }

    [Fact]
    public async Task UpdateAsync_ClearPhoneNumber_ShouldPersistNull()
    {
        // Arrange
        var holder = HolderFactory.CreateWithPhone(phone: "+5511999998888");
        await _repository.AddAsync(holder, CancellationToken.None);
        await _unitOfWork.CommitAsync(CancellationToken.None);

        // Act
        holder.UpdatePhoneNumber(null);
        await _repository.UpdateAsync(holder, CancellationToken.None);
        await _unitOfWork.CommitAsync(CancellationToken.None);

        // Assert
        var saved = await _repository.GetByIdAsync(holder.Id, CancellationToken.None);
        saved!.PhoneNumber.Should().BeNull();
    }
}
```

### Pattern a seguir

- Herdar de `IntegrationTestBase` (configura banco in-memory ou Testcontainers PostgreSQL)
- Testar round-trip: criar → persistir → recarregar → assert
- Testar cenarios nulos/opccionais

### Verificacao

```bash
dotnet test tests/Carf.GeoApi.Infrastructure.Tests/ --filter "HolderRepository"
# Esperado: todos os testes passam
```

---

## Passo 11: Testar End-to-End

### Via Swagger UI

1. Abrir `https://localhost:7001/swagger`
2. Autenticar (clicar "Authorize" e inserir token Bearer)
3. Encontrar `PUT /api/v1/holders/{id}`
4. Clicar "Try it out"
5. Preencher body com `PhoneNumber`:

```json
{
  "fullName": "Joao Silva",
  "cpf": "12345678901",
  "email": "joao@test.com",
  "phoneNumber": "+5511999998888"
}
```

6. Verificar resposta 200 com `phoneNumber` no retorno

### Via cURL

```bash
# 1. Obter token
TOKEN=$(curl -s -X POST http://localhost:8080/realms/carf/protocol/openid-connect/token \
  -d "grant_type=password&client_id=geoapi&username=dev@carf.local&password=dev123" \
  | jq -r .access_token)

# 2. Criar holder (se nao existir)
HOLDER_ID=$(curl -s -X POST http://localhost:5001/api/v1/holders \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fullName":"Joao Silva","cpf":"12345678901"}' \
  | jq -r .id)

# 3. Atualizar com PhoneNumber
curl -s -X PUT "http://localhost:5001/api/v1/holders/$HOLDER_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Joao Silva",
    "cpf": "12345678901",
    "phoneNumber": "+5511999998888"
  }' | jq .

# 4. Verificar no GET
curl -s -H "Authorization: Bearer $TOKEN" \
  "http://localhost:5001/api/v1/holders/$HOLDER_ID" | jq .phoneNumber
# Esperado: "+5511999998888"
```

### Verificar no banco

```bash
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev \
  -c "SELECT id, full_name, phone_number FROM holders WHERE phone_number IS NOT NULL;"
```

---

## Passo 12: Commit e Pull Request

### Arquivos alterados neste exemplo

```
src/Carf.GeoApi.Domain/Entities/Holder.cs                              (entity)
src/Carf.GeoApi.Infrastructure/Persistence/Configurations/HolderConfiguration.cs  (EF config)
src/Carf.GeoApi.Infrastructure/Persistence/Migrations/XXXX_AddHolderPhoneNumberColumn.cs  (migration)
src/Carf.GeoApi.Infrastructure/Persistence/Migrations/AppDbContextModelSnapshot.cs  (snapshot)
src/Carf.GeoApi.Application/Commands/Holders/UpdateHolderCommand.cs    (command)
src/Carf.GeoApi.Application/Commands/Holders/UpdateHolderCommandHandler.cs  (handler)
src/Carf.GeoApi.Application/Commands/Holders/UpdateHolderCommandValidator.cs  (validator)
src/Carf.GeoApi.Application/DTOs/Holders/HolderDto.cs                 (DTO resposta)
src/Carf.GeoApi.Application/DTOs/Holders/UpdateHolderRequest.cs       (DTO request)
src/Carf.GeoApi.Application/Mappers/HolderProfile.cs                  (mapper)
tests/Carf.GeoApi.Application.Tests/Commands/Holders/UpdateHolderCommandHandlerTests.cs  (teste unitario)
tests/Carf.GeoApi.Application.Tests/Validators/Holders/UpdateHolderCommandValidatorTests.cs  (teste validator)
tests/Carf.GeoApi.Infrastructure.Tests/Repositories/HolderRepositoryTests.cs  (teste integracao)
```

### Commit

```bash
git add -A
git commit -m "feat(holders): add PhoneNumber field to Holder entity

- Add phone_number column via EF Core migration
- Add PhoneNumber value object to Holder aggregate
- Update UpdateHolderCommand/Validator/Handler
- Update DTOs and AutoMapper profile
- Add unit tests for handler and validator
- Add integration tests for repository persistence"
```

### Pull Request

```bash
git push -u origin feature/holder-phone-number
gh pr create --title "feat(holders): add PhoneNumber field" \
  --body "Adiciona campo de telefone no Holder seguindo pattern E.164"
```

---

## Checklist Final

| Verificacao | Status |
|-------------|--------|
| Migration criada com `Up()` e `Down()` corretos | |
| Entity atualizada com Value Object e metodo de dominio | |
| EF Configuration mapeando Value Object para coluna | |
| Command com novo campo | |
| Handler usando metodo de dominio para atualizar | |
| Validator com regras para formato E.164 | |
| DTOs de request e response atualizados | |
| Mapper configurado para Value Object → string | |
| Controller funciona (verificar Swagger) | |
| Testes unitarios do handler passam | |
| Testes do validator cobrem casos validos e invalidos | |
| Testes de integracao verificam persistencia | |
| Teste E2E via curl/Swagger funciona | |
| Build completo sem warnings | |
| `dotnet test` all green | |

---

## Variantes Comuns

### Adicionar campo calculado (read-only)

Se o campo nao e editavel (ex: `HolderAge` calculado a partir de `BirthDate`):
- Nao criar Command/Validator (campo nao e input)
- Adicionar propriedade computada na Entity ou no DTO via Mapper
- Pode ser calculado via SQL (computed column) na migration

### Adicionar relacionamento (nova entity filha)

Se a feature requer uma nova entity relacionada:
1. Criar Entity no Domain
2. Criar IRepository no Domain (contract)
3. Criar Repository na Infrastructure
4. Criar Configuration na Infrastructure
5. Criar Migration
6. Registrar Repository no DI (Program.cs)
7. Seguir passos 4-12 normalmente

### Adicionar novo endpoint (sem alterar entity)

Se a feature e apenas um novo endpoint de consulta:
1. Criar Query + Handler (Application)
2. Criar DTO de resposta (Application)
3. Criar endpoint no Controller (Presentation)
4. Testes unitarios do handler
5. Teste E2E

---

## Referencias

| Recurso | Link |
|---------|------|
| Migrations guide | [05-database-migrations.md](./05-database-migrations.md) |
| Domain entities | [DOMAIN/ENTITIES/](../ARCHITECTURE/LAYERS/DOMAIN/ENTITIES/) |
| Application commands | [APPLICATION/COMMANDS/](../ARCHITECTURE/LAYERS/APPLICATION/COMMANDS/) |
| Application validators | [APPLICATION/VALIDATORS/](../ARCHITECTURE/LAYERS/APPLICATION/VALIDATORS/) |
| Presentation controllers | [PRESENTATION/CONTROLLERS/](../ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/) |
| Unit tests | [TESTS/UNIT/](../ARCHITECTURE/LAYERS/TESTS/UNIT/) |
| Integration tests | [TESTS/INTEGRATION/](../ARCHITECTURE/LAYERS/TESTS/INTEGRATION/) |
