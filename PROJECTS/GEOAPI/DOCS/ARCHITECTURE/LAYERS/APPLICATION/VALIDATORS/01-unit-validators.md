# Unit Validators

Validadores FluentValidation para commands e DTOs de unidades.

## CreateUnitRequestValidator

```csharp
public class CreateUnitRequestValidator : AbstractValidator<CreateUnitRequest>
{
    public CreateUnitRequestValidator()
    {
        RuleFor(x => x.Address)
            .NotNull()
            .SetValidator(new AddressValidator());

        RuleFor(x => x.Geometry)
            .NotNull()
            .SetValidator(new GeometryValidator());

        RuleFor(x => x.Photos)
            .ForEach(p => p.SetValidator(new PhotoValidator()))
            .When(x => x.Photos != null);
    }
}
```

## AddressValidator

```csharp
public class AddressValidator : AbstractValidator<AddressDto>
{
    public AddressValidator()
    {
        RuleFor(x => x.Street)
            .NotEmpty().WithMessage("Rua é obrigatória")
            .MaximumLength(200);

        RuleFor(x => x.Number)
            .NotEmpty().WithMessage("Número é obrigatório")
            .MaximumLength(20);

        RuleFor(x => x.Neighborhood)
            .NotEmpty().WithMessage("Bairro é obrigatório")
            .MaximumLength(100);

        RuleFor(x => x.City)
            .NotEmpty().WithMessage("Cidade é obrigatória")
            .MaximumLength(100);

        RuleFor(x => x.State)
            .NotEmpty()
            .Matches("^[A-Z]{2}$").WithMessage("Estado deve ter 2 letras maiúsculas");

        RuleFor(x => x.ZipCode)
            .NotEmpty()
            .Matches(@"^\d{5}-?\d{3}$").WithMessage("CEP inválido");
    }
}
```

## GeometryValidator

```csharp
public class GeometryValidator : AbstractValidator<GeometryDto>
{
    public GeometryValidator()
    {
        RuleFor(x => x.Type)
            .Equal("Polygon").WithMessage("Tipo deve ser Polygon");

        RuleFor(x => x.Coordinates)
            .NotEmpty().WithMessage("Coordenadas são obrigatórias")
            .Must(BeValidPolygon).WithMessage("Polígono inválido")
            .Must(NotBeSelfIntersecting).WithMessage("Polígono não pode ter auto-intersecção");
    }

    private bool BeValidPolygon(double[][][] coords)
    {
        if (coords == null || coords.Length == 0) return false;
        var ring = coords[0];
        return ring.Length >= 4 && ring[0].SequenceEqual(ring[^1]);
    }

    private bool NotBeSelfIntersecting(double[][][] coords)
    {
        var polygon = GeometryFactory.CreatePolygon(coords);
        return polygon.IsValid;
    }
}
```

## UpdateUnitRequestValidator

```csharp
public class UpdateUnitRequestValidator : AbstractValidator<UpdateUnitRequest>
{
    public UpdateUnitRequestValidator()
    {
        RuleFor(x => x.Address)
            .SetValidator(new AddressValidator())
            .When(x => x.Address != null);

        RuleFor(x => x.Geometry)
            .SetValidator(new GeometryValidator())
            .When(x => x.Geometry != null);
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
