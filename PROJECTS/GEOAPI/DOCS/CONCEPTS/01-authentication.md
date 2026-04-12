---
type: leaf
status: review
updated: 2026-02-08
---

# Autenticacao - GEOAPI

Implementacao da autenticacao OAuth2/OIDC na GEOAPI usando Keycloak como Identity Provider, com validacao de JWT, mapeamento de claims para multi-tenancy e integracao com Row Level Security do PostgreSQL.

## Visao Geral

A GEOAPI (.NET 8) utiliza OAuth2 com OpenID Connect para autenticar todas as requisicoes. O Keycloak emite JWTs (JSON Web Tokens) que sao validados pelo middleware ASP.NET Core em cada request. O fluxo e stateless: nenhum fluxo de login acontece na API. Todas as aplicacoes cliente (REURBWEB, REURBCAD, REURBMASTER, WEBDOCS, GEOGIS) autenticam o usuario diretamente no Keycloak via Authorization Code com PKCE e enviam o access token resultante no header `Authorization: Bearer {token}`.

```
Cliente (REURBWEB/REURBCAD/ADMIN)
    |
    | Bearer JWT
    v
GEOAPI (.NET 8)
    |
    |-- 1. JWT Validation Middleware (issuer, audience, signature, expiry)
    |-- 2. Claims Mapping (sub, tenant_id, realm_access.roles)
    |-- 3. TenantMiddleware (SET LOCAL app.current_tenant)
    |-- 4. Controller/Handler (logica de negocio)
    |-- 5. PostgreSQL + RLS (filtragem automatica por tenant)
    |
    v
Response (200/401/403)
```

## Integracao com Keycloak

### Discovery Document

A GEOAPI descobre automaticamente os endpoints do Keycloak via OpenID Connect Discovery (`.well-known/openid-configuration`). Nao e necessario configurar manualmente os endpoints de token, JWKS ou userinfo.

```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.Authority = builder.Configuration["Keycloak:Authority"];
        // Ex: https://auth.carf.gov.br/realms/carf

        options.RequireHttpsMetadata = !builder.Environment.IsDevelopment();

        // O middleware busca automaticamente:
        // - {Authority}/.well-known/openid-configuration
        // - JWKS URI para validacao de assinatura
        // - Issuer para validacao
    });
```

### Validacao JWKS

O middleware baixa e cacheia as chaves publicas do Keycloak via endpoint JWKS (JSON Web Key Set). A rotacao de chaves e transparente: quando o Keycloak emite tokens com uma nova chave, o middleware busca automaticamente o JWKS atualizado.

## Validacao de JWT

### Pipeline de Validacao

A validacao JWT ocorre automaticamente para cada request a endpoints protegidos com `[Authorize]`. O middleware valida em sequencia:

1. **Formato**: Token presente no header `Authorization: Bearer {token}` e e um JWT valido (3 partes base64)
2. **Assinatura**: Verificada contra chaves publicas do JWKS (algoritmo RS256)
3. **Issuer**: Deve ser exatamente a URL do realm Keycloak
4. **Audience**: Deve conter `geoapi` na claim `aud`
5. **Expiracao**: Claim `exp` nao ultrapassada (com tolerancia de ClockSkew)
6. **Not Before**: Claim `nbf` ja atingida

### Configuracao Completa

```csharp
// Extensions/AuthenticationExtensions.cs
public static class AuthenticationExtensions
{
    public static IServiceCollection AddKeycloakAuthentication(
        this IServiceCollection services,
        IConfiguration configuration)
    {
        services.AddAuthentication(options =>
        {
            options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
            options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
        })
        .AddJwtBearer(options =>
        {
            var keycloakConfig = configuration.GetSection("Keycloak");

            options.Authority = keycloakConfig["Authority"];
            options.Audience = keycloakConfig["Audience"]; // "geoapi"
            options.RequireHttpsMetadata = keycloakConfig.GetValue<bool>("RequireHttps");

            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuer = true,
                ValidIssuer = keycloakConfig["Authority"],

                ValidateAudience = true,
                ValidAudience = keycloakConfig["Audience"],

                ValidateLifetime = true,
                ClockSkew = TimeSpan.FromSeconds(30),

                ValidateIssuerSigningKey = true,
                // Chaves buscadas automaticamente via JWKS

                NameClaimType = "preferred_username",
                RoleClaimType = "realm_roles",
            };

            options.Events = new JwtBearerEvents
            {
                OnAuthenticationFailed = context =>
                {
                    var logger = context.HttpContext.RequestServices
                        .GetRequiredService<ILogger<Program>>();
                    logger.LogWarning(
                        "Autenticacao falhou: {Error}",
                        context.Exception.Message);
                    return Task.CompletedTask;
                },

                OnTokenValidated = context =>
                {
                    // Mapear claims customizadas do Keycloak
                    MapKeycloakClaims(context.Principal!);
                    return Task.CompletedTask;
                },
            };
        });

        return services;
    }
}
```

## Tabela de Configuracao de Validacao

| Parametro | Valor Producao | Valor Desenvolvimento | Descricao |
|-----------|---------------|----------------------|-----------|
| `ValidateIssuer` | `true` | `true` | Sempre validar emissor do token |
| `ValidIssuer` | `https://auth.carf.gov.br/realms/carf` | `http://localhost:8080/realms/carf` | URL do realm Keycloak |
| `ValidateAudience` | `true` | `true` | Garantir que token e para a GEOAPI |
| `ValidAudience` | `geoapi` | `geoapi` | Client ID da GEOAPI no Keycloak |
| `ValidateLifetime` | `true` | `true` | Rejeitar tokens expirados |
| `ClockSkew` | `00:00:30` | `00:01:00` | Tolerancia de relogio |
| `RequireHttpsMetadata` | `true` | `false` | HTTPS obrigatorio para JWKS |
| `ValidateIssuerSigningKey` | `true` | `true` | Validar assinatura RS256 |
| `RequireExpirationTime` | `true` | `true` | Token deve ter claim `exp` |
| `RequireSignedTokens` | `true` | `true` | Rejeitar tokens nao assinados |

## Mapeamento de Claims

O Keycloak emite claims em formato especifico que precisa ser mapeado para o modelo da GEOAPI.

### Claims do Token Keycloak

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "preferred_username": "maria.silva",
  "email": "maria.silva@carf.gov.br",
  "tenant_id": "tenant-municipio-abc-uuid",
  "allowed_tenants": ["tenant-uuid-1", "tenant-uuid-2"],
  "realm_access": {
    "roles": ["field-coordinator", "field-cadastrator"]
  },
  "community_ids": ["comm-uuid-1", "comm-uuid-2"],
  "iat": 1707400000,
  "exp": 1707400300
}
```

### Mapeamento para Claims .NET

| Claim Keycloak | Claim .NET | Propriedade ICurrentUser | Uso |
|----------------|-----------|--------------------------|-----|
| `sub` | `ClaimTypes.NameIdentifier` | `UserId` | Identificar usuario em audit logs |
| `preferred_username` | `ClaimTypes.Name` | `Username` | Exibicao e logging |
| `email` | `ClaimTypes.Email` | `Email` | Notificacoes |
| `tenant_id` | `"tenant_id"` | `TenantId` | RLS e isolamento |
| `allowed_tenants` | `"allowed_tenants"` | `AllowedTenants` | Super-admin multi-tenant |
| `realm_access.roles` | `ClaimTypes.Role` | `Roles` | RBAC authorization |
| `community_ids` | `"community_ids"` | `CommunityIds` | Acesso por comunidade |

### Codigo de Mapeamento

```csharp
// Helpers/ClaimsMapper.cs
private static void MapKeycloakClaims(ClaimsPrincipal principal)
{
    var identity = (ClaimsIdentity)principal.Identity!;

    // Mapear realm_access.roles para Role claims
    var realmAccess = principal.FindFirst("realm_access");
    if (realmAccess != null)
    {
        var roles = JsonDocument.Parse(realmAccess.Value)
            .RootElement
            .GetProperty("roles")
            .EnumerateArray()
            .Select(r => r.GetString()!);

        foreach (var role in roles)
        {
            identity.AddClaim(new Claim(ClaimTypes.Role, role));
        }
    }

    // Mapear allowed_tenants para claim array
    var allowedTenants = principal.FindFirst("allowed_tenants");
    if (allowedTenants != null)
    {
        var tenants = JsonDocument.Parse(allowedTenants.Value)
            .RootElement
            .EnumerateArray()
            .Select(t => t.GetString()!);

        foreach (var tenant in tenants)
        {
            identity.AddClaim(new Claim("allowed_tenant", tenant));
        }
    }
}
```

## TenantMiddleware

O TenantMiddleware extrai o `tenant_id` do JWT validado e configura a variavel de sessao do PostgreSQL para ativar Row Level Security (RLS).

```csharp
// Middleware/TenantMiddleware.cs
public class TenantMiddleware
{
    private readonly RequestDelegate _next;
    private readonly ILogger<TenantMiddleware> _logger;

    public TenantMiddleware(RequestDelegate next, ILogger<TenantMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context, ITenantProvider tenantProvider)
    {
        if (context.User.Identity?.IsAuthenticated == true)
        {
            var tenantId = context.User.FindFirstValue("tenant_id");

            // Super-admin pode selecionar tenant via header
            if (context.User.IsInRole("super-admin"))
            {
                var headerTenantId = context.Request.Headers["X-Tenant-Id"].FirstOrDefault();
                if (!string.IsNullOrEmpty(headerTenantId))
                {
                    // Validar que o tenant solicitado esta em allowed_tenants
                    var allowed = context.User.FindAll("allowed_tenant")
                        .Select(c => c.Value);
                    if (allowed.Contains(headerTenantId))
                    {
                        tenantId = headerTenantId;
                    }
                }
            }

            if (string.IsNullOrEmpty(tenantId))
            {
                _logger.LogWarning(
                    "Token JWT sem tenant_id para usuario {UserId}",
                    context.User.FindFirstValue(ClaimTypes.NameIdentifier));

                context.Response.StatusCode = 403;
                await context.Response.WriteAsJsonAsync(new
                {
                    error = "forbidden",
                    message = "Token nao contem tenant_id"
                });
                return;
            }

            // Definir tenant no provider (scoped per request)
            tenantProvider.SetTenant(Guid.Parse(tenantId));

            // A variavel de sessao PostgreSQL sera definida pelo TenantInterceptor
            // no momento da abertura da conexao com o banco
        }

        await _next(context);
    }
}
```

### Configuracao RLS via DbContext Interceptor

```csharp
// Persistence/Interceptors/TenantInterceptor.cs
public class TenantInterceptor : DbConnectionInterceptor
{
    private readonly ITenantProvider _tenantProvider;

    public TenantInterceptor(ITenantProvider tenantProvider)
    {
        _tenantProvider = tenantProvider;
    }

    public override async Task ConnectionOpenedAsync(
        DbConnection connection,
        ConnectionEndEventData eventData,
        CancellationToken cancellationToken = default)
    {
        if (_tenantProvider.HasTenant)
        {
            await using var cmd = connection.CreateCommand();
            cmd.CommandText = $"SET LOCAL app.current_tenant = '{_tenantProvider.TenantId}'";
            await cmd.ExecuteNonQueryAsync(cancellationToken);
        }
    }
}
```

## Fluxo Multi-Tenant Completo

```
1. Request chega com Bearer JWT
   |
2. JwtBearerMiddleware valida token
   |-- Invalido → 401 Unauthorized
   |-- Valido → continua
   |
3. Claims mapeadas (sub, tenant_id, roles, community_ids)
   |
4. TenantMiddleware extrai tenant_id
   |-- Ausente → 403 Forbidden
   |-- Super-admin com X-Tenant-Id → validar contra allowed_tenants
   |-- Presente → SET LOCAL app.current_tenant
   |
5. Authorization ([Authorize(Roles = "...")])
   |-- Role insuficiente → 403 Forbidden
   |-- Role valida → continua
   |
6. Handler processa logica de negocio
   |
7. PostgreSQL RLS filtra automaticamente por tenant
   |-- SELECT: retorna apenas dados do tenant
   |-- INSERT: valida tenant_id no WITH CHECK
   |
8. Response retorna ao cliente
```

## Fluxos por Aplicacao

REURBWEB, REURBMASTER e WEBDOCS usam Authorization Code com PKCE (S256) como clients publicos, redirecionando para Keycloak e recebendo tokens via browser redirect. Access token expira em 5 minutos com refresh silencioso via refresh token.

REURBCAD (mobile) usa Authorization Code com PKCE via custom URL scheme `carf://callback`, com scope `offline_access` para obter refresh token de 30 dias que permite operacao em campo sem internet. Tokens sao armazenados em secure storage nativo (Keychain iOS, EncryptedSharedPreferences Android).

GEOGIS (plugin QGIS) usa Authorization Code com PKCE como client confidential, com servidor HTTP local temporario para capturar callback. Apos login no Keycloak, o analista informa uma Authentication Key (chave adicional gerenciada pela GEOAPI que vincula a sessao do plugin ao backend e habilita acesso as ortofotos do tenant).

## Token Lifetimes

| Token | Duracao | Proposito |
|-------|---------|-----------|
| Access token | 5 minutos | Autorizacao por requisicao, stateless |
| Refresh token (web) | SSO idle 30min, max 10h | Renovacao silenciosa sem re-login |
| Refresh token (remember me) | Idle 1 dia, max 7 dias | Sessao estendida com checkbox |
| Offline token (REURBCAD) | Idle 30 dias | Operacao em campo sem conectividade |

Refresh token rotation esta habilitada com max reuse zero: cada refresh token so pode ser usado uma vez, invalidando o anterior. Uso simultaneo do mesmo refresh token por usuario legitimo e atacante causa revogacao de ambos, detectando comprometimento.

## Respostas de Erro

### 401 Unauthorized

Retornado quando o token JWT e ausente, malformado, expirado ou com assinatura invalida.

```json
{
  "type": "https://httpstatuses.com/401",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Token de autenticacao ausente ou invalido",
  "traceId": "00-abc123-def456-00"
}
```

| Cenario | Header WWW-Authenticate |
|---------|------------------------|
| Token ausente | `Bearer` |
| Token expirado | `Bearer error="invalid_token", error_description="The token expired"` |
| Assinatura invalida | `Bearer error="invalid_token", error_description="The signature key was not found"` |
| Issuer invalido | `Bearer error="invalid_token", error_description="The issuer is invalid"` |

### 403 Forbidden

Retornado quando o token e valido mas o usuario nao tem permissao para o recurso.

```json
{
  "type": "https://httpstatuses.com/403",
  "title": "Forbidden",
  "status": 403,
  "detail": "Voce nao tem permissao para acessar este recurso",
  "requiredRoles": ["manager", "admin", "super-admin"],
  "userRoles": ["field-cadastrator"],
  "traceId": "00-abc123-def456-00"
}
```

## Registro no Pipeline

```csharp
// Program.cs - Ordem do pipeline
var app = builder.Build();

app.UseHttpsRedirection();
app.UseCors();

// 1. Autenticacao: valida JWT
app.UseAuthentication();

// 2. Autorizacao: verifica roles
app.UseAuthorization();

// 3. Tenant: extrai tenant_id e configura RLS
app.UseMiddleware<TenantMiddleware>();

// 4. Audit: registra acoes em audit_logs
app.UseMiddleware<AuditMiddleware>();

app.MapControllers();
```

## Referencias

- [02-authorization.md](./02-authorization.md) - RBAC e permissoes por role
- [ARCHITECTURE/02-admin-security.md](../ARCHITECTURE/02-admin-security.md) - Seguranca dos endpoints admin
- [ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/03-rls-setup.md](../ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/03-rls-setup.md) - Configuracao RLS PostgreSQL
- [ARCHITECTURE/LAYERS/PRESENTATION/MIDDLEWARES/01-exception-handling.md](../ARCHITECTURE/LAYERS/PRESENTATION/MIDDLEWARES/01-exception-handling.md) - Tratamento de erros
- [KEYCLOAK/DOCS/INTEGRATION/TOKENS/01-access-token.md](../../../KEYCLOAK/DOCS/INTEGRATION/TOKENS/01-access-token.md) - Estrutura do token
- [KEYCLOAK/DOCS/INTEGRATION/TOKENS/03-validation.md](../../../KEYCLOAK/DOCS/INTEGRATION/TOKENS/03-validation.md) - Validacao de tokens no Keycloak
- [CENTRAL/ARCHITECTURE/INTEGRATION/01-authentication.md](../../../../CENTRAL/ARCHITECTURE/INTEGRATION/01-authentication.md) - Integracao de autenticacao CARF
