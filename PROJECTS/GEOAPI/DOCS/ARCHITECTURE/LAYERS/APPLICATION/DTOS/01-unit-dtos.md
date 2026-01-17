# Unit DTOs

Data Transfer Objects para unidades habitacionais.

## UnitDto (Response completo)

```csharp
public record UnitDto(
    Guid Id,
    string Code,
    string Status,
    AddressDto Address,
    GeometryDto Geometry,
    decimal AreaM2,
    CentroidDto Centroid,
    List<PhotoDto>? Photos,
    List<HolderSummaryDto>? Holders,
    CommunitySummaryDto? Community,
    Guid TenantId,
    DateTime CreatedAt,
    DateTime UpdatedAt
);
```

## UnitSummaryDto (Listagem)

```csharp
public record UnitSummaryDto(
    Guid Id,
    string Code,
    string Status,
    string FullAddress,
    decimal AreaM2,
    CentroidDto Centroid,
    int HoldersCount,
    DateTime CreatedAt
);
```

## CreateUnitRequest

```csharp
public record CreateUnitRequest(
    AddressDto Address,
    GeometryDto Geometry,
    Guid? CommunityId,
    List<CreatePhotoRequest>? Photos,
    Dictionary<string, object>? Metadata
);
```

## UpdateUnitRequest

```csharp
public record UpdateUnitRequest(
    AddressDto? Address,
    GeometryDto? Geometry,
    List<CreatePhotoRequest>? Photos
);
```

## AddressDto

```csharp
public record AddressDto(
    string Street,
    string Number,
    string? Complement,
    string Neighborhood,
    string City,
    string State,
    string ZipCode
)
{
    public string FullAddress =>
        string.IsNullOrEmpty(Complement)
            ? $"{Street}, {Number} - {Neighborhood}, {City}/{State}"
            : $"{Street}, {Number}, {Complement} - {Neighborhood}, {City}/{State}";
}
```

## GeometryDto

```csharp
public record GeometryDto(
    string Type,
    double[][][] Coordinates
);

// Mapeado de/para GeoJSON Polygon
```

## CentroidDto

```csharp
public record CentroidDto(
    double Latitude,
    double Longitude
);
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
