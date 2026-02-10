---
type: leaf
status: review
updated: 2026-02-08
---

# Setup Ambiente de Desenvolvimento - GEOAPI

Guia completo passo a passo para configurar o ambiente de desenvolvimento local do GEOAPI (.NET 9, PostgreSQL+PostGIS, Redis, MinIO, Keycloak).

---

## 1. Pre-requisitos

### Ferramentas Obrigatorias

| Ferramenta | Versao Minima | Verificacao | Download |
|------------|--------------|-------------|----------|
| .NET 9 SDK | 9.0.x | `dotnet --version` | dotnet.microsoft.com/download |
| Docker Desktop | 4.x | `docker --version` | docker.com/products/docker-desktop |
| Docker Compose | 2.x (incluso Docker Desktop) | `docker compose version` | incluso no Docker Desktop |
| Git | 2.x | `git --version` | git-scm.com |
| EF Core CLI | 9.x | `dotnet ef --version` | via `dotnet tool install` |

### IDE (escolher uma)

| IDE | Versao Minima | Notas |
|-----|--------------|-------|
| JetBrains Rider | 2024.1+ | Recomendado - melhor suporte .NET no geral |
| Visual Studio 2022 | 17.8+ | Requer workload "ASP.NET and web development" |
| VS Code | Latest | Requer extensoes C# Dev Kit + C# |

### Instalacao do .NET 9 SDK

**Windows (winget):**

```bash
winget install Microsoft.DotNet.SDK.9
```

**macOS (Homebrew):**

```bash
brew install dotnet-sdk
```

**Linux (Ubuntu/Debian):**

```bash
sudo apt-get update
sudo apt-get install -y dotnet-sdk-9.0
```

**Verificacao (todos os SOs):**

```bash
dotnet --version
# Esperado: 9.0.xxx (qualquer patch)
```

### Instalacao do EF Core CLI

```bash
dotnet tool install --global dotnet-ef
```

**Verificacao:**

```bash
dotnet ef --version
# Esperado: Entity Framework Core .NET Command-line Tools 9.x.x
```

> **Nota:** Se ja tem versao anterior instalada, atualize com `dotnet tool update --global dotnet-ef`.

---

## 2. Clonar Repositorio

```bash
git clone https://github.com/org/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE
cd PROJECTS/GEOAPI/SRC-CODE
```

**Verificacao:**

```bash
ls -la
# Esperado: ver pastas src/, tests/, docker-compose.yml, Carf.GeoApi.sln
```

**Estrutura esperada:**

```
PROJECTS/GEOAPI/SRC-CODE/
├── src/
│   ├── Carf.GeoApi.Domain/
│   ├── Carf.GeoApi.Application/
│   ├── Carf.GeoApi.Infrastructure/
│   └── Carf.GeoApi.Gateway/          ← startup project
├── tests/
│   ├── Carf.GeoApi.Domain.Tests/
│   ├── Carf.GeoApi.Application.Tests/
│   ├── Carf.GeoApi.Infrastructure.Tests/
│   └── Carf.GeoApi.E2E.Tests/
├── docker-compose.yml
├── docker-compose.override.yml
├── Carf.GeoApi.sln
└── .env.example
```

---

## 3. Subir Infraestrutura (Docker Compose)

### 3.1 Configurar variaveis de ambiente

```bash
cp .env.example .env
```

Editar `.env` conforme necessario (valores padrao funcionam para desenvolvimento local).

### 3.2 Subir todos os servicos

```bash
docker compose up -d
```

**Saida esperada:**

```
[+] Running 5/5
 ✔ Network carf-network     Created
 ✔ Container geoapi-db      Started
 ✔ Container geoapi-redis   Started
 ✔ Container geoapi-minio   Started
 ✔ Container geoapi-keycloak Started
```

### 3.3 Verificar saude dos containers

```bash
docker compose ps
```

**Saida esperada (todos `healthy` ou `running`):**

```
NAME               IMAGE                           STATUS
geoapi-db          postgis/postgis:16-3.4         Up (healthy)
geoapi-redis       redis:7-alpine                 Up (healthy)
geoapi-minio       minio/minio:latest             Up (healthy)
geoapi-keycloak    quay.io/keycloak/keycloak:23.0 Up (healthy)
```

> **Nota:** Keycloak pode levar 30-60 segundos para ficar `healthy`. Aguardar antes de prosseguir.

### 3.4 Verificar conectividade individual

**PostgreSQL:**

```bash
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "SELECT PostGIS_Version();"
# Esperado: 3.4 USE_GEOS=1 USE_PROJ=1 ...
```

**Redis:**

```bash
docker exec -it geoapi-redis redis-cli ping
# Esperado: PONG
```

**MinIO:**

```bash
# Console web: http://localhost:9001
# Login: minioadmin / minioadmin
```

**Keycloak:**

```bash
# Console admin: http://localhost:8080
# Login: admin / admin
```

> Ver [04-docker-compose-reference.md](./04-docker-compose-reference.md) para detalhes completos de cada servico.

---

## 4. Configurar appsettings

### 4.1 Copiar template de desenvolvimento

```bash
cd src/Carf.GeoApi.Gateway
cp appsettings.Development.json.example appsettings.Development.json
```

### 4.2 Conteudo minimo do appsettings.Development.json

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
    "AccessKey": "minioadmin",
    "SecretKey": "minioadmin",
    "ForcePathStyle": true
  },
  "Hangfire": {
    "SchemaName": "hangfire",
    "WorkerCount": 2,
    "Queues": ["default", "sync", "reports"]
  },
  "Cors": {
    "AllowedOrigins": [
      "http://localhost:3000",
      "http://localhost:4321"
    ]
  },
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.EntityFrameworkCore": "Warning",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

> Ver [02-appsettings-reference.md](../ARCHITECTURE/LAYERS/PRESENTATION/CONFIGURATION/02-appsettings-reference.md) para referencia completa de todas as chaves.

---

## 5. Rodar Migrations

### 5.1 Aplicar todas as migrations pendentes

```bash
cd PROJECTS/GEOAPI/SRC-CODE
dotnet ef database update \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

**Saida esperada:**

```
Build started...
Build succeeded.
Applying migration '20240101000000_Initial'.
Applying migration '20240115000000_AddPostGISExtension'.
...
Done.
```

### 5.2 Verificar tabelas criadas

```bash
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev -c "\dt"
```

**Tabelas esperadas (minimo):**

```
 Schema |          Name           | Type  | Owner
--------+-------------------------+-------+-------
 public | units                   | table | geoapi
 public | holders                 | table | geoapi
 public | communities             | table | geoapi
 public | legitimation_requests   | table | geoapi
 public | documents               | table | geoapi
 public | teams                   | table | geoapi
 public | blocks                  | table | geoapi
 public | __EFMigrationsHistory   | table | geoapi
```

> Ver [05-database-migrations.md](./05-database-migrations.md) para guia completo de migrations.

---

## 6. Configurar Keycloak

### 6.1 Importar realm CARF

**Opcao A - Via UI Admin:**

1. Acessar `http://localhost:8080` e fazer login (admin/admin)
2. No dropdown de realm (canto superior esquerdo), clicar "Create realm"
3. Clicar "Browse..." e selecionar `PROJECTS/KEYCLOAK/DOCS/CONFIG/realm-export.json`
4. Clicar "Create"

**Opcao B - Via CLI:**

```bash
# Copiar arquivo de realm para o container
docker cp PROJECTS/KEYCLOAK/DOCS/CONFIG/realm-export.json geoapi-keycloak:/tmp/

# Importar realm
docker exec geoapi-keycloak /opt/keycloak/bin/kc.sh import \
  --file /tmp/realm-export.json \
  --override true
```

### 6.2 Criar usuario de teste

1. Acessar `http://localhost:8080/admin/master/console/#/carf/users`
2. Clicar "Add user"
3. Preencher:
   - Username: `dev@carf.local`
   - Email: `dev@carf.local`
   - First Name: `Dev`
   - Last Name: `User`
   - Email Verified: ON
4. Clicar "Create"
5. Aba "Credentials" → "Set password":
   - Password: `dev123`
   - Temporary: OFF
6. Aba "Role mappings" → "Assign role":
   - Selecionar `coordinator` (ou role desejada)

### 6.3 Obter token de teste

```bash
curl -X POST http://localhost:8080/realms/carf/protocol/openid-connect/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password" \
  -d "client_id=geoapi" \
  -d "username=dev@carf.local" \
  -d "password=dev123"
```

**Saida esperada:** JSON com `access_token`, `refresh_token`, `expires_in`.

### 6.4 Verificar token

Copiar `access_token` e decodificar em [jwt.io](https://jwt.io) para verificar claims:
- `sub` - ID do usuario
- `realm_access.roles` - Roles atribuidas
- `tenant_id` - ID do tenant (se mapeado)
- `aud` - Deve conter `geoapi`

---

## 7. Rodar a API

### 7.1 Restaurar dependencias

```bash
cd PROJECTS/GEOAPI/SRC-CODE
dotnet restore
```

### 7.2 Build do projeto

```bash
dotnet build
```

**Saida esperada:**

```
Build succeeded.
    0 Warning(s)
    0 Error(s)
```

### 7.3 Rodar em modo desenvolvimento

```bash
cd src/Carf.GeoApi.Gateway
dotnet run
```

**Saida esperada:**

```
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: https://localhost:7001
info: Microsoft.Hosting.Lifetime[14]
      Now listening on: http://localhost:5001
```

### 7.4 Rodar com hot reload (recomendado para desenvolvimento)

```bash
cd src/Carf.GeoApi.Gateway
dotnet watch run
```

> Hot reload recompila automaticamente ao salvar alteracoes em arquivos `.cs`.

---

## 8. Verificar Setup

### 8.1 Health check

```bash
curl http://localhost:5001/health
```

**Esperado:**

```json
{
  "status": "Healthy",
  "entries": {
    "postgresql": { "status": "Healthy" },
    "redis": { "status": "Healthy" },
    "storage": { "status": "Healthy" },
    "keycloak": { "status": "Healthy" }
  }
}
```

### 8.2 Swagger UI

Abrir no navegador: `https://localhost:7001/swagger`

Deve mostrar todos os endpoints agrupados por controller (Units, Holders, Communities, etc.).

### 8.3 Testar endpoint autenticado

```bash
# Obter token (ver passo 6.3)
TOKEN="eyJhbGciOiJSUz..."

# Chamar endpoint protegido
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:5001/api/v1/communities
```

**Esperado:** `200 OK` com array JSON (pode estar vazio se nao ha dados seed).

### 8.4 Verificar Hangfire Dashboard

Abrir no navegador: `https://localhost:7001/hangfire`

> Em modo desenvolvimento, o dashboard e acessivel sem autenticacao.

---

## 9. Configurar IDE

### JetBrains Rider

1. **Abrir solution:** File → Open → selecionar `Carf.GeoApi.sln`
2. **Configurar Run/Debug:**
   - Run → Edit Configurations → Add New → .NET Project
   - Project: `Carf.GeoApi.Gateway`
   - Environment variables: `ASPNETCORE_ENVIRONMENT=Development`
3. **Extensoes recomendadas:**
   - .NET Core User Secrets (builtin)
   - Database Tools (builtin) - conectar ao PostgreSQL local
4. **Conectar ao banco:**
   - Database → + → Data Source → PostgreSQL
   - Host: localhost, Port: 5432, User: geoapi, Password: dev123, Database: geoapi_dev

### Visual Studio 2022

1. **Abrir solution:** File → Open → Project/Solution → `Carf.GeoApi.sln`
2. **Definir startup project:**
   - Clicar com botao direito em `Carf.GeoApi.Gateway` → "Set as Startup Project"
3. **Configurar launch profile:**
   - Properties → launchSettings.json ja deve conter perfil HTTPS
4. **Debugging:** F5 para iniciar com debugger
5. **Extensoes recomendadas:**
   - EF Core Power Tools
   - SwitchStartupProject

### VS Code

1. **Extensoes obrigatorias:**

```bash
code --install-extension ms-dotnettools.csharp
code --install-extension ms-dotnettools.csdevkit
code --install-extension formulahendry.dotnet-test-explorer
```

2. **Criar `.vscode/launch.json`:**

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
      }
    }
  ]
}
```

3. **Criar `.vscode/tasks.json`:**

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

---

## Troubleshooting

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| Port 5432 already in use | PostgreSQL local rodando | **Windows:** `services.msc` → PostgreSQL → Stop. **macOS/Linux:** `sudo systemctl stop postgresql`. Alternativa: trocar porta no `docker-compose.yml` para `5433:5432` e atualizar connection string |
| Migrations falhando | Banco em estado inconsistente | Recriar banco: `docker exec -it geoapi-db psql -U postgres -c "DROP DATABASE geoapi_dev; CREATE DATABASE geoapi_dev OWNER geoapi;"` e re-aplicar migrations |
| Keycloak nao acessivel | Container ainda inicializando | Verificar: `docker logs geoapi-keycloak`. Aguardar 30-60s. Se persistir: `docker compose restart keycloak` |
| `dotnet ef` nao encontrado | CLI nao instalada | `dotnet tool install --global dotnet-ef` |
| SSL certificate error (HTTPS) | Certificado dev nao confiavel | `dotnet dev-certs https --trust` |
| Docker permission denied (Linux) | Usuario fora do grupo docker | `sudo usermod -aG docker $USER` e re-login |
| Build falha com package errors | Pacotes NuGet nao restaurados | `dotnet restore` na raiz da solution |
| Hot reload nao funciona | Usando `dotnet run` ao inves de `dotnet watch` | Usar `dotnet watch run` para hot reload |
| EF Core primeira execucao lenta | Compilacao de queries (cold start) | Normal - execucoes subsequentes serao mais rapidas |
| Antivirus bloqueando Docker (Windows) | Firewall/Defender bloqueando containers | Adicionar excecoes para `docker.exe` e portas 5432, 6379, 8080, 9000 |

---

## Referencias

| Recurso | URL |
|---------|-----|
| .NET 9 SDK | dotnet.microsoft.com/download |
| Docker Desktop | docker.com/products/docker-desktop |
| EF Core CLI | learn.microsoft.com/ef/core/cli/dotnet |
| PostgreSQL + PostGIS | postgis.net/documentation |
| Keycloak Admin | keycloak.org/documentation |
| Configuracao Docker Compose | [04-docker-compose-reference.md](./04-docker-compose-reference.md) |
| Guia Migrations | [05-database-migrations.md](./05-database-migrations.md) |
| Referencia appsettings | [02-appsettings-reference.md](../ARCHITECTURE/LAYERS/PRESENTATION/CONFIGURATION/02-appsettings-reference.md) |
