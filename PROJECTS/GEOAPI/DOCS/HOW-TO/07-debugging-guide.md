---
type: leaf
status: review
updated: 2026-02-08
---

# Guia de Debugging - GEOAPI

Como depurar o GEOAPI localmente utilizando diferentes IDEs, configurar logging estruturado, analisar queries EF Core e realizar profiling de performance.

---

## Debugging por IDE

### JetBrains Rider

#### Configurar Run/Debug

1. Menu **Run → Edit Configurations**
2. Clicar **+** → **.NET Project**
3. Configurar:

| Campo | Valor |
|-------|-------|
| Name | `GEOAPI Debug` |
| Project | `Carf.GeoApi.Gateway` |
| Target framework | `net9.0` |
| Environment variables | `ASPNETCORE_ENVIRONMENT=Development` |
| Working directory | `src/Carf.GeoApi.Gateway` |
| Launch browser | `https://localhost:7001/swagger` |

4. Clicar **Apply** → **OK**

#### Breakpoints

- Clicar na margem esquerda do editor (ou `Ctrl+F8`) para adicionar breakpoint
- **Breakpoint condicional:** Clicar com botao direito no breakpoint → "More" → preencher condicao (ex: `request.Id == specificGuid`)
- **Logpoint (sem parar):** Clicar com botao direito → marcar "Log message" → escrever mensagem (ex: `"Handler called with {request.FullName}"`)

#### Breakpoints recomendados

| Local | Proposito |
|-------|-----------|
| Inicio do `Handle()` em qualquer CommandHandler | Ver command recebido |
| Metodos de dominio nas Entities (ex: `UpdatePhoneNumber`) | Ver estado da entity antes/depois |
| `AppDbContext.SaveChangesAsync()` | Ver change tracker |
| `ExceptionHandlingMiddleware.InvokeAsync()` | Ver exceptions antes de serem formatadas |
| `TenantMiddleware.InvokeAsync()` | Ver tenant resolution |

#### Watch Variables

No painel "Variables" durante debugging:
- `_context.ChangeTracker.Entries()` - Ver entities rastreadas e seus estados
- `request` - Payload completo do command/query
- `HttpContext.User.Claims` - Claims do JWT do usuario autenticado

#### Evaluate Expression

No painel "Evaluate" (`Alt+F8`):
- `_context.Database.GetConnectionString()` - Connection string ativa
- `holder.DomainEvents` - Eventos de dominio pendentes
- `JsonSerializer.Serialize(result)` - Serializar resultado para inspecao

---

### Visual Studio 2022

#### Configurar Debug

1. Clicar com botao direito em `Carf.GeoApi.Gateway` → **Set as Startup Project**
2. Verificar perfil de lancamento em `Properties/launchSettings.json`:

```json
{
  "profiles": {
    "Carf.GeoApi.Gateway": {
      "commandName": "Project",
      "dotnetRunMessages": true,
      "launchBrowser": true,
      "launchUrl": "swagger",
      "applicationUrl": "https://localhost:7001;http://localhost:5001",
      "environmentVariables": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  }
}
```

3. Pressionar **F5** para iniciar com debugger

#### Breakpoints Avancados

- **Breakpoint condicional:** Clicar com botao direito no breakpoint → Conditions → `request.PhoneNumber != null`
- **Hit count:** Pausar somente na N-esima execucao → Conditions → Hit Count → `= 5`
- **Tracepoint:** Actions → marcar "Log a message" → `{request.Id} - {DateTime.Now}` → continuar execucao

#### Attach to Process

Se a API ja esta rodando (via `dotnet run`):
1. **Debug → Attach to Process** (`Ctrl+Alt+P`)
2. Filtrar por `dotnet` ou `Carf.GeoApi.Gateway`
3. Selecionar o processo → **Attach**

#### Janelas Uteis

| Janela | Atalho | Uso |
|--------|--------|-----|
| Locals | Auto | Variaveis locais do scope atual |
| Watch | `Ctrl+Alt+W, 1` | Monitorar expressoes especificas |
| Call Stack | `Ctrl+Alt+C` | Ver pilha de chamadas (MediatR pipeline) |
| Immediate | `Ctrl+Alt+I` | Executar expressoes durante pausa |
| Output | `Ctrl+Alt+O` | Ver logs da aplicacao |
| Diagnostic Tools | Auto | CPU/memoria em tempo real |

---

### VS Code

#### Configurar launch.json

**Arquivo:** `.vscode/launch.json`

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch GEOAPI",
      "type": "coreclr",
      "request": "launch",
      "preLaunchTask": "build",
      "program": "${workspaceFolder}/src/Carf.GeoApi.Gateway/bin/Debug/net9.0/Carf.GeoApi.Gateway.dll",
      "args": [],
      "cwd": "${workspaceFolder}/src/Carf.GeoApi.Gateway",
      "stopAtEntry": false,
      "env": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      },
      "sourceFileMap": {
        "/Views": "${workspaceFolder}/Views"
      }
    },
    {
      "name": "Attach to GEOAPI",
      "type": "coreclr",
      "request": "attach",
      "processId": "${command:pickProcess}"
    }
  ]
}
```

#### Configurar tasks.json

**Arquivo:** `.vscode/tasks.json`

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build",
      "command": "dotnet",
      "type": "process",
      "args": [
        "build",
        "${workspaceFolder}/Carf.GeoApi.sln",
        "/property:GenerateFullPaths=true",
        "/consoleloggerparameters:NoSummary"
      ],
      "problemMatcher": "$msCompile"
    }
  ]
}
```

#### Debugging

- **F5** para iniciar debug
- Breakpoints clicando na margem esquerda
- **Conditional breakpoint:** Clicar com botao direito na margem → "Add Conditional Breakpoint"
- **Debug Console** (`Ctrl+Shift+Y`) para avaliar expressoes

---

## Logging Estruturado (Serilog)

### Configuracao de Log Levels

O GEOAPI utiliza Serilog para logging estruturado. Os niveis sao configurados em `appsettings.json`:

```json
{
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft.AspNetCore": "Warning",
        "Microsoft.EntityFrameworkCore": "Warning",
        "Microsoft.EntityFrameworkCore.Database.Command": "Information",
        "Hangfire": "Warning",
        "System.Net.Http": "Warning",
        "Carf.GeoApi.Application": "Debug",
        "Carf.GeoApi.Domain": "Debug",
        "Carf.GeoApi.Infrastructure.Persistence": "Debug"
      }
    },
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "outputTemplate": "[{Timestamp:HH:mm:ss} {Level:u3}] {SourceContext} | {Message:lj}{NewLine}{Exception}"
        }
      },
      {
        "Name": "File",
        "Args": {
          "path": "logs/geoapi-.log",
          "rollingInterval": "Day",
          "retainedFileCountLimit": 7,
          "formatter": "Serilog.Formatting.Compact.CompactJsonFormatter, Serilog.Formatting.Compact"
        }
      }
    ],
    "Enrich": ["FromLogContext", "WithMachineName", "WithThreadId"]
  }
}
```

### Hierarquia de Log Levels

| Level | Uso | Exemplos |
|-------|-----|----------|
| `Verbose` | Trace detalhado (raramente usado) | Cada iteracao de loop, bytes transferidos |
| `Debug` | Informacao de debugging | Query parameters, entity state changes |
| `Information` | Fluxo normal da aplicacao | Request recebido, command processado, migration aplicada |
| `Warning` | Situacao anormal mas recuperavel | Cache miss, retry de operacao, token proximo de expirar |
| `Error` | Erro que impede operacao especifica | Exception em handler, falha de persistencia, timeout |
| `Fatal` | Erro que impede aplicacao de continuar | Banco inacessivel, configuracao critica faltando |

### Alterar nivel em runtime (sem restart)

Modificar `appsettings.Development.json` e salvar. Com `reloadOnChange: true` (padrao), o Serilog recarrega automaticamente.

Para debugging temporario de EF Core queries:

```json
"Override": {
  "Microsoft.EntityFrameworkCore.Database.Command": "Debug"
}
```

---

## Leitura de Logs JSON

### Formato dos logs em arquivo (CompactJsonFormatter)

```json
{"@t":"2024-03-15T14:30:00.123Z","@mt":"Processing {CommandName} for {EntityId}","@l":"Information","CommandName":"UpdateHolderCommand","EntityId":"abc-123","CorrelationId":"req-456","SourceContext":"Carf.GeoApi.Application.Commands.Holders.UpdateHolderCommandHandler","RequestPath":"/api/v1/holders/abc-123","UserId":"user-789","TenantId":"tenant-001"}
```

### Filtrar logs por CorrelationId

```bash
# Linux/macOS
cat logs/geoapi-20240315.log | jq 'select(.CorrelationId == "req-456")'

# Windows (PowerShell)
Get-Content logs\geoapi-20240315.log | ForEach-Object { $_ | ConvertFrom-Json } | Where-Object { $_.CorrelationId -eq "req-456" }
```

### Filtrar por level

```bash
cat logs/geoapi-20240315.log | jq 'select(."@l" == "Error")'
```

### Filtrar por path

```bash
cat logs/geoapi-20240315.log | jq 'select(.RequestPath | test("/api/v1/holders"))'
```

### Propriedades de contexto disponiveis

| Propriedade | Descricao | Exemplo |
|-------------|-----------|---------|
| `@t` | Timestamp UTC | `2024-03-15T14:30:00.123Z` |
| `@l` | Log level | `Information`, `Error` |
| `@mt` | Message template | `Processing {CommandName}` |
| `@x` | Exception (se houver) | Stack trace completo |
| `CorrelationId` | ID unico da request HTTP | `req-456-abc` |
| `RequestPath` | Path da request | `/api/v1/holders/abc-123` |
| `RequestMethod` | Metodo HTTP | `PUT` |
| `UserId` | ID do usuario autenticado | `user-789` |
| `TenantId` | ID do tenant (via RLS) | `tenant-001` |
| `SourceContext` | Namespace do logger | `Carf.GeoApi.Application...` |
| `ElapsedMilliseconds` | Tempo de processamento | `145` |

---

## EF Core Query Logging

### Habilitar log de queries SQL

Em `appsettings.Development.json`:

```json
"Override": {
  "Microsoft.EntityFrameworkCore.Database.Command": "Information"
}
```

Output no console:

```
[14:30:00 INF] Microsoft.EntityFrameworkCore.Database.Command |
  Executed DbCommand (3ms) [Parameters=[@p0='abc-123'], CommandType='Text', CommandTimeout='30']
  SELECT h."Id", h."full_name", h."cpf", h."phone_number", h."tenant_id"
  FROM "holders" AS h
  WHERE h."Id" = @p0 AND h."tenant_id" = current_setting('app.current_tenant')::uuid
  LIMIT 1
```

### Habilitar dados sensiveis nos logs (apenas dev)

```csharp
// Em AppDbContext ou na configuracao do DbContext
optionsBuilder.EnableSensitiveDataLogging();  // Mostra valores dos parametros
optionsBuilder.EnableDetailedErrors();         // Stack traces detalhados
```

> **NUNCA habilitar em producao** - expoe dados de usuarios nos logs.

### Query Tags para rastreabilidade

```csharp
// No repository ou query handler
var holders = await _context.Holders
    .TagWith("GetHoldersByCommunity - HolderQueryHandler")
    .Where(h => h.CommunityId == communityId)
    .ToListAsync(ct);
```

Aparece no log SQL como comentario:

```sql
-- GetHoldersByCommunity - HolderQueryHandler
SELECT h."Id", h."full_name" ...
```

---

## Performance Profiling

### MiniProfiler para Queries EF Core

#### Configuracao

```csharp
// Em Program.cs (ja configurado no DI)
services.AddMiniProfiler(options =>
{
    options.RouteBasePath = "/profiler";
    options.SqlFormatter = new StackExchange.Profiling.SqlFormatters.InlineFormatter();
}).AddEntityFramework();
```

#### Uso

1. Acessar qualquer endpoint da API
2. Abrir `https://localhost:7001/profiler/results-index` para ver resultados
3. Cada request mostra: tempo total, queries SQL executadas, tempo por query

### dotnet-trace (Diagnostico de Runtime)

```bash
# Instalar ferramenta
dotnet tool install --global dotnet-trace

# Listar processos .NET
dotnet-trace list-processes

# Capturar trace (encontrar PID do gateway)
dotnet-trace collect --process-id <PID> --duration 00:00:30

# Analisar no Visual Studio ou PerfView
# Arquivo gerado: trace.nettrace
```

### dotnet-counters (Metricas em Tempo Real)

```bash
# Instalar ferramenta
dotnet tool install --global dotnet-counters

# Monitorar metricas em tempo real
dotnet-counters monitor --process-id <PID> --counters \
  System.Runtime,\
  Microsoft.AspNetCore.Hosting,\
  Microsoft.EntityFrameworkCore
```

**Metricas uteis:**

| Counter | Descricao |
|---------|-----------|
| `cpu-usage` | Uso de CPU do processo |
| `gc-heap-size` | Tamanho do heap GC |
| `alloc-rate` | Taxa de alocacao de memoria |
| `requests-per-second` | RPS do ASP.NET Core |
| `current-requests` | Requests em andamento |
| `ef-active-db-contexts` | DbContexts ativos |
| `ef-queries-per-second` | Queries EF por segundo |

### dotnet-dump (Analise de Memoria)

```bash
# Instalar
dotnet tool install --global dotnet-dump

# Capturar dump
dotnet-dump collect --process-id <PID>

# Analisar
dotnet-dump analyze dump_YYYYMMDD_HHMMSS.dmp

# Comandos dentro do analyzer:
# dumpheap -stat           → objetos na heap por tipo
# dumpheap -type Holder    → instancias de Holder na heap
# gcroot <address>         → cadeia de referencias mantendo objeto vivo
```

---

## Cenarios Comuns de Debug

| Problema | Ferramenta | Como Investigar |
|----------|-----------|-----------------|
| Request retorna 401 mas token parece valido | Breakpoint em `JwtBearerEvents.OnAuthenticationFailed` | Ver `context.Exception` para motivo exato da rejeicao. Verificar `Authority` e `Audience` no appsettings |
| Request retorna 403 com token valido | Breakpoint em `AuthorizationMiddleware` | Inspecionar `HttpContext.User.Claims` e comparar roles com `[Authorize(Roles = "...")]` do endpoint |
| Query retorna dados de outro tenant | Breakpoint em `TenantMiddleware` | Verificar que `SET app.current_tenant` esta sendo executado. Inspecionar `current_setting('app.current_tenant')` no banco |
| EF Core N+1 query problem | MiniProfiler / EF Core logging | Contar numero de queries por request. Adicionar `.Include()` para eager loading |
| Handler nao e encontrado pelo MediatR | Logs de startup (DI registration) | Verificar que assembly do handler esta registrado em `AddMediatR(cfg => cfg.RegisterServicesFromAssembly(...))` |
| Validator nao executa | Breakpoint no `ValidationBehavior<TRequest, TResponse>` | Verificar que FluentValidation esta registrado e behavior esta no pipeline MediatR |
| Domain event nao dispara | Breakpoint em `DomainEventDispatcher.DispatchAsync()` | Verificar que entity herda `BaseAggregateRoot` e evento foi adicionado via `AddDomainEvent()` |
| Migration nao aplica alteracao esperada | Inspecionar arquivo da migration gerada | Comparar `Up()` com a alteracao desejada. Verificar `AppDbContextModelSnapshot.cs` |
| SignalR nao recebe notificacao | Breakpoint no Hub + logging do SignalR | Habilitar: `"Microsoft.AspNetCore.SignalR": "Debug"` |
| Background job nao executa | Hangfire Dashboard + logs | Verificar queue, ver retries e exceptions em `https://localhost:7001/hangfire` |
| Serialization/Deserialization falha | Breakpoint em `JsonSerializer` | Verificar JsonSerializerOptions (camelCase, ReferenceHandler, converters) |
| PostGIS funcao retorna erro | Log da query SQL + pgAdmin | Executar query diretamente no banco para isolar problema. Verificar SRID dos geometries |
| Cache retorna dados stale | Redis CLI + breakpoint no CacheService | `docker exec geoapi-redis redis-cli GET "chave"` para ver valor atual. Verificar TTL |
| Upload arquivo falha | Breakpoint em `FileStorageService` | Verificar bucket existe no MinIO, verificar credenciais, verificar tamanho maximo |
| CORS error no browser | Breakpoint em CORS middleware | Verificar `AllowedOrigins` inclui origin do frontend. Inspecionar headers `Access-Control-Allow-Origin` |

---

## Dicas de Produtividade

### Rider

- `Ctrl+Shift+F8` - Ver todos os breakpoints ativos
- `Alt+F8` - Evaluate expression durante pausa
- `Ctrl+Shift+T` - Navegar para teste da classe atual
- `Shift+F9` - Debug (com breakpoints)

### Visual Studio

- `Ctrl+Alt+B` - Janela de breakpoints
- `Ctrl+Alt+I` - Immediate window
- `F9` - Toggle breakpoint
- `F10` - Step over / `F11` - Step into

### VS Code

- `F9` - Toggle breakpoint
- `Ctrl+Shift+D` - Abrir painel Debug
- `Debug Console` - Avaliar expressoes durante pausa

---

## Referencias

| Recurso | Link |
|---------|------|
| Serilog Configuration | serilog.net |
| EF Core Logging | learn.microsoft.com/ef/core/logging-events-diagnostics |
| MiniProfiler for .NET | miniprofiler.com/dotnet |
| dotnet-trace | learn.microsoft.com/dotnet/core/diagnostics/dotnet-trace |
| dotnet-counters | learn.microsoft.com/dotnet/core/diagnostics/dotnet-counters |
| Troubleshooting | [08-troubleshooting.md](./08-troubleshooting.md) |
