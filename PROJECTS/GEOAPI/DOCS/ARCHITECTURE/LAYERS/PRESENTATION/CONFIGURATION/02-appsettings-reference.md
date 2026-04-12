---
type: leaf
status: review
updated: 2026-02-08
---

# Referencia appsettings.json - GEOAPI

Referencia completa de todas as chaves de configuracao utilizadas pelo GEOAPI nos arquivos `appsettings.json`, `appsettings.Development.json`, `appsettings.Staging.json` e `appsettings.Production.json`.

---

## Visao Geral

O GEOAPI utiliza o sistema de configuracao do ASP.NET Core com a seguinte precedencia (da menor para a maior prioridade):

1. `appsettings.json` (valores base/padrao)
2. `appsettings.{Environment}.json` (sobrescreve por ambiente)
3. Variaveis de ambiente (sobrescreve tudo)
4. User Secrets (apenas Development, via `dotnet user-secrets`)
5. Command-line arguments

---

## ConnectionStrings

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `ConnectionStrings:DefaultConnection` | string | Sim | - | Connection string do PostgreSQL + PostGIS. Formato Npgsql | `ConnectionStrings__DefaultConnection` |
| `ConnectionStrings:Redis` | string | Sim | - | Connection string do Redis (StackExchange.Redis format) | `ConnectionStrings__Redis` |

### Formato DefaultConnection

```
Host=<host>;Port=<port>;Database=<db>;Username=<user>;Password=<pass>;Include Error Detail=<bool>;Maximum Pool Size=<int>;Timeout=<int>
```

### Exemplos por Ambiente

| Ambiente | DefaultConnection |
|----------|-------------------|
| Development | `Host=localhost;Port=5432;Database=geoapi_dev;Username=geoapi;Password=dev123;Include Error Detail=true` |
| Staging | `Host=staging-db.internal;Port=5432;Database=geoapi_stg;Username=geoapi_stg;Password=***;SSL Mode=Require;Trust Server Certificate=true` |
| Production | `Host=prod-db.internal;Port=5432;Database=geoapi_prod;Username=geoapi_prod;Password=***;SSL Mode=VerifyFull;Maximum Pool Size=100;Timeout=30` |

### Exemplos Redis

| Ambiente | Redis |
|----------|-------|
| Development | `localhost:6379,defaultDatabase=0` |
| Staging | `staging-redis.internal:6379,password=***,defaultDatabase=0,ssl=true` |
| Production | `prod-redis.internal:6379,password=***,defaultDatabase=0,ssl=true,connectTimeout=5000,syncTimeout=5000` |

---

## Keycloak

Configuracao do Identity Provider para autenticacao JWT Bearer.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Keycloak:Authority` | string | Sim | - | URL do realm Keycloak. Formato: `{base_url}/realms/{realm}` | `Keycloak__Authority` |
| `Keycloak:Audience` | string | Sim | - | Client ID esperado no campo `aud` do JWT | `Keycloak__Audience` |
| `Keycloak:RequireHttpsMetadata` | bool | Nao | `true` | Se `true`, exige HTTPS para o metadata endpoint. Setar `false` apenas em Development | `Keycloak__RequireHttpsMetadata` |
| `Keycloak:MetadataAddress` | string | Nao | `{Authority}/.well-known/openid-configuration` | URL explicita do OpenID Connect discovery document | `Keycloak__MetadataAddress` |
| `Keycloak:ValidIssuers` | string[] | Nao | `[Authority]` | Lista de issuers validos (util quando URL interna difere da publica) | `Keycloak__ValidIssuers__0`, `Keycloak__ValidIssuers__1` |
| `Keycloak:ClockSkew` | TimeSpan | Nao | `00:00:30` | Tolerancia de dessincronizacao de relogio na validacao de token | `Keycloak__ClockSkew` |
| `Keycloak:RoleClaimType` | string | Nao | `realm_access.roles` | Caminho do claim que contem as roles no JWT | `Keycloak__RoleClaimType` |

### Exemplos por Ambiente

| Ambiente | Authority | RequireHttpsMetadata |
|----------|-----------|---------------------|
| Development | `http://localhost:8080/realms/carf` | `false` |
| Staging | `https://auth-staging.carf.gov.br/realms/carf` | `true` |
| Production | `https://auth.carf.gov.br/realms/carf` | `true` |

---

## Storage (S3/MinIO)

Configuracao do object storage para documentos, fotos e ortofotos.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Storage:Provider` | string | Sim | - | Provedor de storage: `S3` ou `MinIO` | `Storage__Provider` |
| `Storage:Endpoint` | string | Sim (MinIO) | - | URL do endpoint MinIO. Nao necessario para AWS S3 | `Storage__Endpoint` |
| `Storage:BucketName` | string | Sim | - | Nome do bucket principal para documentos | `Storage__BucketName` |
| `Storage:OrthofotoBucket` | string | Nao | `carf-orthofotos` | Bucket separado para ortofotos (arquivos grandes) | `Storage__OrthofotoBucket` |
| `Storage:ExportBucket` | string | Nao | `carf-exports` | Bucket para exports gerados (PDF, CSV, Shapefile) | `Storage__ExportBucket` |
| `Storage:Region` | string | Nao | `us-east-1` | Regiao AWS. Para MinIO local, usar `us-east-1` | `Storage__Region` |
| `Storage:AccessKey` | string | Sim | - | Access key ID (AWS) ou root user (MinIO) | `Storage__AccessKey` |
| `Storage:SecretKey` | string | Sim | - | Secret access key (AWS) ou root password (MinIO) | `Storage__SecretKey` |
| `Storage:ForcePathStyle` | bool | Nao | `false` | Setar `true` para MinIO (path-style ao inves de virtual-hosted-style) | `Storage__ForcePathStyle` |
| `Storage:PresignedUrlExpiration` | TimeSpan | Nao | `01:00:00` | Tempo de validade de URLs presigned para download | `Storage__PresignedUrlExpiration` |
| `Storage:MaxFileSizeMB` | int | Nao | `50` | Tamanho maximo de arquivo para upload (em MB) | `Storage__MaxFileSizeMB` |

### Exemplos por Ambiente

| Ambiente | Provider | Endpoint | ForcePathStyle |
|----------|----------|----------|----------------|
| Development | `MinIO` | `http://localhost:9000` | `true` |
| Staging | `S3` | (nao necessario) | `false` |
| Production | `S3` | (nao necessario) | `false` |

---

## Redis

Configuracao adicional do Redis alem da connection string.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Redis:InstanceName` | string | Nao | `geoapi:` | Prefixo para chaves no Redis (isolamento por aplicacao) | `Redis__InstanceName` |
| `Redis:DefaultDatabase` | int | Nao | `0` | Numero do database Redis (0-15) | `Redis__DefaultDatabase` |
| `Redis:DefaultCacheDuration` | TimeSpan | Nao | `00:30:00` | TTL padrao para cache entries | `Redis__DefaultCacheDuration` |
| `Redis:SlidingExpiration` | TimeSpan | Nao | `00:10:00` | Sliding expiration padrao (reseta TTL a cada acesso) | `Redis__SlidingExpiration` |
| `Redis:ConnectRetry` | int | Nao | `3` | Numero de tentativas de reconexao | `Redis__ConnectRetry` |
| `Redis:ConnectTimeout` | int | Nao | `5000` | Timeout de conexao em milissegundos | `Redis__ConnectTimeout` |

---

## Hangfire

Configuracao do processador de background jobs.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Hangfire:SchemaName` | string | Nao | `hangfire` | Nome do schema PostgreSQL para tabelas do Hangfire | `Hangfire__SchemaName` |
| `Hangfire:WorkerCount` | int | Nao | `Environment.ProcessorCount` | Numero de workers paralelos | `Hangfire__WorkerCount` |
| `Hangfire:Queues` | string[] | Nao | `["default"]` | Queues que os workers processam, em ordem de prioridade | `Hangfire__Queues__0`, `Hangfire__Queues__1` |
| `Hangfire:DashboardPath` | string | Nao | `/hangfire` | Path do dashboard web | `Hangfire__DashboardPath` |
| `Hangfire:DashboardAuthorization` | bool | Nao | `true` | Se `true`, exige autenticacao para acessar dashboard. `false` para dev | `Hangfire__DashboardAuthorization` |
| `Hangfire:RetryAttempts` | int | Nao | `10` | Numero maximo de retries para jobs que falham | `Hangfire__RetryAttempts` |

### Queues Utilizadas

| Queue | Prioridade | Tipo de Jobs |
|-------|-----------|-------------|
| `default` | Normal | Jobs gerais (notificacoes, cleanup) |
| `sync` | Alta | Processamento de pacotes sync offline |
| `reports` | Baixa | Geracao de relatorios PDF/CSV/Shapefile |
| `orthofotos` | Baixa | Processamento de ortofotos (crop, tile) |

---

## Cors

Configuracao de Cross-Origin Resource Sharing.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Cors:AllowedOrigins` | string[] | Sim | - | Lista de origins permitidas | `Cors__AllowedOrigins__0`, `Cors__AllowedOrigins__1` |
| `Cors:AllowCredentials` | bool | Nao | `true` | Permitir envio de cookies/auth headers cross-origin | `Cors__AllowCredentials` |
| `Cors:AllowedHeaders` | string[] | Nao | `["*"]` | Headers permitidos nas requests | `Cors__AllowedHeaders__0` |
| `Cors:AllowedMethods` | string[] | Nao | `["GET","POST","PUT","DELETE","PATCH","OPTIONS"]` | Metodos HTTP permitidos | `Cors__AllowedMethods__0` |
| `Cors:ExposedHeaders` | string[] | Nao | `["Content-Disposition"]` | Headers expostos ao JavaScript do browser | `Cors__ExposedHeaders__0` |

### Origins por Ambiente

| Ambiente | Origins |
|----------|---------|
| Development | `http://localhost:3000` (REURBWEB), `http://localhost:4321` (WEBDOCS), `http://localhost:19006` (Expo) |
| Staging | `https://staging.carf.gov.br`, `https://docs-staging.carf.gov.br` |
| Production | `https://app.carf.gov.br`, `https://docs.carf.gov.br` |

---

## Logging (Serilog)

Configuracao de logging estruturado.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Serilog:MinimumLevel:Default` | string | Nao | `Information` | Nivel minimo global de log | `Serilog__MinimumLevel__Default` |
| `Serilog:MinimumLevel:Override:Microsoft.AspNetCore` | string | Nao | `Warning` | Nivel para logs do ASP.NET Core | `Serilog__MinimumLevel__Override__Microsoft.AspNetCore` |
| `Serilog:MinimumLevel:Override:Microsoft.EntityFrameworkCore` | string | Nao | `Warning` | Nivel para logs do EF Core | `Serilog__MinimumLevel__Override__Microsoft.EntityFrameworkCore` |
| `Serilog:MinimumLevel:Override:Microsoft.EntityFrameworkCore.Database.Command` | string | Nao | `Warning` | Nivel para queries SQL do EF Core. Setar `Information` para ver SQL | `Serilog__MinimumLevel__Override__Microsoft.EntityFrameworkCore.Database.Command` |
| `Serilog:MinimumLevel:Override:Hangfire` | string | Nao | `Warning` | Nivel para logs do Hangfire | `Serilog__MinimumLevel__Override__Hangfire` |
| `Serilog:MinimumLevel:Override:Carf.GeoApi` | string | Nao | `Debug` | Nivel para logs da propria aplicacao | `Serilog__MinimumLevel__Override__Carf.GeoApi` |
| `Serilog:WriteTo` | array | Nao | Console | Sinks de output (Console, File, Elasticsearch, Seq) | - |
| `Serilog:Enrich` | string[] | Nao | `[]` | Enrichers (FromLogContext, WithMachineName, WithThreadId) | - |

### Sinks por Ambiente

| Ambiente | Sinks |
|----------|-------|
| Development | Console (colored), File (JSON, rotacao diaria) |
| Staging | Console (JSON), Elasticsearch |
| Production | Console (JSON), Elasticsearch, alertas via email para Fatal |

---

## HealthChecks

Configuracao dos health check endpoints para probes do Kubernetes.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `HealthChecks:PostgreSQL:Timeout` | TimeSpan | Nao | `00:00:05` | Timeout para check do PostgreSQL | `HealthChecks__PostgreSQL__Timeout` |
| `HealthChecks:PostgreSQL:Query` | string | Nao | `SELECT 1;` | Query de teste de conectividade | `HealthChecks__PostgreSQL__Query` |
| `HealthChecks:Redis:Timeout` | TimeSpan | Nao | `00:00:03` | Timeout para check do Redis | `HealthChecks__Redis__Timeout` |
| `HealthChecks:S3:Timeout` | TimeSpan | Nao | `00:00:05` | Timeout para check do S3/MinIO | `HealthChecks__S3__Timeout` |
| `HealthChecks:S3:BucketToCheck` | string | Nao | `carf-documents` | Bucket usado no health check (verifica existencia) | `HealthChecks__S3__BucketToCheck` |
| `HealthChecks:Keycloak:Timeout` | TimeSpan | Nao | `00:00:05` | Timeout para check do Keycloak | `HealthChecks__Keycloak__Timeout` |
| `HealthChecks:Keycloak:Url` | string | Nao | `{Authority}/.well-known/openid-configuration` | URL de health check do Keycloak | `HealthChecks__Keycloak__Url` |

### Endpoints Expostos

| Endpoint | Proposito | Kubernetes Probe |
|----------|-----------|-----------------|
| `/health` | Status geral (todos os checks) | Readiness probe |
| `/health/live` | Apenas verifica se app responde | Liveness probe |
| `/health/ready` | Verifica dependencias externas | Readiness probe |

---

## RateLimiting

Configuracao de rate limiting para protecao da API.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `RateLimiting:Enabled` | bool | Nao | `true` | Habilitar/desabilitar rate limiting globalmente | `RateLimiting__Enabled` |
| `RateLimiting:PermitLimit` | int | Nao | `100` | Numero maximo de requests por janela de tempo | `RateLimiting__PermitLimit` |
| `RateLimiting:WindowSeconds` | int | Nao | `60` | Janela de tempo em segundos | `RateLimiting__WindowSeconds` |
| `RateLimiting:QueueLimit` | int | Nao | `10` | Requests que podem ficar em fila quando limite atingido | `RateLimiting__QueueLimit` |
| `RateLimiting:SegmentsPerWindow` | int | Nao | `4` | Segmentos da sliding window (granularidade) | `RateLimiting__SegmentsPerWindow` |

### Limites por Ambiente

| Ambiente | PermitLimit | WindowSeconds | Notas |
|----------|-------------|---------------|-------|
| Development | `1000` | `60` | Mais permissivo para dev |
| Staging | `200` | `60` | Simular producao |
| Production | `100` | `60` | Limite real |

---

## Jwt (Configuracao Avancada)

Parametros adicionais de validacao de tokens JWT.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Jwt:ValidateIssuer` | bool | Nao | `true` | Validar campo `iss` do token | `Jwt__ValidateIssuer` |
| `Jwt:ValidateAudience` | bool | Nao | `true` | Validar campo `aud` do token | `Jwt__ValidateAudience` |
| `Jwt:ValidateLifetime` | bool | Nao | `true` | Validar campos `exp` e `nbf` do token | `Jwt__ValidateLifetime` |
| `Jwt:ValidateIssuerSigningKey` | bool | Nao | `true` | Validar assinatura do token com chave publica do Keycloak | `Jwt__ValidateIssuerSigningKey` |
| `Jwt:ClockSkew` | TimeSpan | Nao | `00:00:30` | Tolerancia de clock skew (dessincronizacao de relogio) | `Jwt__ClockSkew` |
| `Jwt:SaveToken` | bool | Nao | `true` | Salvar token no `AuthenticationProperties` para acesso posterior | `Jwt__SaveToken` |

---

## Kestrel

Configuracao do servidor HTTP Kestrel.

| Chave | Tipo | Required | Default | Descricao | Env Var Override |
|-------|------|----------|---------|-----------|-----------------|
| `Kestrel:Endpoints:Https:Url` | string | Nao | `https://localhost:7001` | URL HTTPS do endpoint | `Kestrel__Endpoints__Https__Url` |
| `Kestrel:Endpoints:Http:Url` | string | Nao | `http://localhost:5001` | URL HTTP do endpoint | `Kestrel__Endpoints__Http__Url` |
| `Kestrel:Limits:MaxRequestBodySize` | long | Nao | `30000000` (30MB) | Tamanho maximo do body de request em bytes | `Kestrel__Limits__MaxRequestBodySize` |
| `Kestrel:Limits:RequestHeadersTimeout` | TimeSpan | Nao | `00:00:30` | Timeout para receber headers | `Kestrel__Limits__RequestHeadersTimeout` |
| `Kestrel:Limits:KeepAliveTimeout` | TimeSpan | Nao | `00:02:00` | Timeout para conexoes keep-alive | `Kestrel__Limits__KeepAliveTimeout` |

---

## Exemplo Completo: appsettings.Development.json

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=geoapi_dev;Username=geoapi;Password=dev123;Include Error Detail=true",
    "Redis": "localhost:6379,defaultDatabase=0"
  },
  "Keycloak": {
    "Authority": "http://localhost:8080/realms/carf",
    "Audience": "geoapi",
    "RequireHttpsMetadata": false,
    "MetadataAddress": "http://localhost:8080/realms/carf/.well-known/openid-configuration"
  },
  "Storage": {
    "Provider": "MinIO",
    "Endpoint": "http://localhost:9000",
    "BucketName": "carf-documents",
    "OrthofotoBucket": "carf-orthofotos",
    "ExportBucket": "carf-exports",
    "Region": "us-east-1",
    "AccessKey": "minioadmin",
    "SecretKey": "minioadmin",
    "ForcePathStyle": true,
    "MaxFileSizeMB": 100
  },
  "Redis": {
    "InstanceName": "geoapi-dev:",
    "DefaultCacheDuration": "00:15:00"
  },
  "Hangfire": {
    "SchemaName": "hangfire",
    "WorkerCount": 2,
    "Queues": ["default", "sync", "reports"],
    "DashboardAuthorization": false
  },
  "Cors": {
    "AllowedOrigins": [
      "http://localhost:3000",
      "http://localhost:4321",
      "http://localhost:19006"
    ]
  },
  "Serilog": {
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft.AspNetCore": "Warning",
        "Microsoft.EntityFrameworkCore": "Warning",
        "Microsoft.EntityFrameworkCore.Database.Command": "Information",
        "Hangfire": "Warning",
        "Carf.GeoApi": "Debug"
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
          "retainedFileCountLimit": 7
        }
      }
    ],
    "Enrich": ["FromLogContext", "WithMachineName", "WithThreadId"]
  },
  "HealthChecks": {
    "PostgreSQL": { "Timeout": "00:00:05" },
    "Redis": { "Timeout": "00:00:03" },
    "S3": { "Timeout": "00:00:05" },
    "Keycloak": { "Timeout": "00:00:05" }
  },
  "RateLimiting": {
    "Enabled": false,
    "PermitLimit": 1000,
    "WindowSeconds": 60
  },
  "Jwt": {
    "ClockSkew": "00:05:00"
  }
}
```

---

## Referencias

| Recurso | Link |
|---------|------|
| ASP.NET Core Configuration | learn.microsoft.com/aspnet/core/fundamentals/configuration |
| Serilog Configuration | github.com/serilog/serilog-settings-configuration |
| Npgsql Connection Strings | npgsql.org/doc/connection-string-parameters.html |
| StackExchange.Redis Config | stackexchange.github.io/StackExchange.Redis/Configuration.html |
| Environment Variables | [03-environment-variables.md](./03-environment-variables.md) |
| Setup ambiente | [../../HOW-TO/01-setup-dev-environment.md](../../HOW-TO/01-setup-dev-environment.md) |
