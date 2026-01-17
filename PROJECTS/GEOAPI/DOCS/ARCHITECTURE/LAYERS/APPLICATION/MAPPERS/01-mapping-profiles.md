# Mapping Profiles

Configuração de mapeamento entre Domain Entities e DTOs.

## UnitMappingProfile

```csharp
public class UnitMappingProfile : Profile
{
    public UnitMappingProfile()
    {
        // Entity -> DTO
        CreateMap<Unit, UnitDto>()
            .ForMember(d => d.Geometry, opt => opt.MapFrom(s => ToGeoJson(s.Boundary)))
            .ForMember(d => d.Centroid, opt => opt.MapFrom(s => ToCentroid(s.Centroid)))
            .ForMember(d => d.Holders, opt => opt.MapFrom(s => s.UnitHolders.Select(uh => uh.Holder)));

        CreateMap<Unit, UnitSummaryDto>()
            .ForMember(d => d.FullAddress, opt => opt.MapFrom(s => s.Address.FullAddress))
            .ForMember(d => d.HoldersCount, opt => opt.MapFrom(s => s.UnitHolders.Count));

        // DTO -> Value Objects (para criar entidade)
        CreateMap<AddressDto, Address>();
        CreateMap<GeometryDto, Geometry>()
            .ConvertUsing<GeometryConverter>();
    }

    private static GeometryDto ToGeoJson(Geometry geometry)
    {
        return new GeometryDto(
            "Polygon",
            geometry.Coordinates.Select(c => new[] { c.X, c.Y }).ToArray()
        );
    }

    private static CentroidDto ToCentroid(Point point)
    {
        return new CentroidDto(point.Y, point.X);
    }
}
```

## HolderMappingProfile

```csharp
public class HolderMappingProfile : Profile
{
    public HolderMappingProfile()
    {
        CreateMap<Holder, HolderDto>()
            .ForMember(d => d.CpfMasked, opt => opt.MapFrom(s => s.Cpf.Masked))
            .ForMember(d => d.Age, opt => opt.MapFrom(s => CalculateAge(s.BirthDate)));

        CreateMap<Holder, HolderSummaryDto>();
    }

    private static int CalculateAge(DateTime birthDate)
    {
        var today = DateTime.Today;
        var age = today.Year - birthDate.Year;
        if (birthDate.Date > today.AddYears(-age)) age--;
        return age;
    }
}
```

## GeometryConverter

```csharp
public class GeometryConverter : ITypeConverter<GeometryDto, Geometry>
{
    private readonly GeometryFactory _factory;

    public Geometry Convert(GeometryDto source, Geometry destination, ResolutionContext context)
    {
        var coordinates = source.Coordinates[0]
            .Select(c => new Coordinate(c[0], c[1]))
            .ToArray();

        return _factory.CreatePolygon(coordinates);
    }
}
```

## Registro no DI

```csharp
// Program.cs
services.AddAutoMapper(typeof(UnitMappingProfile).Assembly);
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
