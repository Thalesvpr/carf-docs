# Domain Unit Tests

Testes unitários para camada de domínio do CARF.

## Entities

### Unit Entity

```csharp
// GEOAPI.Domain.Tests/Entities/UnitTests.cs
public class UnitTests
{
    [Fact]
    public void Create_WithValidData_ShouldCreateUnit()
    {
        // Arrange
        var address = new Address("Rua das Flores", "123", "Centro", "São Paulo", "SP", "01310-100");
        var geometry = TestGeometryFactory.CreateValidPolygon();

        // Act
        var unit = Unit.Create(address, geometry, TenantId.From(Guid.NewGuid()));

        // Assert
        unit.Should().NotBeNull();
        unit.Status.Should().Be(UnitStatus.Draft);
        unit.Area.Should().BeGreaterThan(0);
        unit.Code.Should().StartWith("UNI-");
    }

    [Fact]
    public void Create_WithSelfIntersectingPolygon_ShouldThrowDomainException()
    {
        // Arrange
        var address = new Address("Rua das Flores", "123", "Centro", "São Paulo", "SP", "01310-100");
        var invalidGeometry = TestGeometryFactory.CreateSelfIntersectingPolygon();

        // Act & Assert
        var act = () => Unit.Create(address, invalidGeometry, TenantId.From(Guid.NewGuid()));
        act.Should().Throw<DomainException>()
            .WithMessage("*self-intersection*");
    }

    [Fact]
    public void Submit_WhenDraft_ShouldChangeStatusToPending()
    {
        // Arrange
        var unit = TestUnitFactory.CreateDraftUnit();
        unit.AddHolder(TestHolderFactory.CreateHolder(), OwnershipType.Owner, 100);

        // Act
        unit.Submit();

        // Assert
        unit.Status.Should().Be(UnitStatus.Pending);
    }

    [Fact]
    public void Submit_WithoutHolders_ShouldThrowDomainException()
    {
        // Arrange
        var unit = TestUnitFactory.CreateDraftUnit();

        // Act & Assert
        var act = () => unit.Submit();
        act.Should().Throw<DomainException>()
            .WithMessage("*at least one holder*");
    }
}
```

### Holder Entity

```csharp
// GEOAPI.Domain.Tests/Entities/HolderTests.cs
public class HolderTests
{
    [Theory]
    [InlineData("12345678909")] // CPF válido
    [InlineData("123.456.789-09")] // CPF formatado válido
    public void Create_WithValidCpf_ShouldCreateHolder(string cpf)
    {
        // Arrange & Act
        var holder = Holder.Create(
            "Maria da Silva",
            CPF.From(cpf),
            new DateTime(1985, 3, 15),
            TenantId.From(Guid.NewGuid())
        );

        // Assert
        holder.Should().NotBeNull();
        holder.Cpf.Value.Should().Be("12345678909"); // Normalizado
    }

    [Theory]
    [InlineData("12345678900")] // Dígitos verificadores inválidos
    [InlineData("11111111111")] // Todos dígitos iguais
    [InlineData("123")]         // Muito curto
    public void Create_WithInvalidCpf_ShouldThrowDomainException(string cpf)
    {
        // Act & Assert
        var act = () => CPF.From(cpf);
        act.Should().Throw<DomainException>()
            .WithMessage("*Invalid CPF*");
    }

    [Fact]
    public void Create_WithMinorAge_ShouldThrowDomainException()
    {
        // Arrange
        var minorBirthDate = DateTime.Today.AddYears(-17);

        // Act & Assert
        var act = () => Holder.Create(
            "João Menor",
            CPF.From("12345678909"),
            minorBirthDate,
            TenantId.From(Guid.NewGuid())
        );
        act.Should().Throw<DomainException>()
            .WithMessage("*must be at least 18*");
    }
}
```

## Value Objects

### CPF Value Object

```csharp
// GEOAPI.Domain.Tests/ValueObjects/CpfTests.cs
public class CpfTests
{
    [Fact]
    public void Equals_SameValue_ShouldBeEqual()
    {
        var cpf1 = CPF.From("123.456.789-09");
        var cpf2 = CPF.From("12345678909");

        cpf1.Should().Be(cpf2);
    }

    [Fact]
    public void ToString_ShouldReturnFormatted()
    {
        var cpf = CPF.From("12345678909");

        cpf.ToString().Should().Be("123.456.789-09");
    }

    [Fact]
    public void Masked_ShouldHideDigits()
    {
        var cpf = CPF.From("12345678909");

        cpf.Masked.Should().Be("***.***.***-09");
    }
}
```

### Address Value Object

```csharp
// GEOAPI.Domain.Tests/ValueObjects/AddressTests.cs
public class AddressTests
{
    [Fact]
    public void FullAddress_ShouldConcatenateCorrectly()
    {
        var address = new Address(
            "Rua das Flores", "123", "Centro",
            "São Paulo", "SP", "01310-100", "Apto 42"
        );

        address.FullAddress.Should().Be(
            "Rua das Flores, 123, Apto 42 - Centro, São Paulo/SP"
        );
    }
}
```

## Domain Services

```csharp
// GEOAPI.Domain.Tests/Services/GeometryValidatorTests.cs
public class GeometryValidatorTests
{
    [Fact]
    public void Validate_ValidPolygon_ShouldReturnTrue()
    {
        var polygon = TestGeometryFactory.CreateValidPolygon();
        var validator = new GeometryValidator();

        var result = validator.IsValid(polygon);

        result.Should().BeTrue();
    }

    [Fact]
    public void CalculateArea_ShouldReturnCorrectValue()
    {
        var polygon = TestGeometryFactory.CreateSquare(10); // 10m x 10m
        var calculator = new AreaCalculator();

        var area = calculator.Calculate(polygon);

        area.Should().BeApproximately(100, 0.01); // 100 m²
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
