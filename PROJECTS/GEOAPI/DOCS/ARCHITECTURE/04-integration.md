# Integrações Externas - GEOAPI

Este documento detalha todas as integrações externas do GEOAPI, incluindo autenticação, banco de dados, consumidores da API e serviços externos.

## 📋 Índice

- [1. Visão Geral das Integrações](#1-visão-geral-das-integrações)
- [2. Integração com Keycloak](#2-integração-com-keycloak)
- [3. Integração com PostgreSQL + PostGIS](#3-integração-com-postgresql--postgis)
- [4. Consumidores da API](#4-consumidores-da-api)
- [5. Serviços Externos](#5-serviços-externos)
- [6. Resiliência e Error Handling](#6-resiliência-e-error-handling)
- [7. Monitoramento de Integrações](#7-monitoramento-de-integrações)

---

## 1. Visão Geral das Integrações

### 1.1 Diagrama de Contexto

```
┌─────────────────────────────────────────────────────────────────┐
│                        EXTERNAL SYSTEMS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │ Keycloak │    │PostgreSQL│    │  Email   │    │   SMS    │  │
│  │  OAuth2  │    │ + PostGIS│    │  Server  │    │ Gateway  │  │
│  └─────┬────┘    └─────┬────┘    └─────┬────┘    └─────┬────┘  │
│        │               │               │               │        │
│        │ JWT           │ SQL/PostGIS   │ SMTP          │ HTTP   │
│        │               │               │               │        │
└────────┼───────────────┼───────────────┼───────────────┼────────┘
         │               │               │               │
         ▼               ▼               ▼               ▼
    ┌────────────────────────────────────────────────────────┐
    │                     GEOAPI                              │
    │  ┌──────────────────────────────────────────────────┐  │
    │  │         Infrastructure Layer                      │  │
    │  │  • KeycloakClient                                 │  │
    │  │  • DbContext (EF Core)                            │  │
    │  │  • EmailService                                   │  │
    │  │  • SmsService                                     │  │
    │  └──────────────────────────────────────────────────┘  │
    └───┬────────────────────────────────────────────────┬───┘
        │                                                │
        │ REST API (JSON)                                │ REST API (JSON)
        │                                                │
        ▼                                                ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   GEOWEB    │  │  REURBCAD   │  │   ADMIN     │  │   GEOGIS    │
│   (React)   │  │(React Native│  │   (React)   │  │   (React)   │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

### 1.2 Tipos de Integrações

| Tipo | Sistema | Protocolo | Autenticação | Criticidade |
|------|---------|-----------|--------------|-------------|
| **Autenticação** | Keycloak | HTTP/OAuth2 | Client Credentials | ⚠️ Crítica |
| **Database** | PostgreSQL | TCP/SQL | User/Password | ⚠️ Crítica |
| **API Consumers** | GEOWEB, REURBCAD, etc | HTTP/REST | JWT Bearer | 🔵 Alta |
| **Email** | SMTP Server | SMTP | User/Password | 🟡 Média |
| **SMS** | SMS Gateway | HTTP/REST | API Key | 🟡 Média |
| **Storage** | File System / S3 | File/HTTP | Filesystem/IAM | 🔵 Alta |
| **Logs** | Elasticsearch | HTTP | Basic Auth | 🟢 Baixa |

---

## 2. Integração com Keycloak

### 2.1 Visão Geral

O Keycloak é o Identity Provider (IdP) responsável por:
- **Autenticação de usuários** (login/logout)
- **Emissão de tokens JWT** (access tokens e refresh tokens)
- **Autorização baseada em roles** (RBAC - Role-Based Access Control)
- **Gestão de usuários e grupos**
- **SSO (Single Sign-On)** entre aplicações

### 2.2 Fluxo de Autenticação OAuth2/OIDC

```
┌─────────┐                                           ┌──────────┐
│ GEOWEB  │                                           │ Keycloak │
│(Frontend│                                           │  Server  │
└────┬────┘                                           └─────┬────┘
     │                                                      │
     │ 1. Redirect to /auth/realms/carf/protocol/openid-connect/auth
     │    ?client_id=geoweb&redirect_uri=...&response_type=code
     │─────────────────────────────────────────────────────>│
     │                                                      │
     │                    2. Login Page                     │
     │<─────────────────────────────────────────────────────│
     │                                                      │
     │ 3. User enters credentials (username/password)       │
     │─────────────────────────────────────────────────────>│
     │                                                      │
     │              4. Authorization Code                   │
     │<─────────────────────────────────────────────────────│
     │   Redirect: https://geoweb.carf.gov.br?code=ABC123   │
     │                                                      │
     │ 5. POST /auth/realms/carf/protocol/openid-connect/token
     │    code=ABC123&grant_type=authorization_code         │
     │─────────────────────────────────────────────────────>│
     │                                                      │
     │          6. Access Token + Refresh Token             │
     │<─────────────────────────────────────────────────────│
     │   { access_token: "eyJ...", refresh_token: "...",    │
     │     expires_in: 300, token_type: "Bearer" }          │
     │                                                      │
     ▼                                                      ▼

┌─────────┐                                           ┌──────────┐
│ GEOWEB  │                                           │  GEOAPI  │
└────┬────┘                                           └─────┬────┘
     │                                                      │
     │ 7. GET /api/v1/units                                 │
     │    Authorization: Bearer eyJ...                      │
     │─────────────────────────────────────────────────────>│
     │                                                      │
     │              8. Validate JWT Token                   │
     │              (signature, expiration, roles)          │
     │                                                      │
     │          9. Response with data                       │
     │<─────────────────────────────────────────────────────│
     │   { data: [...], meta: {...} }                       │
     │                                                      │
```

### 2.3 Configuração do Keycloak Client

**Realm:** `carf`
**Clients configurados:**

| Client ID | Type | Access Type | Valid Redirect URIs | Roles |
|-----------|------|-------------|---------------------|-------|
| `geoweb` | Public | public | `https://geoweb.carf.gov.br/*` | realm-management |
| `reurbcad` | Public | public | `carf://callback` (Deep Link) | realm-management |
| `admin` | Public | public | `https://admin.carf.gov.br/*` | realm-management |
| `geoapi` | Confidential | confidential | N/A (backend) | realm-management |

### 2.4 Configuração no GEOAPI (appsettings.json)

```json
{
  "Keycloak": {
    "Authority": "https://auth.carf.gov.br/auth/realms/carf",
    "Audience": "geoapi",
    "MetadataAddress": "https://auth.carf.gov.br/auth/realms/carf/.well-known/openid-configuration",
    "RequireHttpsMetadata": true,
    "ValidateAudience": true,
    "ValidateIssuer": true,
    "ValidateLifetime": true,
    "ClockSkew": 300,
    "RoleClaimType": "realm_access.roles"
  }
}
```

### 2.5 Código de Integração (Startup.cs)

```csharp
// GEOAPI/src/Infrastructure/DependencyInjection/AuthenticationExtensions.cs

using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;

namespace GEOAPI.Infrastructure.DependencyInjection;

public static class AuthenticationExtensions
{
    public static IServiceCollection AddKeycloakAuthentication(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var keycloakConfig = configuration.GetSection("Keycloak");

        services.AddAuthentication(options =>
        {
            options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
            options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
        })
        .AddJwtBearer(options =>
        {
            options.Authority = keycloakConfig["Authority"];
            options.Audience = keycloakConfig["Audience"];
            options.MetadataAddress = keycloakConfig["MetadataAddress"];
            options.RequireHttpsMetadata = bool.Parse(keycloakConfig["RequireHttpsMetadata"] ?? "true");

            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateAudience = bool.Parse(keycloakConfig["ValidateAudience"] ?? "true"),
                ValidAudience = keycloakConfig["Audience"],
                ValidateIssuer = bool.Parse(keycloakConfig["ValidateIssuer"] ?? "true"),
                ValidIssuer = keycloakConfig["Authority"],
                ValidateLifetime = bool.Parse(keycloakConfig["ValidateLifetime"] ?? "true"),
                ClockSkew = TimeSpan.FromSeconds(int.Parse(keycloakConfig["ClockSkew"] ?? "300")),
                RoleClaimType = keycloakConfig["RoleClaimType"]
            };

            options.Events = new JwtBearerEvents
            {
                OnAuthenticationFailed = context =>
                {
                    var logger = context.HttpContext.RequestServices
                        .GetRequiredService<ILogger<Program>>();

                    logger.LogError(context.Exception,
                        "JWT authentication failed: {Message}",
                        context.Exception.Message);

                    return Task.CompletedTask;
                },

                OnTokenValidated = context =>
                {
                    var logger = context.HttpContext.RequestServices
                        .GetRequiredService<ILogger<Program>>();

                    var userId = context.Principal?.FindFirst("sub")?.Value;
                    logger.LogInformation("JWT validated for user: {UserId}", userId);

                    return Task.CompletedTask;
                },

                OnChallenge = context =>
                {
                    var logger = context.HttpContext.RequestServices
                        .GetRequiredService<ILogger<Program>>();

                    logger.LogWarning("JWT challenge triggered: {Error} - {ErrorDescription}",
                        context.Error, context.ErrorDescription);

                    return Task.CompletedTask;
                }
            };
        });

        return services;
    }
}
```

### 2.6 Estrutura do JWT Token

**Header:**
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "FJ86GcF3jTbNLOco4NvZkUCIUmfYCqoqtOQeMfbhNlE"
}
```

**Payload:**
```json
{
  "exp": 1736461200,
  "iat": 1736460900,
  "jti": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "iss": "https://auth.carf.gov.br/auth/realms/carf",
  "aud": "geoapi",
  "sub": "f:12345678-1234-1234-1234-123456789012:joao.silva",
  "typ": "Bearer",
  "azp": "geoweb",
  "session_state": "abc123-session-xyz",
  "realm_access": {
    "roles": ["ADMIN", "ANALYST"]
  },
  "scope": "openid profile email",
  "email_verified": true,
  "name": "João Silva",
  "preferred_username": "joao.silva",
  "given_name": "João",
  "family_name": "Silva",
  "email": "joao.silva@example.com",
  "municipality_id": "3550308"
}
```

**Claims importantes:**
- `sub`: Subject (user ID único)
- `realm_access.roles`: Array de roles do usuário
- `municipality_id`: ID do município (custom claim para multi-tenancy)
- `exp`: Expiration time (300 segundos = 5 minutos)
- `iat`: Issued at time

### 2.7 Autorização por Roles

```csharp
// GEOAPI/src/Gateway/Controllers/UnitsController.cs

using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace GEOAPI.Gateway.Controllers;

[ApiController]
[Route("api/v1/[controller]")]
[Authorize] // Requer autenticação JWT
public class UnitsController : ControllerBase
{
    // Qualquer usuário autenticado pode listar units do seu município
    [HttpGet]
    [Authorize(Roles = "PUBLIC,MUNICIPALITY_MANAGER,FIELD_AGENT,ANALYST,ADMIN")]
    public async Task<ActionResult<PagedResult<UnitDto>>> GetUnits(
        [FromQuery] GetUnitsQuery query)
    {
        var result = await _mediator.Send(query);
        return Ok(result);
    }

    // Apenas ADMIN e ANALYST podem criar units
    [HttpPost]
    [Authorize(Roles = "ADMIN,ANALYST")]
    public async Task<ActionResult<UnitDto>> CreateUnit(
        [FromBody] CreateUnitCommand command)
    {
        var result = await _mediator.Send(command);
        return CreatedAtAction(nameof(GetUnit), new { id = result.Id }, result);
    }

    // Apenas ADMIN pode deletar units
    [HttpDelete("{id}")]
    [Authorize(Roles = "ADMIN")]
    public async Task<ActionResult> DeleteUnit(Guid id)
    {
        await _mediator.Send(new DeleteUnitCommand { Id = id });
        return NoContent();
    }
}
```

### 2.8 Custom Authorization Policies

```csharp
// GEOAPI/src/Infrastructure/DependencyInjection/AuthorizationExtensions.cs

using Microsoft.AspNetCore.Authorization;

namespace GEOAPI.Infrastructure.DependencyInjection;

public static class AuthorizationExtensions
{
    public static IServiceCollection AddCustomAuthorization(
        this IServiceCollection services)
    {
        services.AddAuthorization(options =>
        {
            // Policy para operações de leitura
            options.AddPolicy("CanRead", policy =>
                policy.RequireRole("PUBLIC", "MUNICIPALITY_MANAGER", "FIELD_AGENT", "ANALYST", "ADMIN"));

            // Policy para operações de escrita
            options.AddPolicy("CanWrite", policy =>
                policy.RequireRole("FIELD_AGENT", "ANALYST", "ADMIN"));

            // Policy para operações administrativas
            options.AddPolicy("CanAdmin", policy =>
                policy.RequireRole("ADMIN"));

            // Policy personalizada: usuário deve pertencer ao mesmo município
            options.AddPolicy("SameMunicipality", policy =>
                policy.Requirements.Add(new SameMunicipalityRequirement()));
        });

        // Registrar handler para custom requirement
        services.AddScoped<IAuthorizationHandler, SameMunicipalityHandler>();

        return services;
    }
}

// Custom Authorization Requirement
public class SameMunicipalityRequirement : IAuthorizationRequirement { }

// Custom Authorization Handler
public class SameMunicipalityHandler : AuthorizationHandler<SameMunicipalityRequirement>
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public SameMunicipalityHandler(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    protected override Task HandleRequirementAsync(
        AuthorizationHandlerContext context,
        SameMunicipalityRequirement requirement)
    {
        // Extrair municipality_id do JWT
        var userMunicipalityId = context.User
            .FindFirst("municipality_id")?.Value;

        if (string.IsNullOrEmpty(userMunicipalityId))
        {
            context.Fail();
            return Task.CompletedTask;
        }

        // Extrair municipality_id da rota ou body
        var httpContext = _httpContextAccessor.HttpContext;
        var requestedMunicipalityId = httpContext?.Request.RouteValues["municipalityId"]?.ToString()
            ?? httpContext?.Request.Query["municipalityId"].ToString();

        // Admins podem acessar qualquer município
        if (context.User.IsInRole("ADMIN"))
        {
            context.Succeed(requirement);
            return Task.CompletedTask;
        }

        // Verificar se o município solicitado é o mesmo do usuário
        if (userMunicipalityId == requestedMunicipalityId)
        {
            context.Succeed(requirement);
        }
        else
        {
            context.Fail();
        }

        return Task.CompletedTask;
    }
}
```

### 2.9 Keycloak Admin Client (Gestão de Usuários)

```csharp
// GEOAPI/src/Infrastructure/ExternalServices/KeycloakAdminClient.cs

using Keycloak.Net;
using Keycloak.Net.Models.Users;

namespace GEOAPI.Infrastructure.ExternalServices;

public interface IKeycloakAdminClient
{
    Task<string> CreateUserAsync(CreateUserRequest request);
    Task UpdateUserAsync(string userId, UpdateUserRequest request);
    Task DeleteUserAsync(string userId);
    Task AssignRoleAsync(string userId, string roleName);
    Task<User> GetUserByIdAsync(string userId);
}

public class KeycloakAdminClient : IKeycloakAdminClient
{
    private readonly KeycloakClient _client;
    private readonly string _realm;
    private readonly ILogger<KeycloakAdminClient> _logger;

    public KeycloakAdminClient(
        IConfiguration configuration,
        ILogger<KeycloakAdminClient> logger)
    {
        _logger = logger;
        _realm = configuration["Keycloak:Realm"] ?? "carf";

        var adminUrl = configuration["Keycloak:AdminUrl"]
            ?? "https://auth.carf.gov.br/auth";
        var adminUsername = configuration["Keycloak:AdminUsername"];
        var adminPassword = configuration["Keycloak:AdminPassword"];

        _client = new KeycloakClient(adminUrl, adminUsername, adminPassword);
    }

    public async Task<string> CreateUserAsync(CreateUserRequest request)
    {
        try
        {
            var user = new User
            {
                UserName = request.Username,
                Email = request.Email,
                FirstName = request.FirstName,
                LastName = request.LastName,
                Enabled = true,
                EmailVerified = false,
                Attributes = new Dictionary<string, IEnumerable<string>>
                {
                    ["municipality_id"] = new[] { request.MunicipalityId }
                }
            };

            var userId = await _client.CreateUserAsync(_realm, user);

            _logger.LogInformation(
                "User created in Keycloak: {Username} (ID: {UserId})",
                request.Username, userId);

            // Set password
            await _client.ResetUserPasswordAsync(_realm, userId, new Credentials
            {
                Type = "password",
                Value = request.Password,
                Temporary = request.RequirePasswordChange
            });

            return userId;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to create user in Keycloak: {Username}",
                request.Username);
            throw;
        }
    }

    public async Task AssignRoleAsync(string userId, string roleName)
    {
        try
        {
            var roles = await _client.GetRolesAsync(_realm);
            var role = roles.FirstOrDefault(r => r.Name == roleName);

            if (role == null)
            {
                throw new InvalidOperationException($"Role '{roleName}' not found");
            }

            await _client.AddRealmRoleMappingsToUserAsync(_realm, userId, new[] { role });

            _logger.LogInformation(
                "Role '{RoleName}' assigned to user {UserId}",
                roleName, userId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex,
                "Failed to assign role '{RoleName}' to user {UserId}",
                roleName, userId);
            throw;
        }
    }

    public async Task UpdateUserAsync(string userId, UpdateUserRequest request)
    {
        try
        {
            var user = await _client.GetUserAsync(_realm, userId);

            if (request.Email != null) user.Email = request.Email;
            if (request.FirstName != null) user.FirstName = request.FirstName;
            if (request.LastName != null) user.LastName = request.LastName;
            if (request.Enabled.HasValue) user.Enabled = request.Enabled.Value;

            await _client.UpdateUserAsync(_realm, userId, user);

            _logger.LogInformation("User updated in Keycloak: {UserId}", userId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to update user in Keycloak: {UserId}", userId);
            throw;
        }
    }

    public async Task DeleteUserAsync(string userId)
    {
        try
        {
            await _client.DeleteUserAsync(_realm, userId);
            _logger.LogInformation("User deleted from Keycloak: {UserId}", userId);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to delete user from Keycloak: {UserId}", userId);
            throw;
        }
    }

    public async Task<User> GetUserByIdAsync(string userId)
    {
        return await _client.GetUserAsync(_realm, userId);
    }
}

public record CreateUserRequest(
    string Username,
    string Email,
    string FirstName,
    string LastName,
    string Password,
    string MunicipalityId,
    bool RequirePasswordChange = true);

public record UpdateUserRequest(
    string? Email = null,
    string? FirstName = null,
    string? LastName = null,
    bool? Enabled = null);
```

### 2.10 Error Handling com Keycloak

```csharp
// GEOAPI/src/Gateway/Middleware/JwtExceptionMiddleware.cs

using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.IdentityModel.Tokens;

namespace GEOAPI.Gateway.Middleware;

public class JwtExceptionMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<JwtExceptionMiddleware> _logger;

    public JwtExceptionMiddleware(
        RequestDelegate next,
        ILogger<JwtExceptionMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await _next(context);
        }
        catch (SecurityTokenException ex)
        {
            _logger.LogWarning(ex, "JWT token validation failed");
            await HandleJwtExceptionAsync(context, ex);
        }
    }

    private static Task HandleJwtExceptionAsync(HttpContext context, Exception exception)
    {
        context.Response.StatusCode = (int)HttpStatusCode.Unauthorized;
        context.Response.ContentType = "application/json";

        var errorResponse = new
        {
            statusCode = 401,
            message = "Token inválido ou expirado",
            detail = exception.Message,
            timestamp = DateTime.UtcNow
        };

        return context.Response.WriteAsJsonAsync(errorResponse);
    }
}
```

**Registro no Program.cs:**
```csharp
app.UseMiddleware<JwtExceptionMiddleware>();
app.UseAuthentication();
app.UseAuthorization();
```

---

## 3. Integração com PostgreSQL + PostGIS

### 3.1 Visão Geral

O GEOAPI utiliza **PostgreSQL 16** com extensão **PostGIS 3.4** para armazenamento de dados espaciais e não-espaciais.

**Funcionalidades:**
- Armazenamento de geometrias (pontos, polígonos, linhas)
- Queries espaciais (intersections, distance, contains)
- Row-Level Security (RLS) para multi-tenancy
- Full-Text Search (FTS) para pesquisa textual
- Triggers e Stored Procedures para lógica de negócio

### 3.2 Connection String

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=postgres.carf.gov.br;Port=5432;Database=carf_geoapi;Username=geoapi_user;Password=${DB_PASSWORD};SSL Mode=Require;Trust Server Certificate=false;Include Error Detail=true"
  }
}
```

**Variáveis de ambiente:**
- `DB_PASSWORD`: Senha do usuário do banco (injetada via Kubernetes Secret)

### 3.3 DbContext Configuration

```csharp
// GEOAPI/src/Infrastructure/Persistence/ApplicationDbContext.cs

using Microsoft.EntityFrameworkCore;
using NetTopologySuite.Geometries;
using GEOAPI.Domain.Entities;

namespace GEOAPI.Infrastructure.Persistence;

public class ApplicationDbContext : DbContext
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public ApplicationDbContext(
        DbContextOptions<ApplicationDbContext> options,
        IHttpContextAccessor httpContextAccessor) : base(options)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public DbSet<Unit> Units => Set<Unit>();
    public DbSet<Community> Communities => Set<Community>();
    public DbSet<Holder> Holders => Set<Holder>();
    public DbSet<LegitimationRequest> LegitimationRequests => Set<LegitimationRequest>();
    public DbSet<Municipality> Municipalities => Set<Municipality>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        // Apply all configurations from assembly
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);

        // Enable PostGIS extension
        modelBuilder.HasPostgresExtension("postgis");

        // Enable UUID extension
        modelBuilder.HasPostgresExtension("uuid-ossp");

        // Configure RLS (Row-Level Security)
        ConfigureRowLevelSecurity(modelBuilder);
    }

    private void ConfigureRowLevelSecurity(ModelBuilder modelBuilder)
    {
        // Set municipality_id context variable before each query
        // This enables RLS policies to filter data by municipality

        // Note: RLS is configured at database level, not in EF Core
        // See migration files for RLS policies
    }

    public override async Task<int> SaveChangesAsync(CancellationToken cancellationToken = default)
    {
        // Set municipality_id from JWT claim
        var municipalityId = _httpContextAccessor.HttpContext?.User
            .FindFirst("municipality_id")?.Value;

        if (!string.IsNullOrEmpty(municipalityId))
        {
            // Set session variable for RLS
            await Database.ExecuteSqlRawAsync(
                "SET LOCAL app.current_municipality_id = {0}",
                municipalityId);
        }

        // Set audit fields
        var entries = ChangeTracker.Entries()
            .Where(e => e.Entity is IAuditableEntity &&
                (e.State == EntityState.Added || e.State == EntityState.Modified));

        foreach (var entry in entries)
        {
            var entity = (IAuditableEntity)entry.Entity;
            var userId = _httpContextAccessor.HttpContext?.User
                .FindFirst("sub")?.Value;

            if (entry.State == EntityState.Added)
            {
                entity.CreatedAt = DateTime.UtcNow;
                entity.CreatedBy = userId;
            }

            entity.UpdatedAt = DateTime.UtcNow;
            entity.UpdatedBy = userId;
        }

        return await base.SaveChangesAsync(cancellationToken);
    }
}
```

### 3.4 Entity Configuration com PostGIS

```csharp
// GEOAPI/src/Infrastructure/Persistence/Configurations/UnitConfiguration.cs

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using NetTopologySuite.Geometries;
using GEOAPI.Domain.Entities;

namespace GEOAPI.Infrastructure.Persistence.Configurations;

public class UnitConfiguration : IEntityTypeConfiguration<Unit>
{
    public void Configure(EntityTypeBuilder<Unit> builder)
    {
        builder.ToTable("units");

        builder.HasKey(u => u.Id);

        builder.Property(u => u.Id)
            .HasConversion(
                id => id.Value,
                value => new UnitId(value))
            .HasColumnName("id")
            .HasDefaultValueSql("uuid_generate_v4()");

        // Geometry column with PostGIS
        builder.Property(u => u.Location)
            .HasColumnName("location")
            .HasColumnType("geometry(Point, 4674)") // SIRGAS 2000 (Brazilian CRS)
            .IsRequired();

        // Spatial index for fast geometric queries
        builder.HasIndex(u => u.Location)
            .HasMethod("gist");

        // Polygon geometry for unit boundaries
        builder.Property(u => u.Boundary)
            .HasColumnName("boundary")
            .HasColumnType("geometry(Polygon, 4674)")
            .IsRequired(false);

        builder.HasIndex(u => u.Boundary)
            .HasMethod("gist");

        // Calculated area (in square meters)
        builder.Property(u => u.Area)
            .HasColumnName("area")
            .HasColumnType("decimal(12,2)")
            .IsRequired();

        // Address (Value Object)
        builder.OwnsOne(u => u.Address, address =>
        {
            address.Property(a => a.Street).HasColumnName("street").HasMaxLength(200);
            address.Property(a => a.Number).HasColumnName("number").HasMaxLength(20);
            address.Property(a => a.Neighborhood).HasColumnName("neighborhood").HasMaxLength(100);
            address.Property(a => a.City).HasColumnName("city").HasMaxLength(100);
            address.Property(a => a.State).HasColumnName("state").HasMaxLength(2);
            address.Property(a => a.PostalCode).HasColumnName("postal_code").HasMaxLength(9);
        });

        // Municipality relationship
        builder.Property(u => u.MunicipalityId)
            .HasConversion(
                id => id.Value,
                value => new MunicipalityId(value))
            .HasColumnName("municipality_id")
            .IsRequired();

        builder.HasOne(u => u.Municipality)
            .WithMany()
            .HasForeignKey(u => u.MunicipalityId)
            .OnDelete(DeleteBehavior.Restrict);

        // Holders relationship (1-to-many)
        builder.HasMany(u => u.Holders)
            .WithOne()
            .HasForeignKey("UnitId")
            .OnDelete(DeleteBehavior.Cascade);

        // Audit fields
        builder.Property(u => u.CreatedAt)
            .HasColumnName("created_at")
            .IsRequired();

        builder.Property(u => u.CreatedBy)
            .HasColumnName("created_by")
            .HasMaxLength(100);

        builder.Property(u => u.UpdatedAt)
            .HasColumnName("updated_at");

        builder.Property(u => u.UpdatedBy)
            .HasColumnName("updated_by")
            .HasMaxLength(100);

        // Soft delete
        builder.Property(u => u.IsDeleted)
            .HasColumnName("is_deleted")
            .HasDefaultValue(false);

        builder.HasQueryFilter(u => !u.IsDeleted);

        // Indexes for performance
        builder.HasIndex(u => u.MunicipalityId);
        builder.HasIndex(u => u.CreatedAt);
        builder.HasIndex(u => u.IsDeleted);
    }
}
```

### 3.5 PostGIS Queries com EF Core

```csharp
// GEOAPI/src/Infrastructure/Persistence/Repositories/UnitRepository.cs

using Microsoft.EntityFrameworkCore;
using NetTopologySuite.Geometries;
using GEOAPI.Domain.Entities;
using GEOAPI.Domain.Repositories;

namespace GEOAPI.Infrastructure.Persistence.Repositories;

public class UnitRepository : IUnitRepository
{
    private readonly ApplicationDbContext _context;

    public UnitRepository(ApplicationDbContext context)
    {
        _context = context;
    }

    // Find units within a polygon
    public async Task<List<Unit>> FindUnitsWithinPolygonAsync(Polygon polygon)
    {
        return await _context.Units
            .Where(u => u.Location.Within(polygon))
            .ToListAsync();
    }

    // Find units within radius (in meters)
    public async Task<List<Unit>> FindUnitsWithinRadiusAsync(Point center, double radiusMeters)
    {
        return await _context.Units
            .Where(u => u.Location.Distance(center) <= radiusMeters)
            .OrderBy(u => u.Location.Distance(center))
            .ToListAsync();
    }

    // Find units intersecting with a geometry
    public async Task<List<Unit>> FindUnitsIntersectingAsync(Geometry geometry)
    {
        return await _context.Units
            .Where(u => u.Boundary != null && u.Boundary.Intersects(geometry))
            .ToListAsync();
    }

    // Calculate total area of units in a community
    public async Task<double> CalculateTotalAreaAsync(Guid communityId)
    {
        return await _context.Units
            .Where(u => u.CommunityId == new CommunityId(communityId))
            .SumAsync(u => (double)u.Area);
    }

    // Find nearest unit to a point
    public async Task<Unit?> FindNearestUnitAsync(Point point)
    {
        return await _context.Units
            .OrderBy(u => u.Location.Distance(point))
            .FirstOrDefaultAsync();
    }

    // Check if point is within any unit boundary
    public async Task<Unit?> FindUnitContainingPointAsync(Point point)
    {
        return await _context.Units
            .FirstOrDefaultAsync(u => u.Boundary != null && u.Boundary.Contains(point));
    }

    // Full-text search in address
    public async Task<List<Unit>> SearchByAddressAsync(string searchTerm)
    {
        return await _context.Units
            .Where(u => EF.Functions.ILike(u.Address.Street, $"%{searchTerm}%") ||
                        EF.Functions.ILike(u.Address.Neighborhood, $"%{searchTerm}%"))
            .ToListAsync();
    }
}
```

### 3.6 Row-Level Security (RLS) Migration

```csharp
// GEOAPI/src/Infrastructure/Persistence/Migrations/20260109_AddRowLevelSecurity.cs

using Microsoft.EntityFrameworkCore.Migrations;

namespace GEOAPI.Infrastructure.Persistence.Migrations;

public partial class AddRowLevelSecurity : Migration
{
    protected override void Up(MigrationBuilder migrationBuilder)
    {
        // Enable RLS on units table
        migrationBuilder.Sql(@"
            ALTER TABLE units ENABLE ROW LEVEL SECURITY;
        ");

        // Policy: Users can only see units from their municipality
        migrationBuilder.Sql(@"
            CREATE POLICY units_select_policy ON units
            FOR SELECT
            USING (
                municipality_id = COALESCE(
                    current_setting('app.current_municipality_id', true)::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid
                )
            );
        ");

        // Policy: Users can only insert units for their municipality
        migrationBuilder.Sql(@"
            CREATE POLICY units_insert_policy ON units
            FOR INSERT
            WITH CHECK (
                municipality_id = COALESCE(
                    current_setting('app.current_municipality_id', true)::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid
                )
            );
        ");

        // Policy: Users can only update units from their municipality
        migrationBuilder.Sql(@"
            CREATE POLICY units_update_policy ON units
            FOR UPDATE
            USING (
                municipality_id = COALESCE(
                    current_setting('app.current_municipality_id', true)::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid
                )
            );
        ");

        // Policy: Users can only delete units from their municipality
        migrationBuilder.Sql(@"
            CREATE POLICY units_delete_policy ON units
            FOR DELETE
            USING (
                municipality_id = COALESCE(
                    current_setting('app.current_municipality_id', true)::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid
                )
            );
        ");

        // Create bypass policy for admin users
        migrationBuilder.Sql(@"
            CREATE POLICY units_admin_bypass_policy ON units
            FOR ALL
            USING (
                current_setting('app.current_user_role', true) = 'ADMIN'
            );
        ");

        // Apply same policies to other tables
        ApplyRLSToCommunities(migrationBuilder);
        ApplyRLSToHolders(migrationBuilder);
        ApplyRLSToLegitimationRequests(migrationBuilder);
    }

    protected override void Down(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql("DROP POLICY IF EXISTS units_select_policy ON units;");
        migrationBuilder.Sql("DROP POLICY IF EXISTS units_insert_policy ON units;");
        migrationBuilder.Sql("DROP POLICY IF EXISTS units_update_policy ON units;");
        migrationBuilder.Sql("DROP POLICY IF EXISTS units_delete_policy ON units;");
        migrationBuilder.Sql("DROP POLICY IF EXISTS units_admin_bypass_policy ON units;");
        migrationBuilder.Sql("ALTER TABLE units DISABLE ROW LEVEL SECURITY;");

        // Revert for other tables...
    }

    private void ApplyRLSToCommunities(MigrationBuilder migrationBuilder)
    {
        migrationBuilder.Sql(@"
            ALTER TABLE communities ENABLE ROW LEVEL SECURITY;
            CREATE POLICY communities_municipality_policy ON communities
            FOR ALL
            USING (
                municipality_id = COALESCE(
                    current_setting('app.current_municipality_id', true)::uuid,
                    '00000000-0000-0000-0000-000000000000'::uuid
                )
                OR current_setting('app.current_user_role', true) = 'ADMIN'
            );
        ");
    }

    private void ApplyRLSToHolders(MigrationBuilder migrationBuilder)
    {
        // Similar implementation for holders table
    }

    private void ApplyRLSToLegitimationRequests(MigrationBuilder migrationBuilder)
    {
        // Similar implementation for legitimation_requests table
    }
}
```

### 3.7 Connection Resilience

```csharp
// GEOAPI/src/Infrastructure/DependencyInjection/DatabaseExtensions.cs

using Microsoft.EntityFrameworkCore;
using Npgsql;

namespace GEOAPI.Infrastructure.DependencyInjection;

public static class DatabaseExtensions
{
    public static IServiceCollection AddDatabase(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        var connectionString = configuration.GetConnectionString("DefaultConnection");

        services.AddDbContext<ApplicationDbContext>(options =>
        {
            options.UseNpgsql(connectionString, npgsqlOptions =>
            {
                // Enable PostGIS extension
                npgsqlOptions.UseNetTopologySuite();

                // Configure retry logic
                npgsqlOptions.EnableRetryOnFailure(
                    maxRetryCount: 5,
                    maxRetryDelay: TimeSpan.FromSeconds(30),
                    errorCodesToAdd: null);

                // Command timeout (30 seconds)
                npgsqlOptions.CommandTimeout(30);

                // Migrations assembly
                npgsqlOptions.MigrationsAssembly("GEOAPI.Infrastructure");
            });

            // Enable sensitive data logging in development
            if (configuration.GetValue<bool>("Logging:EnableSensitiveDataLogging"))
            {
                options.EnableSensitiveDataLogging();
            }

            // Enable detailed errors
            options.EnableDetailedErrors();
        });

        return services;
    }
}
```

### 3.8 Database Health Check

```csharp
// GEOAPI/src/Infrastructure/HealthChecks/DatabaseHealthCheck.cs

using Microsoft.Extensions.Diagnostics.HealthChecks;
using Npgsql;

namespace GEOAPI.Infrastructure.HealthChecks;

public class DatabaseHealthCheck : IHealthCheck
{
    private readonly string _connectionString;

    public DatabaseHealthCheck(IConfiguration configuration)
    {
        _connectionString = configuration.GetConnectionString("DefaultConnection")
            ?? throw new InvalidOperationException("Connection string not found");
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            await using var connection = new NpgsqlConnection(_connectionString);
            await connection.OpenAsync(cancellationToken);

            // Check PostGIS extension
            await using var command = new NpgsqlCommand(
                "SELECT PostGIS_Version();",
                connection);

            var result = await command.ExecuteScalarAsync(cancellationToken);

            var data = new Dictionary<string, object>
            {
                ["postgis_version"] = result?.ToString() ?? "unknown",
                ["connection_state"] = connection.State.ToString()
            };

            return HealthCheckResult.Healthy("PostgreSQL + PostGIS is healthy", data);
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy(
                "PostgreSQL + PostGIS is unhealthy",
                ex);
        }
    }
}
```

---

## 4. Consumidores da API

### 4.1 Visão Geral dos Consumidores

O GEOAPI é consumido por 4 aplicações frontend:

| Aplicação | Tecnologia | Plataforma | Autenticação | Usuários |
|-----------|-----------|------------|--------------|----------|
| **GEOWEB** | React + TypeScript | Web (Desktop) | OAuth2 PKCE | Analistas, Gestores |
| **REURBCAD** | React Native + TypeScript | Mobile (Android/iOS) | OAuth2 PKCE | Agentes de Campo |
| **ADMIN** | React + TypeScript | Web (Desktop) | OAuth2 PKCE | Administradores |
| **GEOGIS** | React + TypeScript | Web (Desktop/Mobile) | Public (Read-only) | Público Geral |

### 4.2 GEOWEB (Frontend Web para Analistas)

**Descrição:** Aplicação web desktop para analistas e gestores municipais realizarem cadastro e gestão de imóveis.

**Funcionalidades principais:**
- Visualização de mapas com camadas (communities, units, boundaries)
- Cadastro de unidades imobiliárias
- Gestão de possuidores
- Análise de pedidos de legitimação
- Relatórios e dashboards

**Stack:**
- React 18 + TypeScript
- Feature-Sliced Design (FSD)
- TanStack Query (react-query) para cache
- Leaflet / Mapbox para mapas
- @carf/geoapi-client (SDK TypeScript)
- @carf/ui (componentes compartilhados)

**Exemplo de uso do SDK:**

```typescript
// GEOWEB/src/features/units/api/useUnits.ts

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { geoApiClient } from '@/shared/api/geoApiClient';
import type { Unit, CreateUnitDto, UpdateUnitDto } from '@carf/geoapi-client';

export function useUnits(params?: { page?: number; pageSize?: number }) {
  return useQuery({
    queryKey: ['units', params],
    queryFn: () => geoApiClient.units.list(params),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useUnit(id: string) {
  return useQuery({
    queryKey: ['units', id],
    queryFn: () => geoApiClient.units.getById(id),
    enabled: !!id,
  });
}

export function useCreateUnit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUnitDto) => geoApiClient.units.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
    },
  });
}

export function useUpdateUnit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdateUnitDto }) =>
      geoApiClient.units.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
      queryClient.invalidateQueries({ queryKey: ['units', variables.id] });
    },
  });
}

export function useDeleteUnit() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => geoApiClient.units.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['units'] });
    },
  });
}
```

**Configuração de autenticação:**

```typescript
// GEOWEB/src/app/providers/AuthProvider.tsx

import { createContext, useContext, useEffect, useState } from 'react';
import { useAuth as useKeycloakAuth } from 'react-oidc-context';
import { geoApiClient } from '@/shared/api/geoApiClient';

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const keycloakAuth = useKeycloakAuth();

  useEffect(() => {
    if (keycloakAuth.isAuthenticated && keycloakAuth.user?.access_token) {
      // Set access token in API client
      geoApiClient.setAccessToken(keycloakAuth.user.access_token);

      // Setup token refresh
      const refreshInterval = setInterval(async () => {
        try {
          await keycloakAuth.signinSilent();
        } catch (error) {
          console.error('Failed to refresh token:', error);
        }
      }, 4 * 60 * 1000); // Refresh every 4 minutes (token expires in 5)

      return () => clearInterval(refreshInterval);
    }
  }, [keycloakAuth.isAuthenticated, keycloakAuth.user?.access_token]);

  return <>{children}</>;
}
```

### 4.3 REURBCAD (Mobile App para Agentes de Campo)

**Descrição:** Aplicação móvel offline-first para agentes de campo realizarem cadastro em áreas sem conexão à internet.

**Funcionalidades principais:**
- Cadastro offline de unidades (GPS, fotos, dados)
- Sincronização automática quando online
- Mapa offline (tiles pré-baixados)
- Captura de coordenadas GPS
- Upload de fotos e documentos

**Stack:**
- React Native + TypeScript
- WatermelonDB (banco local SQLite)
- React Navigation
- React Native Maps
- @carf/geoapi-client (SDK TypeScript)

**Exemplo de sincronização offline:**

```typescript
// REURBCAD/src/features/sync/services/SyncService.ts

import { database } from '@/shared/db/database';
import { geoApiClient } from '@/shared/api/geoApiClient';
import NetInfo from '@react-native-community/netinfo';
import { Q } from '@nozbe/watermelondb';

export class SyncService {
  async syncUnits(): Promise<void> {
    const isConnected = await this.checkConnection();

    if (!isConnected) {
      console.log('No internet connection. Skipping sync.');
      return;
    }

    try {
      // 1. Push local changes to server
      await this.pushLocalChanges();

      // 2. Pull server changes to local
      await this.pullServerChanges();

      console.log('Sync completed successfully');
    } catch (error) {
      console.error('Sync failed:', error);
      throw error;
    }
  }

  private async pushLocalChanges(): Promise<void> {
    const unitsCollection = database.get('units');

    // Find units pending sync (created/updated locally)
    const pendingUnits = await unitsCollection
      .query(Q.where('synced', false))
      .fetch();

    for (const unit of pendingUnits) {
      try {
        if (unit._raw._status === 'created') {
          // Create on server
          const serverUnit = await geoApiClient.units.create({
            address: unit.address,
            coordinates: { lat: unit.latitude, lng: unit.longitude },
            area: unit.area,
            // ... other fields
          });

          // Update local record with server ID
          await database.write(async () => {
            await unit.update(u => {
              u.serverId = serverUnit.id;
              u.synced = true;
            });
          });
        } else if (unit._raw._status === 'updated') {
          // Update on server
          await geoApiClient.units.update(unit.serverId!, {
            address: unit.address,
            // ... other fields
          });

          await database.write(async () => {
            await unit.update(u => {
              u.synced = true;
            });
          });
        }
      } catch (error) {
        console.error(`Failed to sync unit ${unit.id}:`, error);
        // Continue with next unit
      }
    }
  }

  private async pullServerChanges(): Promise<void> {
    const lastSyncTimestamp = await this.getLastSyncTimestamp();

    // Fetch units updated since last sync
    const serverUnits = await geoApiClient.units.list({
      updatedAfter: lastSyncTimestamp,
      pageSize: 1000,
    });

    await database.write(async () => {
      for (const serverUnit of serverUnits.data) {
        const unitsCollection = database.get('units');

        const existingUnit = await unitsCollection
          .query(Q.where('server_id', serverUnit.id))
          .fetch();

        if (existingUnit.length > 0) {
          // Update existing
          await existingUnit[0].update(u => {
            u.address = serverUnit.address;
            u.latitude = serverUnit.coordinates.lat;
            u.longitude = serverUnit.coordinates.lng;
            u.area = serverUnit.area;
            u.synced = true;
            // ... other fields
          });
        } else {
          // Create new
          await unitsCollection.create(u => {
            u.serverId = serverUnit.id;
            u.address = serverUnit.address;
            u.latitude = serverUnit.coordinates.lat;
            u.longitude = serverUnit.coordinates.lng;
            u.area = serverUnit.area;
            u.synced = true;
            // ... other fields
          });
        }
      }
    });

    await this.setLastSyncTimestamp(new Date());
  }

  private async checkConnection(): Promise<boolean> {
    const state = await NetInfo.fetch();
    return state.isConnected ?? false;
  }

  private async getLastSyncTimestamp(): Promise<Date | null> {
    // Retrieve from AsyncStorage
    // ...
    return null;
  }

  private async setLastSyncTimestamp(timestamp: Date): Promise<void> {
    // Store in AsyncStorage
    // ...
  }
}

export const syncService = new SyncService();
```

### 4.4 ADMIN (Painel Administrativo)

**Descrição:** Aplicação web para administradores do sistema realizarem gestão de usuários, municípios e configurações.

**Funcionalidades principais:**
- Gestão de usuários e roles
- Gestão de municípios
- Auditoria e logs
- Configurações do sistema
- Relatórios globais

**Stack:**
- React 18 + TypeScript
- Feature-Sliced Design (FSD)
- TanStack Query
- @carf/geoapi-client
- @carf/ui

**Exemplo de gestão de usuários:**

```typescript
// ADMIN/src/features/users/api/useUsers.ts

import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { geoApiClient } from '@/shared/api/geoApiClient';
import type { User, CreateUserDto, UpdateUserDto } from '@carf/geoapi-client';

export function useUsers(params?: { role?: string; municipalityId?: string }) {
  return useQuery({
    queryKey: ['users', params],
    queryFn: () => geoApiClient.users.list(params),
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateUserDto) => geoApiClient.users.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
    },
  });
}

export function useAssignRole() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ userId, role }: { userId: string; role: string }) =>
      geoApiClient.users.assignRole(userId, role),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['users'] });
      queryClient.invalidateQueries({ queryKey: ['users', variables.userId] });
    },
  });
}
```

### 4.5 GEOGIS (Portal Público)

**Descrição:** Aplicação web pública (sem autenticação) para consulta de informações de regularização fundiária.

**Funcionalidades principais:**
- Visualização de mapa público
- Consulta de status de regularização por endereço
- Informações sobre o programa
- FAQ e documentação

**Stack:**
- React 18 + TypeScript
- Next.js (SSR/SSG)
- @carf/geoapi-client
- @carf/ui

**Exemplo de consulta pública:**

```typescript
// GEOGIS/src/features/public-search/api/usePublicSearch.ts

import { useQuery } from '@tanstack/react-query';
import { geoApiClient } from '@/shared/api/geoApiClient';

// Note: Public endpoints don't require authentication
export function usePublicSearchByAddress(address: string) {
  return useQuery({
    queryKey: ['public-search', 'address', address],
    queryFn: () => geoApiClient.public.searchByAddress(address),
    enabled: address.length >= 3,
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

export function usePublicUnitStatus(unitId: string) {
  return useQuery({
    queryKey: ['public-search', 'unit', unitId],
    queryFn: () => geoApiClient.public.getUnitStatus(unitId),
    enabled: !!unitId,
  });
}
```

### 4.6 Tratamento de Erros nos Consumidores

Todos os consumidores utilizam um error handler compartilhado do SDK:

```typescript
// @carf/geoapi-client/src/errorHandler.ts

import type { AxiosError } from 'axios';

export interface ApiError {
  statusCode: number;
  message: string;
  detail?: string;
  errors?: Record<string, string[]>;
  timestamp: string;
}

export class GeoApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public detail?: string,
    public errors?: Record<string, string[]>
  ) {
    super(message);
    this.name = 'GeoApiError';
  }

  static fromAxiosError(error: AxiosError<ApiError>): GeoApiError {
    if (error.response) {
      const { statusCode, message, detail, errors } = error.response.data;
      return new GeoApiError(statusCode, message, detail, errors);
    }

    if (error.request) {
      return new GeoApiError(
        0,
        'No response from server. Please check your internet connection.',
        error.message
      );
    }

    return new GeoApiError(0, 'Request failed', error.message);
  }

  isUnauthorized(): boolean {
    return this.statusCode === 401;
  }

  isForbidden(): boolean {
    return this.statusCode === 403;
  }

  isNotFound(): boolean {
    return this.statusCode === 404;
  }

  isValidationError(): boolean {
    return this.statusCode === 400 && !!this.errors;
  }
}
```

**Uso no frontend:**

```typescript
// GEOWEB/src/features/units/components/CreateUnitForm.tsx

import { useCreateUnit } from '../api/useUnits';
import { GeoApiError } from '@carf/geoapi-client';
import { toast } from '@/shared/ui/toast';

export function CreateUnitForm() {
  const createUnit = useCreateUnit();

  const handleSubmit = async (data: CreateUnitDto) => {
    try {
      await createUnit.mutateAsync(data);
      toast.success('Unit created successfully!');
    } catch (error) {
      if (error instanceof GeoApiError) {
        if (error.isUnauthorized()) {
          toast.error('Your session expired. Please login again.');
          // Redirect to login
        } else if (error.isValidationError()) {
          // Display validation errors
          Object.entries(error.errors!).forEach(([field, messages]) => {
            toast.error(`${field}: ${messages.join(', ')}`);
          });
        } else {
          toast.error(error.message);
        }
      } else {
        toast.error('An unexpected error occurred');
      }
    }
  };

  return (
    // ... form JSX
  );
}
```

---

## 5. Serviços Externos

### 5.1 Serviço de Email (SMTP)

**Descrição:** Envio de emails transacionais (notificações, confirmações, alertas).

**Configuração:**

```json
{
  "Email": {
    "SmtpHost": "smtp.gmail.com",
    "SmtpPort": 587,
    "SmtpUsername": "noreply@carf.gov.br",
    "SmtpPassword": "${EMAIL_PASSWORD}",
    "UseSsl": true,
    "From": "noreply@carf.gov.br",
    "FromName": "CARF - Regularização Fundiária"
  }
}
```

**Implementação:**

```csharp
// GEOAPI/src/Infrastructure/ExternalServices/EmailService.cs

using MailKit.Net.Smtp;
using MimeKit;

namespace GEOAPI.Infrastructure.ExternalServices;

public interface IEmailService
{
    Task SendAsync(string to, string subject, string body);
    Task SendTemplateAsync(string to, string templateName, object data);
}

public class EmailService : IEmailService
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<EmailService> _logger;

    public EmailService(
        IConfiguration configuration,
        ILogger<EmailService> logger)
    {
        _configuration = configuration;
        _logger = logger;
    }

    public async Task SendAsync(string to, string subject, string body)
    {
        try
        {
            var message = new MimeMessage();
            message.From.Add(new MailboxAddress(
                _configuration["Email:FromName"],
                _configuration["Email:From"]));
            message.To.Add(MailboxAddress.Parse(to));
            message.Subject = subject;
            message.Body = new TextPart("html") { Text = body };

            using var client = new SmtpClient();
            await client.ConnectAsync(
                _configuration["Email:SmtpHost"],
                int.Parse(_configuration["Email:SmtpPort"]!),
                bool.Parse(_configuration["Email:UseSsl"]!));

            await client.AuthenticateAsync(
                _configuration["Email:SmtpUsername"],
                _configuration["Email:SmtpPassword"]);

            await client.SendAsync(message);
            await client.DisconnectAsync(true);

            _logger.LogInformation("Email sent to {To}: {Subject}", to, subject);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to send email to {To}", to);
            throw;
        }
    }

    public async Task SendTemplateAsync(string to, string templateName, object data)
    {
        var template = await LoadTemplateAsync(templateName);
        var body = RenderTemplate(template, data);
        var subject = ExtractSubject(template);

        await SendAsync(to, subject, body);
    }

    private async Task<string> LoadTemplateAsync(string templateName)
    {
        var path = Path.Combine("Templates", "Email", $"{templateName}.html");
        return await File.ReadAllTextAsync(path);
    }

    private string RenderTemplate(string template, object data)
    {
        // Simple string replacement (consider using a templating engine like Handlebars)
        var result = template;
        foreach (var prop in data.GetType().GetProperties())
        {
            var placeholder = $"{{{{{prop.Name}}}}}";
            var value = prop.GetValue(data)?.ToString() ?? "";
            result = result.Replace(placeholder, value);
        }
        return result;
    }

    private string ExtractSubject(string template)
    {
        // Extract subject from <!-- SUBJECT: ... --> comment
        var match = System.Text.RegularExpressions.Regex.Match(
            template,
            @"<!-- SUBJECT: (.+?) -->");
        return match.Success ? match.Groups[1].Value : "Notification";
    }
}
```

**Template de email:**

```html
<!-- GEOAPI/Templates/Email/UnitCreated.html -->
<!-- SUBJECT: Nova Unidade Cadastrada - {{UnitAddress}} -->

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #1976d2; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .button { display: inline-block; padding: 10px 20px; background: #1976d2; color: white; text-decoration: none; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>CARF - Regularização Fundiária</h1>
        </div>
        <div class="content">
            <h2>Nova Unidade Cadastrada</h2>
            <p>Olá {{HolderName}},</p>
            <p>Uma nova unidade foi cadastrada no sistema:</p>
            <ul>
                <li><strong>Endereço:</strong> {{UnitAddress}}</li>
                <li><strong>Área:</strong> {{UnitArea}} m²</li>
                <li><strong>Cadastrado em:</strong> {{CreatedAt}}</li>
            </ul>
            <p>Você pode visualizar os detalhes acessando o portal:</p>
            <p style="text-align: center;">
                <a href="{{PortalUrl}}" class="button">Acessar Portal</a>
            </p>
        </div>
    </div>
</body>
</html>
```

### 5.2 Serviço de SMS

**Descrição:** Envio de SMS para notificações críticas.

**Configuração:**

```json
{
  "Sms": {
    "Provider": "Twilio",
    "AccountSid": "${TWILIO_ACCOUNT_SID}",
    "AuthToken": "${TWILIO_AUTH_TOKEN}",
    "FromNumber": "+5511999999999"
  }
}
```

**Implementação:**

```csharp
// GEOAPI/src/Infrastructure/ExternalServices/SmsService.cs

using Twilio;
using Twilio.Rest.Api.V2010.Account;
using Twilio.Types;

namespace GEOAPI.Infrastructure.ExternalServices;

public interface ISmsService
{
    Task SendAsync(string to, string message);
}

public class SmsService : ISmsService
{
    private readonly IConfiguration _configuration;
    private readonly ILogger<SmsService> _logger;

    public SmsService(
        IConfiguration configuration,
        ILogger<SmsService> logger)
    {
        _configuration = configuration;
        _logger = logger;

        TwilioClient.Init(
            _configuration["Sms:AccountSid"],
            _configuration["Sms:AuthToken"]);
    }

    public async Task SendAsync(string to, string message)
    {
        try
        {
            var result = await MessageResource.CreateAsync(
                to: new PhoneNumber(to),
                from: new PhoneNumber(_configuration["Sms:FromNumber"]!),
                body: message);

            _logger.LogInformation(
                "SMS sent to {To}. SID: {Sid}",
                to, result.Sid);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to send SMS to {To}", to);
            throw;
        }
    }
}
```

### 5.3 Serviço de Armazenamento (S3 / File System)

**Descrição:** Armazenamento de fotos, documentos e arquivos.

**Configuração:**

```json
{
  "Storage": {
    "Provider": "S3",
    "S3": {
      "BucketName": "carf-geoapi-files",
      "Region": "us-east-1",
      "AccessKeyId": "${AWS_ACCESS_KEY_ID}",
      "SecretAccessKey": "${AWS_SECRET_ACCESS_KEY}"
    },
    "FileSystem": {
      "BasePath": "/var/carf/files"
    }
  }
}
```

**Implementação:**

```csharp
// GEOAPI/src/Infrastructure/ExternalServices/StorageService.cs

using Amazon.S3;
using Amazon.S3.Model;

namespace GEOAPI.Infrastructure.ExternalServices;

public interface IStorageService
{
    Task<string> UploadAsync(Stream fileStream, string fileName, string contentType);
    Task<Stream> DownloadAsync(string fileKey);
    Task DeleteAsync(string fileKey);
    string GetPublicUrl(string fileKey);
}

public class S3StorageService : IStorageService
{
    private readonly IAmazonS3 _s3Client;
    private readonly string _bucketName;
    private readonly ILogger<S3StorageService> _logger;

    public S3StorageService(
        IConfiguration configuration,
        ILogger<S3StorageService> logger)
    {
        _logger = logger;
        _bucketName = configuration["Storage:S3:BucketName"]!;

        _s3Client = new AmazonS3Client(
            configuration["Storage:S3:AccessKeyId"],
            configuration["Storage:S3:SecretAccessKey"],
            Amazon.RegionEndpoint.GetBySystemName(configuration["Storage:S3:Region"]!));
    }

    public async Task<string> UploadAsync(
        Stream fileStream,
        string fileName,
        string contentType)
    {
        try
        {
            var fileKey = $"{Guid.NewGuid()}/{fileName}";

            var request = new PutObjectRequest
            {
                BucketName = _bucketName,
                Key = fileKey,
                InputStream = fileStream,
                ContentType = contentType,
                CannedACL = S3CannedACL.Private
            };

            await _s3Client.PutObjectAsync(request);

            _logger.LogInformation("File uploaded to S3: {FileKey}", fileKey);

            return fileKey;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to upload file to S3: {FileName}", fileName);
            throw;
        }
    }

    public async Task<Stream> DownloadAsync(string fileKey)
    {
        try
        {
            var request = new GetObjectRequest
            {
                BucketName = _bucketName,
                Key = fileKey
            };

            var response = await _s3Client.GetObjectAsync(request);
            return response.ResponseStream;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to download file from S3: {FileKey}", fileKey);
            throw;
        }
    }

    public async Task DeleteAsync(string fileKey)
    {
        try
        {
            var request = new DeleteObjectRequest
            {
                BucketName = _bucketName,
                Key = fileKey
            };

            await _s3Client.DeleteObjectAsync(request);

            _logger.LogInformation("File deleted from S3: {FileKey}", fileKey);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to delete file from S3: {FileKey}", fileKey);
            throw;
        }
    }

    public string GetPublicUrl(string fileKey)
    {
        // Generate pre-signed URL valid for 1 hour
        var request = new GetPreSignedUrlRequest
        {
            BucketName = _bucketName,
            Key = fileKey,
            Expires = DateTime.UtcNow.AddHours(1)
        };

        return _s3Client.GetPreSignedURL(request);
    }
}
```

---

## 6. Resiliência e Error Handling

### 6.1 Retry Policies com Polly

```csharp
// GEOAPI/src/Infrastructure/DependencyInjection/HttpClientsExtensions.cs

using Polly;
using Polly.Extensions.Http;

namespace GEOAPI.Infrastructure.DependencyInjection;

public static class HttpClientsExtensions
{
    public static IServiceCollection AddResilientHttpClients(
        this IServiceCollection services)
    {
        // Keycloak Admin Client with retry
        services.AddHttpClient<IKeycloakAdminClient, KeycloakAdminClient>()
            .AddPolicyHandler(GetRetryPolicy())
            .AddPolicyHandler(GetCircuitBreakerPolicy());

        // SMS Service with retry
        services.AddHttpClient<ISmsService, SmsService>()
            .AddPolicyHandler(GetRetryPolicy());

        return services;
    }

    private static IAsyncPolicy<HttpResponseMessage> GetRetryPolicy()
    {
        return HttpPolicyExtensions
            .HandleTransientHttpError()
            .OrResult(msg => msg.StatusCode == System.Net.HttpStatusCode.TooManyRequests)
            .WaitAndRetryAsync(
                retryCount: 3,
                sleepDurationProvider: retryAttempt => TimeSpan.FromSeconds(Math.Pow(2, retryAttempt)),
                onRetry: (outcome, timespan, retryAttempt, context) =>
                {
                    var logger = context.GetLogger();
                    logger?.LogWarning(
                        "Retry {RetryAttempt} after {Delay}s due to {Reason}",
                        retryAttempt, timespan.TotalSeconds, outcome.Exception?.Message ?? outcome.Result.StatusCode.ToString());
                });
    }

    private static IAsyncPolicy<HttpResponseMessage> GetCircuitBreakerPolicy()
    {
        return HttpPolicyExtensions
            .HandleTransientHttpError()
            .CircuitBreakerAsync(
                handledEventsAllowedBeforeBreaking: 5,
                durationOfBreak: TimeSpan.FromSeconds(30),
                onBreak: (outcome, duration) =>
                {
                    // Log circuit breaker opened
                },
                onReset: () =>
                {
                    // Log circuit breaker reset
                });
    }
}
```

### 6.2 Health Checks para Integrações

```csharp
// GEOAPI/src/Infrastructure/HealthChecks/IntegrationsHealthCheck.cs

using Microsoft.Extensions.Diagnostics.HealthChecks;

namespace GEOAPI.Infrastructure.HealthChecks;

public class KeycloakHealthCheck : IHealthCheck
{
    private readonly IConfiguration _configuration;
    private readonly HttpClient _httpClient;

    public KeycloakHealthCheck(IConfiguration configuration, IHttpClientFactory httpClientFactory)
    {
        _configuration = configuration;
        _httpClient = httpClientFactory.CreateClient();
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            var keycloakUrl = _configuration["Keycloak:Authority"];
            var response = await _httpClient.GetAsync(
                $"{keycloakUrl}/.well-known/openid-configuration",
                cancellationToken);

            if (response.IsSuccessStatusCode)
            {
                return HealthCheckResult.Healthy("Keycloak is reachable");
            }

            return HealthCheckResult.Degraded($"Keycloak returned {response.StatusCode}");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Keycloak is unreachable", ex);
        }
    }
}

public class EmailHealthCheck : IHealthCheck
{
    private readonly IEmailService _emailService;

    public EmailHealthCheck(IEmailService emailService)
    {
        _emailService = emailService;
    }

    public async Task<HealthCheckResult> CheckHealthAsync(
        HealthCheckContext context,
        CancellationToken cancellationToken = default)
    {
        try
        {
            // Try to connect to SMTP server (without sending email)
            // Implementation depends on email service
            return HealthCheckResult.Healthy("Email service is available");
        }
        catch (Exception ex)
        {
            return HealthCheckResult.Unhealthy("Email service is unavailable", ex);
        }
    }
}
```

**Registro no Program.cs:**

```csharp
builder.Services.AddHealthChecks()
    .AddCheck<DatabaseHealthCheck>("database")
    .AddCheck<KeycloakHealthCheck>("keycloak")
    .AddCheck<EmailHealthCheck>("email")
    .AddCheck<SmsHealthCheck>("sms");

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = async (context, report) =>
    {
        context.Response.ContentType = "application/json";
        var result = JsonSerializer.Serialize(new
        {
            status = report.Status.ToString(),
            checks = report.Entries.Select(e => new
            {
                name = e.Key,
                status = e.Value.Status.ToString(),
                description = e.Value.Description,
                duration = e.Value.Duration.TotalMilliseconds,
                data = e.Value.Data
            }),
            totalDuration = report.TotalDuration.TotalMilliseconds
        });
        await context.Response.WriteAsync(result);
    }
});
```

---

## 7. Monitoramento de Integrações

### 7.1 Logging Estruturado com Serilog

```csharp
// GEOAPI/src/Gateway/Program.cs

using Serilog;
using Serilog.Enrichers;

var builder = WebApplication.CreateBuilder(args);

// Configure Serilog
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithProperty("Application", "GEOAPI")
    .WriteTo.Console(outputTemplate: "[{Timestamp:HH:mm:ss} {Level:u3}] {Message:lj} {Properties:j}{NewLine}{Exception}")
    .WriteTo.File(
        path: "logs/geoapi-.log",
        rollingInterval: RollingInterval.Day,
        retainedFileCountLimit: 30)
    .WriteTo.Elasticsearch(new ElasticsearchSinkOptions(new Uri(builder.Configuration["Elasticsearch:Uri"]!))
    {
        IndexFormat = "geoapi-logs-{0:yyyy.MM.dd}",
        AutoRegisterTemplate = true,
        NumberOfShards = 2,
        NumberOfReplicas = 1
    })
    .CreateLogger();

builder.Host.UseSerilog();
```

### 7.2 Métricas com Prometheus

```csharp
// GEOAPI/src/Infrastructure/Metrics/MetricsService.cs

using Prometheus;

namespace GEOAPI.Infrastructure.Metrics;

public static class MetricsService
{
    // HTTP request metrics
    public static readonly Counter HttpRequestsTotal = Metrics
        .CreateCounter("geoapi_http_requests_total", "Total HTTP requests",
            new CounterConfiguration { LabelNames = new[] { "method", "endpoint", "status" } });

    public static readonly Histogram HttpRequestDuration = Metrics
        .CreateHistogram("geoapi_http_request_duration_seconds", "HTTP request duration",
            new HistogramConfiguration { LabelNames = new[] { "method", "endpoint" } });

    // Database metrics
    public static readonly Counter DatabaseQueriesTotal = Metrics
        .CreateCounter("geoapi_database_queries_total", "Total database queries",
            new CounterConfiguration { LabelNames = new[] { "operation", "entity" } });

    public static readonly Histogram DatabaseQueryDuration = Metrics
        .CreateHistogram("geoapi_database_query_duration_seconds", "Database query duration",
            new HistogramConfiguration { LabelNames = new[] { "operation", "entity" } });

    // Keycloak metrics
    public static readonly Counter KeycloakRequestsTotal = Metrics
        .CreateCounter("geoapi_keycloak_requests_total", "Total Keycloak requests",
            new CounterConfiguration { LabelNames = new[] { "operation", "status" } });

    // Email metrics
    public static readonly Counter EmailsSentTotal = Metrics
        .CreateCounter("geoapi_emails_sent_total", "Total emails sent",
            new CounterConfiguration { LabelNames = new[] { "template", "status" } });

    // SMS metrics
    public static readonly Counter SmsSentTotal = Metrics
        .CreateCounter("geoapi_sms_sent_total", "Total SMS sent",
            new CounterConfiguration { LabelNames = new[] { "status" } });
}
```

**Middleware para métricas HTTP:**

```csharp
// GEOAPI/src/Gateway/Middleware/MetricsMiddleware.cs

using GEOAPI.Infrastructure.Metrics;

namespace GEOAPI.Gateway.Middleware;

public class MetricsMiddleware
{
    private readonly RequestDelegate _next;

    public MetricsMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        var path = context.Request.Path.Value ?? "/";
        var method = context.Request.Method;

        using (MetricsService.HttpRequestDuration.WithLabels(method, path).NewTimer())
        {
            await _next(context);
        }

        MetricsService.HttpRequestsTotal
            .WithLabels(method, path, context.Response.StatusCode.ToString())
            .Inc();
    }
}
```

**Endpoint de métricas:**

```csharp
app.UseMetricServer(); // Exposes /metrics endpoint for Prometheus
app.UseMiddleware<MetricsMiddleware>();
```

