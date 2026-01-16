# GEOAPI Dockerfile

Multi-stage Dockerfile para build e deploy da API .NET.

## Dockerfile

```dockerfile
# Dockerfile.geoapi

# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY ["src/GEOAPI.Presentation/GEOAPI.Presentation.csproj", "GEOAPI.Presentation/"]
COPY ["src/GEOAPI.Application/GEOAPI.Application.csproj", "GEOAPI.Application/"]
COPY ["src/GEOAPI.Domain/GEOAPI.Domain.csproj", "GEOAPI.Domain/"]
COPY ["src/GEOAPI.Infrastructure/GEOAPI.Infrastructure.csproj", "GEOAPI.Infrastructure/"]
RUN dotnet restore "GEOAPI.Presentation/GEOAPI.Presentation.csproj"

# Copy all source and build
COPY src/ .
WORKDIR /src/GEOAPI.Presentation
RUN dotnet build -c Release -o /app/build

# Stage 2: Publish
FROM build AS publish
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

# Stage 3: Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app

# Install PostGIS client for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r geoapi && useradd -r -g geoapi geoapi
USER geoapi

COPY --from=publish /app/publish .

# Environment
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "GEOAPI.Presentation.dll"]
```

## Otimizações

- **Multi-stage build**: Imagem final ~200MB vs ~2GB com SDK
- **Layer caching**: csproj copiados antes do source para cache de restore
- **Non-root user**: Execução como usuário não privilegiado
- **Health check nativo**: Container auto-reporta saúde

## Build

```bash
# Build local
docker build -f Dockerfile.geoapi -t carf/geoapi:latest .

# Build com tag específica
docker build -f Dockerfile.geoapi -t carf/geoapi:1.2.3 .

# Build com build args
docker build -f Dockerfile.geoapi \
  --build-arg CONFIGURATION=Release \
  -t carf/geoapi:latest .
```

## Variáveis de Ambiente

| Variável | Descrição | Default |
|----------|-----------|---------|
| ASPNETCORE_ENVIRONMENT | Ambiente | Production |
| ConnectionStrings__DefaultConnection | String PostgreSQL | - |
| Keycloak__Authority | URL Keycloak | - |
| Redis__ConnectionString | String Redis | - |

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
