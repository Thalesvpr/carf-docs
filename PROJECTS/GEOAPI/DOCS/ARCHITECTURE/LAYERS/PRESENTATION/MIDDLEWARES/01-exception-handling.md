# Exception Handling Middleware

Middleware para tratamento global de exceções.

## ExceptionHandlingMiddleware

```csharp
public class ExceptionHandlingMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (Exception ex)
        {
            await HandleExceptionAsync(context, ex);
        }
    }

    private async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        var correlationId = context.TraceIdentifier;

        var (statusCode, problemDetails) = exception switch
        {
            ValidationException ve => (
                StatusCodes.Status400BadRequest,
                CreateProblemDetails("Validation Error", ve.Message, ve.Errors)),

            DomainException de => (
                StatusCodes.Status400BadRequest,
                CreateProblemDetails("Domain Error", de.Message)),

            NotFoundException nf => (
                StatusCodes.Status404NotFound,
                CreateProblemDetails("Not Found", nf.Message)),

            UnauthorizedException => (
                StatusCodes.Status401Unauthorized,
                CreateProblemDetails("Unauthorized", "Authentication required")),

            ForbiddenException fe => (
                StatusCodes.Status403Forbidden,
                CreateProblemDetails("Forbidden", fe.Message)),

            ConflictException ce => (
                StatusCodes.Status409Conflict,
                CreateProblemDetails("Conflict", ce.Message)),

            _ => (
                StatusCodes.Status500InternalServerError,
                CreateProblemDetails("Internal Server Error", "An unexpected error occurred"))
        };

        // Log
        if (statusCode >= 500)
            _logger.LogError(exception, "Unhandled exception. CorrelationId: {CorrelationId}", correlationId);
        else
            _logger.LogWarning("Handled exception: {Message}. CorrelationId: {CorrelationId}",
                exception.Message, correlationId);

        // Response
        problemDetails.Extensions["correlationId"] = correlationId;
        context.Response.StatusCode = statusCode;
        context.Response.ContentType = "application/problem+json";
        await context.Response.WriteAsJsonAsync(problemDetails);
    }

    private static ProblemDetails CreateProblemDetails(string title, string detail, object? errors = null)
    {
        var problemDetails = new ProblemDetails
        {
            Title = title,
            Detail = detail,
            Status = null // Set by response
        };

        if (errors != null)
            problemDetails.Extensions["errors"] = errors;

        return problemDetails;
    }
}
```

## Registro

```csharp
// Program.cs
app.UseMiddleware<ExceptionHandlingMiddleware>();
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
