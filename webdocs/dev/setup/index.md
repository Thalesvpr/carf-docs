# Setup Inicial

Guia passo a passo para configurar o ambiente de desenvolvimento do CARF.

## Pré-requisitos

### Para Todos os Desenvolvedores

- **Git** (versão 2.30+): https://git-scm.com/downloads
- **GitHub CLI** (opcional): https://cli.github.com/

### Por Projeto

| Projeto | Requisitos |
|---------|------------|
| **GEOAPI** (Backend) | .NET 9 SDK, PostgreSQL 16 + PostGIS, Docker (opcional) |
| **GEOWEB** (Frontend) | Node.js 20+, npm/yarn |
| **REURBCAD** (Mobile) | Node.js 20+, React Native CLI, Android Studio/Xcode |
| **GEOGIS** (Plugin) | Python 3.x, QGIS 3.x |
| **WEBDOCS** (Docs) | Node.js 20+, npm/yarn |

## Passo 1: Clonar Documentação

```bash
git clone https://github.com/Thalesvpr/carf-docs.git CARF
cd CARF
```

## Passo 2: Clonar Projetos

Clone apenas os repositórios que você precisa:

```bash
# Backend .NET (Backend Team)
git clone https://github.com/Thalesvpr/carf-geoapi.git PROJECTS/GEOAPI/SRC-CODE

# Frontend React (Frontend Team)
git clone https://github.com/Thalesvpr/carf-geoweb.git PROJECTS/GEOWEB/SRC-CODE

# Mobile React Native (Mobile Team)
git clone https://github.com/Thalesvpr/carf-reurbcad.git PROJECTS/REURBCAD/SRC-CODE

# Plugin QGIS (GIS Team)
git clone https://github.com/Thalesvpr/carf-geogis.git PROJECTS/GEOGIS/SRC-CODE

# Portal de documentação
git clone https://github.com/Thalesvpr/carf-webdocs.git PROJECTS/WEBDOCS/SRC-CODE
```

## Passo 3: Setup por Projeto

### Backend (GEOAPI)

```bash
cd CARF/PROJECTS/GEOAPI/SRC-CODE

# Restaurar dependências
dotnet restore

# Build
dotnet build

# Executar
dotnet run --project src/Gateway

# Executar migrations (configurar connection string antes)
dotnet ef database update --project src/Infrastructure --startup-project src/Gateway
```

**Connection String**: Configure em `src/Gateway/appsettings.Development.json`

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Database=carf;Username=postgres;Password=sua_senha"
  }
}
```

### Frontend (GEOWEB)

```bash
cd CARF/PROJECTS/GEOWEB/SRC-CODE

# Instalar dependências
npm install

# Criar .env.local
cat > .env.local <<EOF
VITE_API_URL=http://localhost:5000/api
VITE_KEYCLOAK_URL=http://localhost:8080
VITE_KEYCLOAK_REALM=carf
VITE_KEYCLOAK_CLIENT_ID=geoweb
EOF

# Dev server
npm run dev
```

### Mobile (REURBCAD)

```bash
cd CARF/PROJECTS/REURBCAD/SRC-CODE

# Instalar dependências
npm install

# Criar .env
cat > .env <<EOF
API_URL=http://localhost:5000/api
KEYCLOAK_URL=http://localhost:8080
KEYCLOAK_REALM=carf
KEYCLOAK_CLIENT_ID=reurbcad
EOF

# Android
npx react-native run-android

# iOS (macOS apenas)
npx react-native run-ios
```

### Portal Docs (WEBDOCS)

```bash
cd CARF/PROJECTS/WEBDOCS/SRC-CODE/webdocs

# Instalar dependências
npm install

# Dev server
npm run dev
```

## Infraestrutura Local (Docker)

Para rodar PostgreSQL + Keycloak localmente:

```bash
# TODO: Adicionar docker-compose.yml
docker-compose up -d
```

## Verificação

Verifique se tudo está funcionando:

```bash
# Backend
curl http://localhost:5000/api/health

# Frontend
# Acesse http://localhost:3000

# Docs
# Acesse http://localhost:5173
```

## Troubleshooting

### Erro: "Connection refused" no PostgreSQL

Verifique se o PostgreSQL está rodando:

```bash
# Linux/Mac
sudo service postgresql status

# Windows
# Verifique no Services.msc
```

### Erro: Node version incompatível

Use nvm para gerenciar versões:

```bash
nvm install 20
nvm use 20
```

## Próximos Passos

- Ver [Arquitetura](/dev/arquitetura/)
- Consultar [API Reference](/dev/api/)
- Ler [Guias Técnicos](/dev/guias/)
