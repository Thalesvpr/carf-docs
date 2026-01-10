# Arquitetura de Segurança - Endpoints Admin

## Visão Geral

Os endpoints `/api/admin/*` do GEOAPI implementam **7 camadas de segurança** conforme [Security Guidelines CENTRAL](../../../../CENTRAL/SECURITY/README.md) para proteger operações administrativas sensíveis (gerenciamento de tenants, usuários, e configurações do sistema) consumidas pelo [ADMIN Console](../../../ADMIN/DOCS/ARCHITECTURE/README.md).

## Por que não Next.js para Admin?

A decisão de **NÃO usar Next.js** para o console administrativo foi tomada por segurança:

### Problema com Next.js

```
❌ Next.js Admin Console
   ↓
   API Routes (/api/keycloak/*)
   ↓
   Keycloak Admin Client API
   - Requer client_secret confidencial
   - Secrets em Next.js podem vazar:
     * Bundled no client-side acidentalmente
     * Expostos em environment variables do browser
     * Vulnerável a XSS se mal configurado
```

### Solução Segura: SPA + Backend API

```
✅ carf-admin (SPA React + Vite)
   ↓ PKCE flow (sem client_secret)
   ↓ HTTPS + Bearer Token

   carf-geoapi (Backend .NET 9)
   ↓ /api/admin/* endpoints
   ↓ Keycloak Admin Client (confidential)
   ↓ client_secret isolado no backend

   Keycloak Admin API
```

**Benefícios:**
- ✅ `client_secret` **nunca sai do backend**
- ✅ Frontend usa PKCE (public client seguro)
- ✅ Tokens com expiração curta (5 min)
- ✅ Backend .NET oferece melhor isolamento

## Arquitetura dos Endpoints Admin

### Estrutura no GEOAPI

```
src/
├── Gateway/
│   └── Controllers/
│       └── AdminController.cs        # Endpoints /api/admin/*
│
├── Application/
│   └── Admin/
│       ├── Commands/
│       │   ├── CreateTenantCommand.cs
│       │   ├── CreateUserCommand.cs
│       │   └── AssignRolesCommand.cs
│       └── Queries/
│           ├── GetTenantsQuery.cs
│           └── GetUsersQuery.cs
│
└── Infrastructure/
    └── Keycloak/
        ├── KeycloakAdminService.cs   # Wrapper Keycloak Admin Client
        └── KeycloakAdminConfig.cs    # Configuração confidencial
```

### Fluxo de Requisição

```
1. carf-admin (SPA)
   ↓ POST /api/admin/users
   ↓ Authorization: Bearer <JWT token>

2. AdminController [Authorize(Roles = "super-admin,admin")]
   ↓ Valida token JWT (Keycloak)
   ↓ Valida role (super-admin ou admin)
   ↓ Valida tenant (admin só vê próprio tenant)

3. MediatR Handler
   ↓ CreateUserCommand
   ↓ FluentValidation (valida DTO)

4. KeycloakAdminService
   ↓ Usa client_secret confidencial
   ↓ POST /admin/realms/carf/users (Keycloak Admin API)

5. Response → carf-admin
   ↓ Auditoria registrada (AdminActionLogger)
```

## 7 Camadas de Segurança

### 1. Autenticação OAuth2

Todos os endpoints requerem JWT válido do Keycloak.

```csharp
[ApiController]
[Route("api/admin")]
[Authorize]  // ← Camada 1: Requer autenticação
public class AdminController : ControllerBase
{
    // ...
}
```

**O que valida:**
- Token assinado corretamente (RS256)
- Token não expirado (exp claim)
- Issuer correto (Keycloak realm)
- Audience correto (geoapi)

### 2. Autorização por Roles

Operações admin restritas a roles específicas.

```csharp
[HttpPost("tenants")]
[Authorize(Roles = "super-admin")]  // ← Camada 2: Apenas super-admin
public async Task<IActionResult> CreateTenant(CreateTenantDto dto)
{
    var command = new CreateTenantCommand(dto);
    var result = await _mediator.Send(command);
    return Ok(result);
}

[HttpGet("users")]
[Authorize(Roles = "super-admin,admin")]  // ← super-admin OU admin
public async Task<IActionResult> GetUsers([FromQuery] GetUsersQuery query)
{
    var result = await _mediator.Send(query);
    return Ok(result);
}
```

**Hierarquia de Roles:**
- `super-admin`: Acesso total a todos tenants
- `admin`: Acesso apenas ao próprio tenant
- `analyst`, `field-collector`: **Sem acesso** a /api/admin/*

### 3. Validação de Tenant (RLS)

Admins só podem gerenciar recursos do próprio tenant.

```csharp
public class CreateUserHandler : IRequestHandler<CreateUserCommand, int>
{
    public async Task<int> Handle(CreateUserCommand request, CancellationToken ct)
    {
        // Camada 3: Validação de tenant
        if (!User.IsInRole("super-admin"))
        {
            // Admins regulares só podem criar usuários no próprio tenant
            if (request.TenantId != User.GetTenantId())
            {
                throw new ForbiddenException("Você não tem permissão para criar usuários em outro tenant.");
            }
        }

        // super-admin pode criar usuários em qualquer tenant
        var userId = await _keycloakAdminService.CreateUserAsync(request);
        return userId;
    }
}
```

**Exemplos:**

| User Role | User Tenant | Request Tenant | Resultado |
|-----------|-------------|----------------|-----------|
| `super-admin` | prefeitura-sp | prefeitura-rio | ✅ Permitido |
| `admin` | prefeitura-sp | prefeitura-sp | ✅ Permitido |
| `admin` | prefeitura-sp | prefeitura-rio | ❌ **403 Forbidden** |
| `analyst` | prefeitura-sp | prefeitura-sp | ❌ **403 Forbidden** (role insuficiente) |

### 4. Rate Limiting

Proteção contra brute force e DDoS.

```csharp
// Program.cs
builder.Services.AddRateLimiter(options =>
{
    options.AddPolicy("admin-policy", httpContext =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: httpContext.Connection.RemoteIpAddress?.ToString(),
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 100,        // 100 requisições
                Window = TimeSpan.FromMinutes(1),  // por minuto
                QueueProcessingOrder = QueueProcessingOrder.OldestFirst,
                QueueLimit = 10
            }
        )
    );
});

// AdminController.cs
[EnableRateLimiting("admin-policy")]  // ← Camada 4: Rate limit
public class AdminController : ControllerBase
{
    // ...
}
```

**Configurações:**
- 100 requisições/minuto por IP
- Fila de 10 requisições adicionais
- Resposta: `429 Too Many Requests`

### 5. CORS Restrito

Apenas origens autorizadas podem acessar os endpoints.

```csharp
// Program.cs
builder.Services.AddCors(options =>
{
    options.AddPolicy("AdminPolicy", policy =>
    {
        policy
            .WithOrigins(
                "https://admin.carf.example.com",      // Produção
                "http://localhost:5174"                 // Desenvolvimento
            )
            .AllowCredentials()
            .WithMethods("GET", "POST", "PUT", "DELETE")
            .WithHeaders("Authorization", "Content-Type")
            .SetPreflightMaxAge(TimeSpan.FromHours(1));
    });
});

// Aplicar na pipeline
app.UseCors("AdminPolicy");  // ← Camada 5: CORS
```

**Segurança:**
- ✅ Impede requisições de origens desconhecidas
- ✅ Preflight cache (1h) reduz overhead
- ✅ Apenas métodos HTTP necessários

### 6. Auditoria Completa

Todas as ações admin são registradas para [auditoria](../CONCEPTS/04-audit-logging.md) conforme políticas de compliance.

```csharp
// Middleware: AdminAuditMiddleware.cs
public class AdminAuditMiddleware
{
    public async Task InvokeAsync(HttpContext context)
    {
        // Captura requisição
        var request = await CaptureRequestAsync(context.Request);

        // Executa action
        await _next(context);

        // Captura resposta
        var response = await CaptureResponseAsync(context.Response);

        // Registra auditoria (Camada 6)
        if (context.Request.Path.StartsWithSegments("/api/admin"))
        {
            await _auditLogger.LogAsync(new AdminAuditLog
            {
                UserId = context.User.GetUserId(),
                Username = context.User.GetUsername(),
                TenantId = context.User.GetTenantId(),
                Action = GetActionName(context.Request.Method, context.Request.Path),
                Resource = context.Request.Path,
                RequestBody = request,
                ResponseStatus = context.Response.StatusCode,
                IpAddress = context.Connection.RemoteIpAddress?.ToString(),
                UserAgent = context.Request.Headers["User-Agent"],
                Timestamp = DateTime.UtcNow
            });
        }
    }
}
```

**Informações Registradas:**
- Quem (user_id, username, tenant_id)
- Quando (timestamp UTC)
- O quê (action, resource, changes)
- Como (request body, response status)
- De onde (IP, User-Agent)

**Exemplo de Log:**
```json
{
  "userId": "abc-123",
  "username": "admin@prefeitura-sp.gov.br",
  "tenantId": "prefeitura-sp",
  "action": "CREATE_USER",
  "resource": "/api/admin/users",
  "requestBody": {
    "email": "user@example.com",
    "roles": ["analyst"],
    "tenantId": "prefeitura-sp"
  },
  "responseStatus": 201,
  "ipAddress": "192.168.1.100",
  "timestamp": "2026-01-09T12:30:45Z"
}
```

### 7. Keycloak Admin Client (Confidential)

Client secret isolado no backend, nunca exposto.

```csharp
// appsettings.json (backend APENAS)
{
  "KeycloakAdmin": {
    "ServerUrl": "http://keycloak:8080",
    "Realm": "carf",
    "ClientId": "admin-backend",
    "ClientSecret": "***CONFIDENTIAL_SECRET***",  // ← Camada 7: Isolado
    "GrantType": "client_credentials"
  }
}

// KeycloakAdminService.cs
public class KeycloakAdminService
{
    private readonly KeycloakAdminConfig _config;

    public KeycloakAdminService(IOptions<KeycloakAdminConfig> config)
    {
        _config = config.Value;
    }

    private async Task<string> GetAdminTokenAsync()
    {
        // Client Credentials flow (confidential)
        var request = new HttpRequestMessage(HttpMethod.Post,
            $"{_config.ServerUrl}/realms/{_config.Realm}/protocol/openid-connect/token");

        request.Content = new FormUrlEncodedContent(new Dictionary<string, string>
        {
            ["grant_type"] = "client_credentials",
            ["client_id"] = _config.ClientId,
            ["client_secret"] = _config.ClientSecret  // ← Backend APENAS
        });

        var response = await _httpClient.SendAsync(request);
        var token = await response.Content.ReadFromJsonAsync<TokenResponse>();
        return token.AccessToken;
    }

    public async Task<string> CreateUserAsync(CreateUserRequest request)
    {
        var adminToken = await GetAdminTokenAsync();

        var httpRequest = new HttpRequestMessage(HttpMethod.Post,
            $"{_config.ServerUrl}/admin/realms/{_config.Realm}/users");

        httpRequest.Headers.Authorization = new AuthenticationHeaderValue("Bearer", adminToken);
        httpRequest.Content = JsonContent.Create(request);

        var response = await _httpClient.SendAsync(httpRequest);
        response.EnsureSuccessStatusCode();

        // Extrair user ID da resposta
        var location = response.Headers.Location;
        var userId = location?.Segments.Last();
        return userId;
    }
}
```

**Segurança:**
- ✅ Secret em `appsettings.json` (nunca em código)
- ✅ Em produção: variável de ambiente ou Azure Key Vault
- ✅ Token admin válido por 5 minutos
- ✅ Token admin não compartilhado com frontend

## Endpoints Disponíveis

### Gerenciamento de Tenants

```csharp
[HttpGet("tenants")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> GetTenants([FromQuery] GetTenantsQuery query);

[HttpPost("tenants")]
[Authorize(Roles = "super-admin")]
public async Task<IActionResult> CreateTenant(CreateTenantDto dto);

[HttpPut("tenants/{id}")]
[Authorize(Roles = "super-admin")]
public async Task<IActionResult> UpdateTenant(Guid id, UpdateTenantDto dto);

[HttpDelete("tenants/{id}")]
[Authorize(Roles = "super-admin")]
public async Task<IActionResult> DeactivateTenant(Guid id);
```

### Gerenciamento de Usuários

```csharp
[HttpGet("users")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> GetUsers([FromQuery] GetUsersQuery query);

[HttpPost("users")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> CreateUser(CreateUserDto dto);

[HttpPut("users/{id}")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> UpdateUser(string id, UpdateUserDto dto);

[HttpPut("users/{id}/roles")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> AssignRoles(string id, AssignRolesDto dto);

[HttpPut("users/{id}/tenants")]
[Authorize(Roles = "super-admin")]
public async Task<IActionResult> AssignTenants(string id, AssignTenantsDto dto);

[HttpPost("users/{id}/reset-password")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> ResetPassword(string id);
```

### Auditoria

```csharp
[HttpGet("audit")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> GetAuditLogs([FromQuery] GetAuditLogsQuery query);

[HttpGet("audit/users/{userId}")]
[Authorize(Roles = "super-admin,admin")]
public async Task<IActionResult> GetUserAuditLogs(string userId);

[HttpGet("audit/tenants/{tenantId}")]
[Authorize(Roles = "super-admin")]
public async Task<IActionResult> GetTenantAuditLogs(Guid tenantId);
```

## Configuração em Produção

### 1. HTTPS Obrigatório

```csharp
// Program.cs
if (app.Environment.IsProduction())
{
    app.UseHsts();  // HTTP Strict Transport Security
    app.UseHttpsRedirection();
}
```

### 2. Secrets no Azure Key Vault

```csharp
// Program.cs
if (app.Environment.IsProduction())
{
    builder.Configuration.AddAzureKeyVault(
        new Uri($"https://{keyVaultName}.vault.azure.net/"),
        new DefaultAzureCredential()
    );
}
```

### 3. Logging com Serilog

```csharp
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .WriteTo.Console()
    .WriteTo.File("logs/admin-.txt", rollingInterval: RollingInterval.Day)
    .WriteTo.ApplicationInsights(telemetryConfiguration, TelemetryConverter.Traces)
    .CreateLogger();
```

## Checklist de Segurança

### Backend (GEOAPI)

- ✅ Endpoints protegidos com `[Authorize]`
- ✅ Roles validadas com `[Authorize(Roles = "...")]`
- ✅ Tenant validation em handlers
- ✅ Rate limiting habilitado
- ✅ CORS restrito a origens conhecidas
- ✅ Auditoria de todas ações admin
- ✅ Keycloak Admin Client configurado como confidential
- ✅ Client secret em Key Vault (produção)
- ✅ HTTPS obrigatório em produção
- ✅ Tokens com expiração curta (5 min)
- ✅ Logging estruturado (Serilog + Application Insights)

### Frontend (carf-admin)

- ✅ Autenticação via Keycloak PKCE flow
- ✅ Sem client_secret no código
- ✅ Tokens armazenados em memória (não localStorage)
- ✅ Refresh automático de tokens (< 60s expiry)
- ✅ Logout limpa sessão Keycloak (SSO logout)
- ✅ Validação de roles no UI (esconder ações não permitidas)
- ✅ HTTPS obrigatório em produção
- ✅ CSP (Content Security Policy) headers

## Testes de Segurança

### 1. Testes de Autorização

```csharp
[Fact]
public async Task CreateTenant_WithAdminRole_ReturnsForbidden()
{
    // Arrange
    var token = GenerateToken(roles: ["admin"]);  // Admin comum (não super-admin)
    _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

    // Act
    var response = await _client.PostAsJsonAsync("/api/admin/tenants", new CreateTenantDto
    {
        Name = "Prefeitura Teste"
    });

    // Assert
    Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
}
```

### 2. Testes de Isolamento de Tenant

```csharp
[Fact]
public async Task GetUsers_AdminFromTenant1_CannotSeeUsersFromTenant2()
{
    // Arrange
    var token = GenerateToken(roles: ["admin"], tenantId: "tenant-1");
    _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

    // Act
    var response = await _client.GetAsync("/api/admin/users?tenantId=tenant-2");

    // Assert
    Assert.Equal(HttpStatusCode.Forbidden, response.StatusCode);
}
```

### 3. Testes de Rate Limiting

```csharp
[Fact]
public async Task AdminEndpoints_ExceedRateLimit_Returns429()
{
    // Arrange
    var token = GenerateToken(roles: ["super-admin"]);
    _client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);

    // Act - Fazer 101 requisições (limite é 100/min)
    var responses = new List<HttpResponseMessage>();
    for (int i = 0; i < 101; i++)
    {
        responses.Add(await _client.GetAsync("/api/admin/tenants"));
    }

    // Assert
    Assert.Equal(HttpStatusCode.TooManyRequests, responses.Last().StatusCode);
}
```
