# Keycloak Integration

Integração com Keycloak para autenticação OAuth2/OIDC.

## Configuração

```csharp
// appsettings.json
{
  "Keycloak": {
    "Authority": "https://keycloak.carf.com.br/realms/carf",
    "Audience": "carf-api",
    "ClientId": "carf-api",
    "ClientSecret": "***"
  }
}

// Program.cs
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = keycloakOptions.Authority;
        options.Audience = keycloakOptions.Audience;
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });
```

## IKeycloakService

```csharp
public interface IKeycloakService
{
    Task<TokenResponse> LoginAsync(string username, string password, Guid? tenantId, CancellationToken ct);
    Task<TokenResponse> RefreshTokenAsync(string refreshToken, CancellationToken ct);
    Task RevokeTokenAsync(string refreshToken, CancellationToken ct);
    Task<UserInfo> GetUserInfoAsync(string accessToken, CancellationToken ct);
}
```

## KeycloakService

```csharp
public class KeycloakService : IKeycloakService
{
    private readonly HttpClient _httpClient;
    private readonly KeycloakOptions _options;

    public async Task<TokenResponse> LoginAsync(string username, string password, Guid? tenantId, CancellationToken ct)
    {
        var tokenEndpoint = $"{_options.Authority}/protocol/openid-connect/token";

        var form = new Dictionary<string, string>
        {
            ["grant_type"] = "password",
            ["client_id"] = _options.ClientId,
            ["client_secret"] = _options.ClientSecret,
            ["username"] = username,
            ["password"] = password,
            ["scope"] = "openid profile email"
        };

        var response = await _httpClient.PostAsync(tokenEndpoint,
            new FormUrlEncodedContent(form), ct);

        if (!response.IsSuccessStatusCode)
        {
            var error = await response.Content.ReadFromJsonAsync<KeycloakError>(ct);
            throw new AuthenticationException(error.ErrorDescription);
        }

        return await response.Content.ReadFromJsonAsync<TokenResponse>(ct);
    }

    public async Task RevokeTokenAsync(string refreshToken, CancellationToken ct)
    {
        var revokeEndpoint = $"{_options.Authority}/protocol/openid-connect/revoke";

        var form = new Dictionary<string, string>
        {
            ["token"] = refreshToken,
            ["token_type_hint"] = "refresh_token",
            ["client_id"] = _options.ClientId,
            ["client_secret"] = _options.ClientSecret
        };

        await _httpClient.PostAsync(revokeEndpoint,
            new FormUrlEncodedContent(form), ct);
    }
}
```

## Extração de Claims

```csharp
public class TenantContext : ITenantContext
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public Guid TenantId => GetClaimValue<Guid>("tenant_id");
    public Guid UserId => GetClaimValue<Guid>(ClaimTypes.NameIdentifier);
    public string Email => GetClaimValue<string>(ClaimTypes.Email);
    public IEnumerable<string> Roles => GetClaimValues("roles");

    private T GetClaimValue<T>(string claimType)
    {
        var claim = _httpContextAccessor.HttpContext?.User.FindFirst(claimType);
        return claim != null ? (T)Convert.ChangeType(claim.Value, typeof(T)) : default;
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
