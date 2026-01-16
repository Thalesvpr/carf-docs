# Repository Integration Tests

Testes de integração para repositories com banco de dados real.

## Setup

```csharp
public class DatabaseFixture : IAsyncLifetime
{
    private PostgreSqlContainer _container;
    public CARFDbContext DbContext { get; private set; }

    public async Task InitializeAsync()
    {
        _container = new PostgreSqlBuilder()
            .WithImage("postgis/postgis:16-3.4")
            .Build();

        await _container.StartAsync();

        var options = new DbContextOptionsBuilder<CARFDbContext>()
            .UseNpgsql(_container.GetConnectionString(), npgsql =>
                npgsql.UseNetTopologySuite())
            .Options;

        DbContext = new CARFDbContext(options, new TestTenantContext());
        await DbContext.Database.MigrateAsync();
    }

    public async Task DisposeAsync()
    {
        await DbContext.DisposeAsync();
        await _container.DisposeAsync();
    }
}
```

## UnitRepository Tests

```csharp
[Collection("Database")]
public class UnitRepositoryTests : IClassFixture<DatabaseFixture>
{
    private readonly CARFDbContext _dbContext;
    private readonly UnitRepository _repository;

    [Fact]
    public async Task AddAsync_PersistsUnit()
    {
        // Arrange
        var unit = TestUnitFactory.CreateUnit();

        // Act
        await _repository.AddAsync(unit, CancellationToken.None);
        await _dbContext.SaveChangesAsync();

        // Assert
        var persisted = await _dbContext.Units.FindAsync(unit.Id);
        persisted.Should().NotBeNull();
        persisted!.Code.Should().Be(unit.Code);
    }

    [Fact]
    public async Task HasOverlap_WithOverlappingGeometry_ReturnsTrue()
    {
        // Arrange
        var existingUnit = TestUnitFactory.CreateUnit(geometry: TestGeometry.Square(-46.6, -23.5, 100));
        await _repository.AddAsync(existingUnit, CancellationToken.None);
        await _dbContext.SaveChangesAsync();

        var overlappingGeometry = TestGeometry.Square(-46.6, -23.5, 50); // Sobrepõe

        // Act
        var hasOverlap = await _repository.HasOverlapAsync(overlappingGeometry, CancellationToken.None);

        // Assert
        hasOverlap.Should().BeTrue();
    }

    [Fact]
    public async Task GetByIdAsync_WithRLS_ReturnsOnlyTenantData()
    {
        // Arrange
        var unit1 = TestUnitFactory.CreateUnit(tenantId: TenantA);
        var unit2 = TestUnitFactory.CreateUnit(tenantId: TenantB);
        await _repository.AddAsync(unit1, CancellationToken.None);
        await _repository.AddAsync(unit2, CancellationToken.None);
        await _dbContext.SaveChangesAsync();

        // Contexto está configurado para TenantA
        // Act
        var result = await _repository.GetByIdAsync(unit2.Id, CancellationToken.None);

        // Assert
        result.Should().BeNull(); // RLS impede acesso
    }

    [Fact]
    public async Task ListAsync_WithBoundingBox_ReturnsOnlyContainedUnits()
    {
        // Arrange
        var insideUnit = TestUnitFactory.CreateUnit(centroid: Point(-46.6, -23.5));
        var outsideUnit = TestUnitFactory.CreateUnit(centroid: Point(-47.0, -24.0));
        await _repository.AddAsync(insideUnit, CancellationToken.None);
        await _repository.AddAsync(outsideUnit, CancellationToken.None);
        await _dbContext.SaveChangesAsync();

        var bbox = new BoundingBox(-46.7, -23.6, -46.5, -23.4);

        // Act
        var result = await _repository.ListAsync(bbox: bbox, ct: CancellationToken.None);

        // Assert
        result.Should().ContainSingle();
        result.First().Id.Should().Be(insideUnit.Id);
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
