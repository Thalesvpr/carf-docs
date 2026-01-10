# Setup Dev Environment - GEOAPI

## Requisitos

Setup do ambiente de desenvolvimento GEOAPI requer .NET 9 SDK, Docker Desktop para PostgreSQL + PostGIS, e IDE (Visual Studio 2022 ou VS Code com extensão C# Dev Kit), clonar repositório `git clone https://github.com/user/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE`, subir banco com `docker-compose up -d` criando container `geoapi-db` PostgreSQL 16 + PostGIS 3.4 em porta 5432, criar migration inicial com `dotnet ef migrations add Initial` gerando schema em `Migrations/`, aplicar migrations com `dotnet ef database update` criando tabelas e RLS policies, configurar Keycloak local em `http://localhost:8080` importando realm `carf-realm.json` de `CENTRAL/INTEGRATION/KEYCLOAK/runbooks/`, e rodar API com `dotnet run` abrindo Swagger em `https://localhost:7001/swagger`.

## Passo a Passo

### 1. Instalar .NET 9 SDK

```bash
# Windows
winget install Microsoft.DotNet.SDK.9

# macOS
brew install dotnet-sdk

# Linux (Ubuntu)
sudo apt-get update
sudo apt-get install -y dotnet-sdk-9.0

# Verificar instalação
dotnet --version  # Deve retornar 9.0.x
```

### 2. Instalar Docker Desktop

- **Windows/macOS:** https://www.docker.com/products/docker-desktop/
- **Linux:** https://docs.docker.com/engine/install/

Verificar instalação:

```bash
docker --version
docker-compose --version
```

### 3. Clonar Repositório

```bash
git clone https://github.com/user/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
cd PROJECTS/GEOAPI/SRC-CODE
```

### 4. Subir PostgreSQL + PostGIS

```bash
# Criar docker-compose.yml na raiz do projeto
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgis/postgis:16-3.4
    container_name: geoapi-db
    environment:
      POSTGRES_DB: geoapi_dev
      POSTGRES_USER: geoapi
      POSTGRES_PASSWORD: dev123
      PGDATA: /var/lib/postgresql/data
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U geoapi"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
EOF

# Subir container
docker-compose up -d

# Verificar que está rodando
docker ps  # Deve mostrar geoapi-db com status "healthy"
```

### 5. Configurar Connection String

```json
// appsettings.Development.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=geoapi_dev;Username=geoapi;Password=dev123"
  },
  "Keycloak": {
    "Authority": "http://localhost:8080/realms/carf",
    "Audience": "geoapi",
    "RequireHttpsMetadata": false
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.EntityFrameworkCore": "Warning"
    }
  }
}
```

### 6. Criar e Aplicar Migrations

```bash
# Navegar para projeto Infrastructure
cd src/Carf.GEOAPI.Infrastructure

# Criar migration inicial
dotnet ef migrations add Initial \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext

# Aplicar migration
dotnet ef database update \
  --startup-project ../Carf.GEOAPI.Gateway \
  --context AppDbContext

# Verificar que tabelas foram criadas
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "\dt"
```

### 7. Configurar Keycloak

```bash
# Subir Keycloak via Docker
docker run -d \
  --name keycloak \
  -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  quay.io/keycloak/keycloak:23.0 \
  start-dev

# Aguardar inicialização (30-60s)
# Acessar http://localhost:8080
# Login: admin / admin

# Importar realm
# 1. Clicar em "Select realm" dropdown
# 2. Clicar em "Create Realm"
# 3. Clicar em "Browse" e selecionar CENTRAL/INTEGRATION/KEYCLOAK/runbooks/carf-realm.json
# 4. Clicar em "Create"
```

**OU** importar via CLI:

```bash
# Copiar realm.json para container
docker cp CENTRAL/INTEGRATION/KEYCLOAK/runbooks/carf-realm.json keycloak:/tmp/

# Importar
docker exec keycloak /opt/keycloak/bin/kc.sh import \
  --file /tmp/carf-realm.json \
  --override true
```

### 8. Rodar API

```bash
# Voltar para raiz do projeto
cd PROJECTS/GEOAPI/SRC-CODE

# Restaurar dependências
dotnet restore

# Build
dotnet build

# Rodar projeto Gateway
cd src/Carf.GEOAPI.Gateway
dotnet run

# API rodando em:
# - HTTPS: https://localhost:7001
# - HTTP: http://localhost:5001
# - Swagger: https://localhost:7001/swagger
```

### 9. Configurar IDE

#### Visual Studio 2022

1. Abrir `Carf.GEOAPI.sln`
2. Definir `Carf.GEOAPI.Gateway` como startup project
3. F5 para rodar com debugger

#### VS Code

Instalar extensões:

```bash
code --install-extension ms-dotnettools.csharp
code --install-extension ms-dotnettools.csdevkit
code --install-extension formulahendry.dotnet-test-explorer
```

Configurar `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch GEOAPI",
      "type": "coreclr",
      "request": "launch",
      "preLaunchTask": "build",
      "program": "${workspaceFolder}/src/Carf.GEOAPI.Gateway/bin/Debug/net9.0/Carf.GEOAPI.Gateway.dll",
      "args": [],
      "cwd": "${workspaceFolder}/src/Carf.GEOAPI.Gateway",
      "stopAtEntry": false,
      "env": {
        "ASPNETCORE_ENVIRONMENT": "Development"
      }
    }
  ]
}
```

### 10. Verificar Setup

```bash
# 1. Health check
curl https://localhost:7001/health
# Deve retornar: {"status":"Healthy"}

# 2. Swagger UI
# Abrir https://localhost:7001/swagger
# Deve mostrar todos os endpoints

# 3. Database connectivity
curl https://localhost:7001/health/db
# Deve retornar: {"status":"Healthy","database":"Connected"}
```

## Troubleshooting

### Erro: Port 5432 already in use

```bash
# Parar PostgreSQL local
# Windows: services.msc → PostgreSQL → Stop
# macOS/Linux: sudo systemctl stop postgresql

# OU trocar porta no docker-compose.yml
ports:
  - "5433:5432"  # Usar 5433 ao invés de 5432
```

### Erro: Migrations failing

```bash
# Deletar banco e recriar
docker exec -it geoapi-db psql -U postgres -c "DROP DATABASE geoapi_dev;"
docker exec -it geoapi-db psql -U postgres -c "CREATE DATABASE geoapi_dev OWNER geoapi;"

# Aplicar migrations novamente
dotnet ef database update --startup-project ../Carf.GEOAPI.Gateway
```

### Erro: Keycloak not accessible

```bash
# Verificar que container está rodando
docker ps | grep keycloak

# Ver logs
docker logs keycloak

# Reiniciar container
docker restart keycloak
```

## Referências

- [.NET 9 Installation](https://dotnet.microsoft.com/download/dotnet/9.0)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Entity Framework Core Tools](https://learn.microsoft.com/en-us/ef/core/cli/dotnet)
- [CENTRAL/INTEGRATION/DATABASE/README.md](../../../../CENTRAL/INTEGRATION/DATABASE/README.md)
- [CENTRAL/INTEGRATION/KEYCLOAK/03-docker-setup.md](../../../../CENTRAL/INTEGRATION/KEYCLOAK/03-docker-setup.md)
