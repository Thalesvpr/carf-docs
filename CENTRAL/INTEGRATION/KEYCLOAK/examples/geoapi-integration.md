# GEOAPI + Keycloak (.NET)

## Install
```bash
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

## Config (appsettings.json)
```json
{
  "Jwt": {
    "Authority": "http://localhost:8080/realms/carf",
    "Audience": "geoapi"
  }
}
```

## Program.cs
```csharp
builder.Services
  .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
  .AddJwtBearer(options => {
    options.Authority = config["Jwt:Authority"];
    options.Audience = config["Jwt:Audience"];
    options.TokenValidationParameters = new() {
      RoleClaimType = "roles",
      NameClaimType = "preferred_username"
    };
  });

builder.Services.AddAuthorization(options => {
  options.AddPolicy("Analyst", policy => policy.RequireRole("analyst", "admin"));
  options.AddPolicy("Admin", policy => policy.RequireRole("admin", "super_admin"));
});

app.UseAuthentication();
app.UseAuthorization();
```

## Controller
```csharp
[ApiController]
[Route("api/[controller]")]
[Authorize]
public class UnitsController : ControllerBase {

  [HttpGet]
  [Authorize(Roles = "analyst,admin")]
  public async Task<IActionResult> GetAll() {
    var tenantId = User.FindFirst("tenant_id")?.Value;
    var userId = User.FindFirst("sub")?.Value;

    return Ok(await _service.GetUnits(tenantId));
  }

  [HttpPost]
  [Authorize(Policy = "Analyst")]
  public async Task<IActionResult> Create(CreateUnitDto dto) {
    dto.TenantId = User.FindFirst("tenant_id")?.Value;
    return Ok(await _service.Create(dto));
  }
}
```

## Tenant Middleware
```csharp
app.Use(async (context, next) => {
  var tenantId = context.User.FindFirst("tenant_id")?.Value;
  if (tenantId != null) {
    context.Items["TenantId"] = tenantId;
  }
  await next();
});
```

## Current User Service
```csharp
public class CurrentUserService : ICurrentUserService {
  private readonly IHttpContextAccessor _http;

  public string? UserId => _http.HttpContext?.User.FindFirst("sub")?.Value;
  public string? TenantId => _http.HttpContext?.User.FindFirst("tenant_id")?.Value;
  public List<string> Roles => _http.HttpContext?.User.FindAll("roles").Select(c => c.Value).ToList();
}
```

Done. ✅
