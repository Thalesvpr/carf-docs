---
type: leaf
status: review
updated: 2026-02-08
---

# Variaveis de Ambiente - GEOAPI

Referencia completa de todas as variaveis de ambiente utilizadas pelo GEOAPI, incluindo mapeamento para appsettings, exemplos por ambiente e classificacao de sensibilidade.

---

## Como Funciona o Binding de Configuracao

O ASP.NET Core utiliza um sistema hierarquico de configuracao onde variaveis de ambiente sobrescrevem valores de `appsettings.json`. O mapeamento segue a convencao:

### Regra de Conversao

| appsettings.json path | Variavel de Ambiente |
|----------------------|---------------------|
| `ConnectionStrings:DefaultConnection` | `ConnectionStrings__DefaultConnection` |
| `Keycloak:Authority` | `Keycloak__Authority` |
| `Storage:ForcePathStyle` | `Storage__ForcePathStyle` |
| `Serilog:MinimumLevel:Default` | `Serilog__MinimumLevel__Default` |
| `Cors:AllowedOrigins[0]` | `Cors__AllowedOrigins__0` |

**Regra:** Substituir `:` por `__` (duplo underscore). Para arrays, usar indice numerico.

> **Nota:** Em Linux, o separador `:` tambem funciona em variaveis de ambiente, mas `__` e recomendado por compatibilidade cross-platform.

---

## Variaveis de Ambiente Completas

### Connection Strings

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `ConnectionStrings__DefaultConnection` | `ConnectionStrings:DefaultConnection` | Npgsql connection string | `Host=localhost;Port=5432;Database=geoapi_dev;Username=geoapi;Password=dev123` | `Host=prod-db.internal;Port=5432;Database=geoapi_prod;Username=geoapi_prod;Password=***;SSL Mode=VerifyFull` | Sim | Connection string do PostgreSQL |
| `ConnectionStrings__Redis` | `ConnectionStrings:Redis` | StackExchange.Redis format | `localhost:6379,defaultDatabase=0` | `prod-redis.internal:6379,password=***,ssl=true` | Sim | Connection string do Redis |

### Keycloak / Autenticacao

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `Keycloak__Authority` | `Keycloak:Authority` | URL | `http://localhost:8080/realms/carf` | `https://auth.carf.gov.br/realms/carf` | Nao | URL do realm Keycloak |
| `Keycloak__Audience` | `Keycloak:Audience` | string | `geoapi` | `geoapi` | Nao | Client ID esperado no JWT |
| `Keycloak__RequireHttpsMetadata` | `Keycloak:RequireHttpsMetadata` | bool | `false` | `true` | Nao | Exigir HTTPS para metadata |
| `Keycloak__MetadataAddress` | `Keycloak:MetadataAddress` | URL | `http://localhost:8080/realms/carf/.well-known/openid-configuration` | (auto-derivado da Authority) | Nao | URL do discovery document |
| `Keycloak__ClockSkew` | `Keycloak:ClockSkew` | TimeSpan | `00:05:00` | `00:00:30` | Nao | Tolerancia de clock skew |

### Storage (S3/MinIO)

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `Storage__Provider` | `Storage:Provider` | string | `MinIO` | `S3` | Nao | Provedor de storage |
| `Storage__Endpoint` | `Storage:Endpoint` | URL | `http://localhost:9000` | (nao necessario para S3) | Nao | Endpoint MinIO |
| `Storage__BucketName` | `Storage:BucketName` | string | `carf-documents` | `carf-documents-prod` | Nao | Bucket de documentos |
| `Storage__OrthofotoBucket` | `Storage:OrthofotoBucket` | string | `carf-orthofotos` | `carf-orthofotos-prod` | Nao | Bucket de ortofotos |
| `Storage__ExportBucket` | `Storage:ExportBucket` | string | `carf-exports` | `carf-exports-prod` | Nao | Bucket de exports |
| `Storage__Region` | `Storage:Region` | string | `us-east-1` | `sa-east-1` | Nao | Regiao AWS |
| `Storage__AccessKey` | `Storage:AccessKey` | string | `minioadmin` | `AKIA...` | Sim | Access key |
| `Storage__SecretKey` | `Storage:SecretKey` | string | `minioadmin` | `wJalrXU...` | Sim | Secret key |
| `Storage__ForcePathStyle` | `Storage:ForcePathStyle` | bool | `true` | `false` | Nao | Path style (MinIO=true) |
| `Storage__MaxFileSizeMB` | `Storage:MaxFileSizeMB` | int | `100` | `50` | Nao | Tamanho maximo upload |

### Redis

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `Redis__InstanceName` | `Redis:InstanceName` | string | `geoapi-dev:` | `geoapi-prod:` | Nao | Prefixo de chaves Redis |
| `Redis__DefaultDatabase` | `Redis:DefaultDatabase` | int | `0` | `0` | Nao | Database number |
| `Redis__DefaultCacheDuration` | `Redis:DefaultCacheDuration` | TimeSpan | `00:15:00` | `00:30:00` | Nao | TTL padrao de cache |

### Hangfire

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `Hangfire__SchemaName` | `Hangfire:SchemaName` | string | `hangfire` | `hangfire` | Nao | Schema PostgreSQL |
| `Hangfire__WorkerCount` | `Hangfire:WorkerCount` | int | `2` | `8` | Nao | Workers paralelos |
| `Hangfire__Queues__0` | `Hangfire:Queues[0]` | string | `default` | `default` | Nao | Primeira queue |
| `Hangfire__Queues__1` | `Hangfire:Queues[1]` | string | `sync` | `sync` | Nao | Queue de sync |
| `Hangfire__Queues__2` | `Hangfire:Queues[2]` | string | `reports` | `reports` | Nao | Queue de relatorios |
| `Hangfire__DashboardAuthorization` | `Hangfire:DashboardAuthorization` | bool | `false` | `true` | Nao | Auth no dashboard |

### CORS

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `Cors__AllowedOrigins__0` | `Cors:AllowedOrigins[0]` | URL | `http://localhost:3000` | `https://app.carf.gov.br` | Nao | Primeira origin permitida |
| `Cors__AllowedOrigins__1` | `Cors:AllowedOrigins[1]` | URL | `http://localhost:4321` | `https://docs.carf.gov.br` | Nao | Segunda origin permitida |
| `Cors__AllowedOrigins__2` | `Cors:AllowedOrigins[2]` | URL | `http://localhost:19006` | (nao necessario) | Nao | Terceira origin permitida |

### Logging

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `Serilog__MinimumLevel__Default` | `Serilog:MinimumLevel:Default` | string | `Information` | `Warning` | Nao | Nivel minimo global |
| `Serilog__MinimumLevel__Override__Microsoft.AspNetCore` | `Serilog:MinimumLevel:Override:Microsoft.AspNetCore` | string | `Warning` | `Warning` | Nao | Nivel ASP.NET Core |
| `Serilog__MinimumLevel__Override__Microsoft.EntityFrameworkCore` | `Serilog:MinimumLevel:Override:Microsoft.EntityFrameworkCore` | string | `Warning` | `Error` | Nao | Nivel EF Core |
| `Serilog__MinimumLevel__Override__Carf.GeoApi` | `Serilog:MinimumLevel:Override:Carf.GeoApi` | string | `Debug` | `Information` | Nao | Nivel aplicacao |

### Rate Limiting

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `RateLimiting__Enabled` | `RateLimiting:Enabled` | bool | `false` | `true` | Nao | Habilitar rate limiting |
| `RateLimiting__PermitLimit` | `RateLimiting:PermitLimit` | int | `1000` | `100` | Nao | Requests por janela |
| `RateLimiting__WindowSeconds` | `RateLimiting:WindowSeconds` | int | `60` | `60` | Nao | Janela em segundos |

### Health Checks

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `HealthChecks__PostgreSQL__Timeout` | `HealthChecks:PostgreSQL:Timeout` | TimeSpan | `00:00:05` | `00:00:03` | Nao | Timeout check PostgreSQL |
| `HealthChecks__Redis__Timeout` | `HealthChecks:Redis:Timeout` | TimeSpan | `00:00:03` | `00:00:02` | Nao | Timeout check Redis |
| `HealthChecks__S3__Timeout` | `HealthChecks:S3:Timeout` | TimeSpan | `00:00:05` | `00:00:03` | Nao | Timeout check S3 |
| `HealthChecks__Keycloak__Timeout` | `HealthChecks:Keycloak:Timeout` | TimeSpan | `00:00:05` | `00:00:03` | Nao | Timeout check Keycloak |

### Kestrel

| Variavel | Secao appsettings | Formato | Exemplo Dev | Exemplo Prod | Sensivel | Descricao |
|----------|-------------------|---------|------------|-------------|----------|-----------|
| `ASPNETCORE_URLS` | (built-in) | URLs separadas por `;` | `https://localhost:7001;http://localhost:5001` | `http://+:5001` | Nao | URLs do Kestrel |
| `ASPNETCORE_ENVIRONMENT` | (built-in) | string | `Development` | `Production` | Nao | Ambiente de execucao |
| `Kestrel__Limits__MaxRequestBodySize` | `Kestrel:Limits:MaxRequestBodySize` | long | `104857600` (100MB) | `52428800` (50MB) | Nao | Tamanho maximo body |

---

## Classificacao de Sensibilidade

### Variaveis Sensiveis (Secrets)

Estas variaveis NUNCA devem estar em appsettings.json commitado no repositorio. Devem ser fornecidas via:
- **Development:** User Secrets (`dotnet user-secrets set`) ou `.env` (gitignored)
- **Staging/Production:** Kubernetes Secrets, Vault, ou sistema de secrets do cloud provider

| Variavel | Risco se Exposta |
|----------|-----------------|
| `ConnectionStrings__DefaultConnection` | Acesso total ao banco de dados |
| `ConnectionStrings__Redis` | Acesso ao cache (pode conter tokens) |
| `Storage__AccessKey` | Acesso a todos os arquivos no S3/MinIO |
| `Storage__SecretKey` | Acesso a todos os arquivos no S3/MinIO |

### Variaveis Nao-Sensiveis (Config)

Podem estar em appsettings.json versionado. Nao representam risco de seguranca se expostas:

Todas as demais variaveis listadas acima (URLs, timeouts, log levels, flags de feature, nomes de buckets, etc.).

---

## Docker Compose: env_file

### Arquivo `.env` (gitignored)

```env
# PostgreSQL
POSTGRES_DB=geoapi_dev
POSTGRES_USER=geoapi
POSTGRES_PASSWORD=dev123

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# Keycloak
KEYCLOAK_ADMIN=admin
KEYCLOAK_ADMIN_PASSWORD=admin

# GEOAPI (se rodando em container)
ConnectionStrings__DefaultConnection=Host=geoapi-db;Port=5432;Database=geoapi_dev;Username=geoapi;Password=dev123
ConnectionStrings__Redis=geoapi-redis:6379,defaultDatabase=0
Keycloak__Authority=http://geoapi-keycloak:8080/realms/carf
Storage__Endpoint=http://geoapi-minio:9000
Storage__AccessKey=minioadmin
Storage__SecretKey=minioadmin
```

### Referencia no docker-compose.yml

```yaml
services:
  geoapi:
    env_file:
      - .env
    # ou variaveis inline:
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=geoapi-db;...
```

> **Importante:** Quando a API roda dentro do Docker, usar nomes de container (`geoapi-db`, `geoapi-redis`) ao inves de `localhost`.

---

## Kubernetes: ConfigMap e Secrets

### ConfigMap (variaveis nao-sensiveis)

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: geoapi-config
  namespace: carf
data:
  ASPNETCORE_ENVIRONMENT: "Production"
  Keycloak__Authority: "https://auth.carf.gov.br/realms/carf"
  Keycloak__Audience: "geoapi"
  Keycloak__RequireHttpsMetadata: "true"
  Storage__Provider: "S3"
  Storage__Region: "sa-east-1"
  Storage__BucketName: "carf-documents-prod"
  Storage__ForcePathStyle: "false"
  Redis__InstanceName: "geoapi-prod:"
  Hangfire__WorkerCount: "8"
  Hangfire__Queues__0: "default"
  Hangfire__Queues__1: "sync"
  Hangfire__Queues__2: "reports"
  Cors__AllowedOrigins__0: "https://app.carf.gov.br"
  Cors__AllowedOrigins__1: "https://docs.carf.gov.br"
  Serilog__MinimumLevel__Default: "Warning"
  RateLimiting__Enabled: "true"
  RateLimiting__PermitLimit: "100"
  HealthChecks__PostgreSQL__Timeout: "00:00:03"
```

### Secret (variaveis sensiveis)

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: geoapi-secrets
  namespace: carf
type: Opaque
stringData:
  ConnectionStrings__DefaultConnection: "Host=prod-db.internal;Port=5432;Database=geoapi_prod;Username=geoapi_prod;Password=SUPER_SECRET;SSL Mode=VerifyFull"
  ConnectionStrings__Redis: "prod-redis.internal:6379,password=REDIS_SECRET,ssl=true"
  Storage__AccessKey: "AKIAIOSFODNN7EXAMPLE"
  Storage__SecretKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

### Deployment referenciando ConfigMap e Secret

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geoapi
  namespace: carf
spec:
  template:
    spec:
      containers:
        - name: geoapi
          image: registry.carf.gov.br/geoapi:latest
          envFrom:
            - configMapRef:
                name: geoapi-config
            - secretRef:
                name: geoapi-secrets
          ports:
            - containerPort: 5001
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 5001
            initialDelaySeconds: 10
            periodSeconds: 15
          livenessProbe:
            httpGet:
              path: /health/live
              port: 5001
            initialDelaySeconds: 15
            periodSeconds: 30
```

---

## Exemplos Completos por Ambiente

### Development (local)

```bash
export ASPNETCORE_ENVIRONMENT=Development
export ConnectionStrings__DefaultConnection="Host=localhost;Port=5432;Database=geoapi_dev;Username=geoapi;Password=dev123;Include Error Detail=true"
export ConnectionStrings__Redis="localhost:6379,defaultDatabase=0"
export Keycloak__Authority="http://localhost:8080/realms/carf"
export Keycloak__Audience="geoapi"
export Keycloak__RequireHttpsMetadata="false"
export Storage__Provider="MinIO"
export Storage__Endpoint="http://localhost:9000"
export Storage__BucketName="carf-documents"
export Storage__AccessKey="minioadmin"
export Storage__SecretKey="minioadmin"
export Storage__ForcePathStyle="true"
export Hangfire__WorkerCount="2"
export Hangfire__DashboardAuthorization="false"
export RateLimiting__Enabled="false"
export Serilog__MinimumLevel__Default="Debug"
```

### Staging

```bash
export ASPNETCORE_ENVIRONMENT=Staging
export ConnectionStrings__DefaultConnection="Host=staging-db.internal;Port=5432;Database=geoapi_stg;Username=geoapi_stg;Password=***;SSL Mode=Require"
export ConnectionStrings__Redis="staging-redis.internal:6379,password=***,ssl=true"
export Keycloak__Authority="https://auth-staging.carf.gov.br/realms/carf"
export Keycloak__Audience="geoapi"
export Keycloak__RequireHttpsMetadata="true"
export Storage__Provider="S3"
export Storage__Region="sa-east-1"
export Storage__BucketName="carf-documents-staging"
export Storage__AccessKey="AKIA..."
export Storage__SecretKey="***"
export Storage__ForcePathStyle="false"
export Hangfire__WorkerCount="4"
export RateLimiting__Enabled="true"
export RateLimiting__PermitLimit="200"
export Serilog__MinimumLevel__Default="Information"
```

### Production

```bash
export ASPNETCORE_ENVIRONMENT=Production
export ConnectionStrings__DefaultConnection="Host=prod-db.internal;Port=5432;Database=geoapi_prod;Username=geoapi_prod;Password=***;SSL Mode=VerifyFull;Maximum Pool Size=100;Timeout=30"
export ConnectionStrings__Redis="prod-redis.internal:6379,password=***,ssl=true,connectTimeout=5000"
export Keycloak__Authority="https://auth.carf.gov.br/realms/carf"
export Keycloak__Audience="geoapi"
export Keycloak__RequireHttpsMetadata="true"
export Storage__Provider="S3"
export Storage__Region="sa-east-1"
export Storage__BucketName="carf-documents-prod"
export Storage__AccessKey="AKIA..."
export Storage__SecretKey="***"
export Storage__ForcePathStyle="false"
export Hangfire__WorkerCount="8"
export RateLimiting__Enabled="true"
export RateLimiting__PermitLimit="100"
export Serilog__MinimumLevel__Default="Warning"
export Cors__AllowedOrigins__0="https://app.carf.gov.br"
export Cors__AllowedOrigins__1="https://docs.carf.gov.br"
```

---

## Validacao de Variaveis

### Verificar variaveis no startup da aplicacao

O GEOAPI valida variaveis criticas no startup. Se alguma estiver faltando, a API nao inicia e loga o erro:

```
[FATAL] Configuration validation failed:
  - ConnectionStrings:DefaultConnection is required
  - Keycloak:Authority is required
  - Storage:AccessKey is required
```

### Variaveis obrigatorias (API nao inicia sem elas)

| Variavel | Motivo |
|----------|--------|
| `ConnectionStrings__DefaultConnection` | Sem banco nao ha API |
| `ConnectionStrings__Redis` | Cache e sessao dependem do Redis |
| `Keycloak__Authority` | Autenticacao JWT depende do Keycloak |
| `Keycloak__Audience` | Validacao de audience no token |
| `Storage__AccessKey` | Upload/download de documentos |
| `Storage__SecretKey` | Upload/download de documentos |

### Verificar em runtime qual valor esta ativo

```bash
# Endpoint de diagnostico (apenas Development)
curl http://localhost:5001/api/v1/admin/config-check \
  -H "Authorization: Bearer $TOKEN"
```

> Este endpoint retorna as secoes de configuracao (sem valores sensiveis) para diagnostico. Desabilitado em Staging/Production.

---

## Referencias

| Recurso | Link |
|---------|------|
| ASP.NET Core Configuration | learn.microsoft.com/aspnet/core/fundamentals/configuration |
| Environment Variables Provider | learn.microsoft.com/aspnet/core/fundamentals/configuration/#environment-variables |
| User Secrets | learn.microsoft.com/aspnet/core/security/app-secrets |
| Kubernetes ConfigMaps | kubernetes.io/docs/concepts/configuration/configmap |
| Kubernetes Secrets | kubernetes.io/docs/concepts/configuration/secret |
| Referencia appsettings | [02-appsettings-reference.md](./02-appsettings-reference.md) |
| Docker Compose | [../../HOW-TO/04-docker-compose-reference.md](../../HOW-TO/04-docker-compose-reference.md) |
