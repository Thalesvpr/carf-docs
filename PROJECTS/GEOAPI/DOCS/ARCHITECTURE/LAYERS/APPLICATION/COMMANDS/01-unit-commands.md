# Unit Commands

Commands CQRS para operações de escrita em unidades habitacionais.

## CreateUnitCommand

```csharp
public record CreateUnitCommand(
    AddressDto Address,
    GeometryDto Geometry,
    Guid? CommunityId,
    List<PhotoDto>? Photos
) : IRequest<Result<UnitDto>>;

public class CreateUnitHandler : IRequestHandler<CreateUnitCommand, Result<UnitDto>>
{
    public async Task<Result<UnitDto>> Handle(CreateUnitCommand request, CancellationToken ct)
    {
        // 1. Validar geometria
        if (!_geometryValidator.IsValid(request.Geometry))
            return Result.Failure<UnitDto>("Geometria inválida");

        // 2. Verificar sobreposição
        if (await _unitRepository.HasOverlap(request.Geometry, ct))
            return Result.Failure<UnitDto>("Sobreposição com unidade existente");

        // 3. Criar entidade
        var unit = Unit.Create(
            Address.FromDto(request.Address),
            Geometry.FromDto(request.Geometry),
            _tenantContext.TenantId
        );

        // 4. Persistir
        await _unitRepository.AddAsync(unit, ct);
        await _unitOfWork.CommitAsync(ct);

        return Result.Success(_mapper.Map<UnitDto>(unit));
    }
}
```

## UpdateUnitCommand

```csharp
public record UpdateUnitCommand(
    Guid Id,
    AddressDto? Address,
    GeometryDto? Geometry
) : IRequest<Result<UnitDto>>;
```

## SubmitUnitCommand

```csharp
public record SubmitUnitCommand(Guid UnitId) : IRequest<Result>;

// Transiciona status de Rascunho para Pendente
// Valida que unidade tem pelo menos um titular
```

## ApproveUnitCommand

```csharp
public record ApproveUnitCommand(
    Guid UnitId,
    string? Comments
) : IRequest<Result>;

// Requer role 'aprovador'
// Transiciona status de Pendente para Aprovado
```

## DeleteUnitCommand

```csharp
public record DeleteUnitCommand(Guid UnitId) : IRequest<Result>;

// Soft delete apenas em status Rascunho
// Unidades aprovadas não podem ser deletadas
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
