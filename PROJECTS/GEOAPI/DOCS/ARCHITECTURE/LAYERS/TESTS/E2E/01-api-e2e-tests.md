# API E2E Tests

Testes end-to-end da API GEOAPI usando TestContainers.

## Setup

```csharp
public class ApiFixture : IAsyncLifetime
{
    private PostgreSqlContainer _postgres;
    private RedisContainer _redis;
    public HttpClient Client { get; private set; }

    public async Task InitializeAsync()
    {
        _postgres = new PostgreSqlBuilder()
            .WithImage("postgis/postgis:16-3.4")
            .Build();
        await _postgres.StartAsync();

        _redis = new RedisBuilder().Build();
        await _redis.StartAsync();

        var factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.ConfigureServices(services =>
                {
                    services.RemoveAll<DbContextOptions<CARFDbContext>>();
                    services.AddDbContext<CARFDbContext>(options =>
                        options.UseNpgsql(_postgres.GetConnectionString()));
                });
            });

        Client = factory.CreateClient();
    }

    public async Task DisposeAsync()
    {
        await _postgres.DisposeAsync();
        await _redis.DisposeAsync();
    }
}
```

## Testes de Units

```csharp
[Collection("API")]
public class UnitsE2ETests : IClassFixture<ApiFixture>
{
    private readonly HttpClient _client;

    [Fact]
    public async Task CreateUnit_WithValidData_Returns201()
    {
        // Arrange
        await AuthenticateAsAsync("cadastrista");
        var request = TestDataFactory.CreateUnitRequest();

        // Act
        var response = await _client.PostAsJsonAsync("/api/units", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Created);
        var unit = await response.Content.ReadFromJsonAsync<UnitDto>();
        unit.Should().NotBeNull();
        unit!.Code.Should().StartWith("UNI-");
    }

    [Fact]
    public async Task CreateUnit_WithOverlappingGeometry_Returns409()
    {
        // Arrange
        await AuthenticateAsAsync("cadastrista");
        var existingUnit = await CreateUnitAsync();
        var request = TestDataFactory.CreateUnitRequest(overlapping: existingUnit.Geometry);

        // Act
        var response = await _client.PostAsJsonAsync("/api/units", request);

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.Conflict);
    }

    [Fact]
    public async Task ListUnits_WithPagination_ReturnsCorrectPage()
    {
        // Arrange
        await AuthenticateAsAsync("cadastrista");
        await CreateUnitsAsync(50);

        // Act
        var response = await _client.GetAsync("/api/units?page=2&limit=20");

        // Assert
        response.StatusCode.Should().Be(HttpStatusCode.OK);
        var result = await response.Content.ReadFromJsonAsync<PagedResult<UnitSummaryDto>>();
        result!.Data.Should().HaveCount(20);
        result.Pagination.Page.Should().Be(2);
    }
}
```

## Helper Methods

```csharp
private async Task AuthenticateAsAsync(string role)
{
    var token = JwtTestHelper.GenerateToken(tenantId: TestTenantId, roles: new[] { role });
    _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
}

private async Task<UnitDto> CreateUnitAsync()
{
    var request = TestDataFactory.CreateUnitRequest();
    var response = await _client.PostAsJsonAsync("/api/units", request);
    return await response.Content.ReadFromJsonAsync<UnitDto>();
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
