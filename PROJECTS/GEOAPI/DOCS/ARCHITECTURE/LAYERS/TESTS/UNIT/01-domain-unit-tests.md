# Domain Unit Tests

Testes unitários da camada de domínio.

## Unit Entity Tests

```csharp
public class UnitTests
{
    [Fact]
    public void Create_WithValidData_CreatesUnit()
    {
        // Arrange
        var address = new Address("Rua A", "1", "Bairro", "Cidade", "SP", "01310-100");
        var geometry = TestGeometry.ValidPolygon();
        var tenantId = TenantId.From(Guid.NewGuid());

        // Act
        var unit = Unit.Create(address, geometry, tenantId);

        // Assert
        unit.Should().NotBeNull();
        unit.Status.Should().Be(UnitStatus.Draft);
        unit.Area.Should().BeGreaterThan(0);
        unit.Code.Should().MatchRegex(@"^UNI-\d{4}-\d{5}$");
    }

    [Fact]
    public void Submit_WithHolders_ChangesStatusToPending()
    {
        // Arrange
        var unit = TestUnitFactory.CreateDraftUnit();
        unit.AddHolder(TestHolderFactory.Create(), OwnershipType.Owner, 100);

        // Act
        unit.Submit();

        // Assert
        unit.Status.Should().Be(UnitStatus.Pending);
    }

    [Fact]
    public void Submit_WithoutHolders_ThrowsDomainException()
    {
        // Arrange
        var unit = TestUnitFactory.CreateDraftUnit();

        // Act & Assert
        var act = () => unit.Submit();
        act.Should().Throw<DomainException>()
            .WithMessage("*at least one holder*");
    }

    [Fact]
    public void Approve_WhenPending_ChangesStatusToApproved()
    {
        // Arrange
        var unit = TestUnitFactory.CreatePendingUnit();

        // Act
        unit.Approve();

        // Assert
        unit.Status.Should().Be(UnitStatus.Approved);
    }

    [Fact]
    public void Approve_WhenDraft_ThrowsDomainException()
    {
        // Arrange
        var unit = TestUnitFactory.CreateDraftUnit();

        // Act & Assert
        var act = () => unit.Approve();
        act.Should().Throw<DomainException>()
            .WithMessage("*cannot approve*draft*");
    }
}
```

## Value Object Tests

```csharp
public class CPFTests
{
    [Theory]
    [InlineData("12345678909")]
    [InlineData("123.456.789-09")]
    public void From_ValidCPF_CreatesCPF(string cpf)
    {
        var result = CPF.From(cpf);
        result.Value.Should().Be("12345678909");
    }

    [Theory]
    [InlineData("12345678900")]
    [InlineData("11111111111")]
    [InlineData("abc")]
    public void From_InvalidCPF_ThrowsDomainException(string cpf)
    {
        var act = () => CPF.From(cpf);
        act.Should().Throw<DomainException>();
    }

    [Fact]
    public void Masked_HidesDigits()
    {
        var cpf = CPF.From("12345678909");
        cpf.Masked.Should().Be("***.***.***-09");
    }
}

public class AddressTests
{
    [Fact]
    public void FullAddress_FormatsCorrectly()
    {
        var address = new Address("Rua A", "123", "Centro", "SP", "SP", "01310-100", "Apto 1");
        address.FullAddress.Should().Be("Rua A, 123, Apto 1 - Centro, SP/SP");
    }
}
```

## Command Handler Tests

```csharp
public class CreateUnitHandlerTests
{
    private readonly Mock<IUnitRepository> _repositoryMock;
    private readonly Mock<IGeometryValidator> _validatorMock;
    private readonly CreateUnitHandler _handler;

    [Fact]
    public async Task Handle_ValidCommand_ReturnsSuccessWithUnit()
    {
        // Arrange
        _validatorMock.Setup(v => v.IsValid(It.IsAny<Geometry>())).Returns(true);
        _repositoryMock.Setup(r => r.HasOverlapAsync(It.IsAny<Geometry>(), It.IsAny<CancellationToken>()))
            .ReturnsAsync(false);

        var command = TestCommandFactory.CreateUnitCommand();

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.IsSuccess.Should().BeTrue();
        result.Value.Should().NotBeNull();
        _repositoryMock.Verify(r => r.AddAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>()), Times.Once);
    }

    [Fact]
    public async Task Handle_InvalidGeometry_ReturnsFailure()
    {
        // Arrange
        _validatorMock.Setup(v => v.IsValid(It.IsAny<Geometry>())).Returns(false);
        var command = TestCommandFactory.CreateUnitCommand();

        // Act
        var result = await _handler.Handle(command, CancellationToken.None);

        // Assert
        result.IsFailure.Should().BeTrue();
        result.Error.Code.Should().Be("INVALID_GEOMETRY");
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
