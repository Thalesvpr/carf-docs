# Units Controller

Controller REST para operações de unidades habitacionais.

## UnitsController

```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class UnitsController : ControllerBase
{
    private readonly IMediator _mediator;

    [HttpPost]
    [ProducesResponseType(typeof(UnitDto), StatusCodes.Status201Created)]
    [ProducesResponseType(typeof(ProblemDetails), StatusCodes.Status400BadRequest)]
    public async Task<IActionResult> Create([FromBody] CreateUnitRequest request, CancellationToken ct)
    {
        var command = new CreateUnitCommand(request.Address, request.Geometry, request.CommunityId, request.Photos);
        var result = await _mediator.Send(command, ct);

        return result.IsSuccess
            ? CreatedAtAction(nameof(GetById), new { id = result.Value.Id }, result.Value)
            : BadRequest(result.ToProblemDetails());
    }

    [HttpGet("{id:guid}")]
    [ProducesResponseType(typeof(UnitDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status404NotFound)]
    public async Task<IActionResult> GetById(
        Guid id,
        [FromQuery] bool includeHolders = false,
        [FromQuery] bool includeCommunity = false,
        CancellationToken ct = default)
    {
        var query = new GetUnitByIdQuery(id, includeHolders, includeCommunity);
        var result = await _mediator.Send(query, ct);

        return result.Value != null
            ? Ok(result.Value)
            : NotFound();
    }

    [HttpGet]
    [ProducesResponseType(typeof(PagedResult<UnitSummaryDto>), StatusCodes.Status200OK)]
    public async Task<IActionResult> List([FromQuery] ListUnitsQueryParams queryParams, CancellationToken ct)
    {
        var query = queryParams.ToQuery();
        var result = await _mediator.Send(query, ct);
        return Ok(result);
    }

    [HttpPatch("{id:guid}")]
    [ProducesResponseType(typeof(UnitDto), StatusCodes.Status200OK)]
    [ProducesResponseType(StatusCodes.Status403Forbidden)]
    public async Task<IActionResult> Update(Guid id, [FromBody] UpdateUnitRequest request, CancellationToken ct)
    {
        var command = new UpdateUnitCommand(id, request.Address, request.Geometry);
        var result = await _mediator.Send(command, ct);

        return result.IsSuccess
            ? Ok(result.Value)
            : result.Error.Code == "UNIT_LOCKED"
                ? Forbid()
                : BadRequest(result.ToProblemDetails());
    }

    [HttpPost("{id:guid}/submit")]
    [ProducesResponseType(StatusCodes.Status200OK)]
    public async Task<IActionResult> Submit(Guid id, CancellationToken ct)
    {
        var command = new SubmitUnitCommand(id);
        var result = await _mediator.Send(command, ct);

        return result.IsSuccess ? Ok() : BadRequest(result.ToProblemDetails());
    }

    [HttpDelete("{id:guid}")]
    [ProducesResponseType(StatusCodes.Status204NoContent)]
    public async Task<IActionResult> Delete(Guid id, CancellationToken ct)
    {
        var command = new DeleteUnitCommand(id);
        var result = await _mediator.Send(command, ct);

        return result.IsSuccess ? NoContent() : BadRequest(result.ToProblemDetails());
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
