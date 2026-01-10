# Build and Run - GEOAPI

## Build do Projeto

Build do GEOAPI usa `dotnet build` compilando solução completa (Domain, Application, Infrastructure, Gateway layers) gerando assemblies em `bin/Debug/net9.0/`, rodar testes com `dotnet test` executando unit tests (Domain, Application) e integration tests (Infrastructure, Gateway) com coverage mínimo de 80%, rodar migrations com `dotnet ef database update` aplicando schemas pendentes, e iniciar API com `dotnet run --project src/Carf.GEOAPI.Gateway` abrindo Swagger UI em `https://localhost:7001/swagger` para testar endpoints interativamente, variáveis de ambiente configuradas em `appsettings.Development.json` incluindo connection string PostgreSQL, Keycloak URL, JWT secret, e CORS origins.

## Comandos de Build

### Build Completo

```bash
# Na raiz do projeto
dotnet build

# Build específico de um projeto
dotnet build src/Carf.GEOAPI.Domain
dotnet build src/Carf.GEOAPI.Application
dotnet build src/Carf.GEOAPI.Infrastructure
dotnet build src/Carf.GEOAPI.Gateway

# Build em Release mode
dotnet build --configuration Release
```

### Clean

```bash
# Limpar todos os artefatos de build
dotnet clean

# Limpar e rebuildar
dotnet clean && dotnet build
```

### Restore

```bash
# Restaurar dependências NuGet
dotnet restore

# Forçar redownload de packages
dotnet restore --force
```

## Rodar API

### Development Mode

```bash
# Rodar com hot reload
dotnet watch run --project src/Carf.GEOAPI.Gateway

# Rodar sem hot reload
dotnet run --project src/Carf.GEOAPI.Gateway

# Rodar com porta específica
dotnet run --project src/Carf.GEOAPI.Gateway --urls "https://localhost:8001"
```

### Variáveis de Ambiente

```bash
# Definir ambiente
export ASPNETCORE_ENVIRONMENT=Development  # Linux/macOS
set ASPNETCORE_ENVIRONMENT=Development     # Windows

# Rodar com variável inline
ASPNETCORE_ENVIRONMENT=Staging dotnet run --project src/Carf.GEOAPI.Gateway
```

### Production Mode

```bash
# Build Release
dotnet build --configuration Release

# Rodar
dotnet run --project src/Carf.GEOAPI.Gateway --configuration Release --no-build

# OU executar DLL diretamente
dotnet src/Carf.GEOAPI.Gateway/bin/Release/net9.0/Carf.GEOAPI.Gateway.dll
```

## Migrations

### Criar Migration

```bash
cd src/Carf.GEOAPI.Infrastructure

# Criar nova migration
dotnet ef migrations add <MigrationName> \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext

# Exemplo
dotnet ef migrations add AddHolderPhoneColumn \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext
```

### Aplicar Migrations

```bash
# Aplicar todas as migrations pendentes
dotnet ef database update \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext

# Aplicar até migration específica
dotnet ef database update <MigrationName> \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext

# Reverter todas as migrations (CUIDADO!)
dotnet ef database update 0 \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext
```

### Gerar SQL Script

```bash
# Gerar script SQL das migrations
dotnet ef migrations script \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext \
  --output migrations.sql

# Script idempotente (pode ser executado múltiplas vezes)
dotnet ef migrations script \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext \
  --idempotent \
  --output migrations.sql
```

### Remover Migration

```bash
# Remover última migration (antes de aplicar)
dotnet ef migrations remove \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext

# Forçar remoção (depois de aplicada)
dotnet ef migrations remove \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext \
  --force
```

## Testes

### Rodar Todos os Testes

```bash
# Na raiz do projeto
dotnet test

# Com logger verboso
dotnet test --logger "console;verbosity=detailed"

# Com filtro por categoria
dotnet test --filter "Category=Unit"
dotnet test --filter "Category=Integration"
```

### Testes por Projeto

```bash
# Unit tests do Domain
dotnet test tests/Carf.GEOAPI.Domain.Tests

# Unit tests do Application
dotnet test tests/Carf.GEOAPI.Application.Tests

# Integration tests
dotnet test tests/Carf.GEOAPI.Integration.Tests
```

### Coverage

```bash
# Instalar ferramenta de coverage
dotnet tool install --global dotnet-coverage

# Rodar testes com coverage
dotnet test --collect:"XPlat Code Coverage"

# Gerar relatório HTML
reportgenerator \
  -reports:"**/coverage.cobertura.xml" \
  -targetdir:"coverage-report" \
  -reporttypes:Html

# Abrir relatório
open coverage-report/index.html  # macOS
start coverage-report/index.html # Windows
xdg-open coverage-report/index.html # Linux
```

### Testes Específicos

```bash
# Por nome da classe
dotnet test --filter "FullyQualifiedName~UnitTests"

# Por nome do método
dotnet test --filter "Name=CreateUnit_ShouldSucceed"

# Múltiplos filtros
dotnet test --filter "Category=Unit&Priority=High"
```

## Docker

### Build Imagem

```bash
# Build imagem Docker
docker build -t carf-geoapi:latest .

# Build com argumentos
docker build \
  --build-arg ASPNETCORE_ENVIRONMENT=Production \
  -t carf-geoapi:v1.0.0 \
  .
```

### Rodar Container

```bash
# Rodar container
docker run -d \
  --name geoapi \
  -p 8080:8080 \
  -e ASPNETCORE_ENVIRONMENT=Production \
  -e ConnectionStrings__DefaultConnection="Host=postgres;..." \
  carf-geoapi:latest

# Ver logs
docker logs -f geoapi

# Parar container
docker stop geoapi

# Remover container
docker rm geoapi
```

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      ASPNETCORE_ENVIRONMENT: Production
      ConnectionStrings__DefaultConnection: "Host=postgres;Database=geoapi;Username=geoapi;Password=secure123"
    depends_on:
      postgres:
        condition: service_healthy

  postgres:
    image: postgis/postgis:16-3.4
    environment:
      POSTGRES_DB: geoapi
      POSTGRES_USER: geoapi
      POSTGRES_PASSWORD: secure123
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U geoapi"]
      interval: 5s
      timeout: 5s
      retries: 5
```

```bash
# Subir stack completa
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar stack
docker-compose down
```

## Publicação

### Publish Local

```bash
# Publish Release
dotnet publish src/Carf.GEOAPI.Gateway \
  --configuration Release \
  --output ./publish

# Rodar publicado
cd publish
dotnet Carf.GEOAPI.Gateway.dll
```

### Publish Self-Contained

```bash
# Incluir runtime .NET
dotnet publish src/Carf.GEOAPI.Gateway \
  --configuration Release \
  --runtime linux-x64 \
  --self-contained true \
  --output ./publish-linux

# Executável nativo
./publish-linux/Carf.GEOAPI.Gateway
```

### Publish para Azure

```bash
# Instalar Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login
az login

# Publish
az webapp up \
  --name carf-geoapi \
  --resource-group carf-rg \
  --runtime "DOTNETCORE:9.0"
```

## Performance

### Benchmark

```bash
# Instalar BenchmarkDotNet
dotnet add package BenchmarkDotNet

# Rodar benchmarks
dotnet run --project tests/Carf.GEOAPI.Benchmarks \
  --configuration Release
```

### Profiling

```bash
# Instalar dotnet-trace
dotnet tool install --global dotnet-trace

# Capturar trace
dotnet-trace collect --process-id <PID>

# Analisar com PerfView (Windows)
PerfView.exe trace.nettrace
```

## Checklist Pré-Deploy

```bash
# 1. Build sem erros
dotnet build --configuration Release

# 2. Testes passando
dotnet test

# 3. Coverage > 80%
dotnet test --collect:"XPlat Code Coverage"

# 4. Migrations aplicadas
dotnet ef database update

# 5. Swagger documentado
# Abrir https://localhost:7001/swagger
# Verificar que todos os endpoints estão documentados

# 6. Health checks funcionando
curl https://localhost:7001/health

# 7. Logs estruturados
# Verificar que logs aparecem em formato JSON

# 8. Variáveis de ambiente configuradas
# Verificar appsettings.Production.json
```

## Referências

- [.NET CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/)
- [Entity Framework Core Tools](https://learn.microsoft.com/en-us/ef/core/cli/dotnet)
- [Docker Build](https://docs.docker.com/engine/reference/commandline/build/)
- [ASP.NET Core Deployment](https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/)
