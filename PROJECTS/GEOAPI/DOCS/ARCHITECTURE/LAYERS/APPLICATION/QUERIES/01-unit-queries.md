# Unit Queries

Queries CQRS para operações de leitura de unidades.

## GetUnitByIdQuery

```csharp
public record GetUnitByIdQuery(
    Guid Id,
    bool IncludeHolders = false,
    bool IncludeCommunity = false
) : IRequest<Result<UnitDto?>>;

public class GetUnitByIdHandler : IRequestHandler<GetUnitByIdQuery, Result<UnitDto?>>
{
    public async Task<Result<UnitDto?>> Handle(GetUnitByIdQuery request, CancellationToken ct)
    {
        var query = _dbContext.Units
            .Where(u => u.Id == request.Id);

        if (request.IncludeHolders)
            query = query.Include(u => u.UnitHolders).ThenInclude(uh => uh.Holder);

        if (request.IncludeCommunity)
            query = query.Include(u => u.Community);

        var unit = await query.FirstOrDefaultAsync(ct);
        return unit == null
            ? Result.Success<UnitDto?>(null)
            : Result.Success(_mapper.Map<UnitDto>(unit));
    }
}
```

## ListUnitsQuery

```csharp
public record ListUnitsQuery(
    int Page = 1,
    int Limit = 20,
    string? Status = null,
    string? Neighborhood = null,
    Guid? CommunityId = null,
    BoundingBox? Bbox = null,
    string? Search = null,
    string Sort = "-created_at"
) : IRequest<PagedResult<UnitSummaryDto>>;
```

## GetUnitsGeoJsonQuery

```csharp
public record GetUnitsGeoJsonQuery(
    Guid? CommunityId = null,
    string? Status = null
) : IRequest<GeoJsonFeatureCollection>;

// Retorna FeatureCollection para renderização em mapa
// Simplifica geometrias para viewport atual
```

## GetUnitStatisticsQuery

```csharp
public record GetUnitStatisticsQuery(
    Guid? CommunityId = null
) : IRequest<UnitStatisticsDto>;

// Retorna agregações: total, por status, área total, etc.
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
