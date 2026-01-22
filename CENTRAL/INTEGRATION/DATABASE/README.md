---
type: readme
status: rejected
description: "Duplicacao com ADRs e PROJECTS. Cada integracao deve ter UM lugar so. Contem blocos de codigo."
updated: 2026-01-15
---

# DATABASE

Configuração do banco de dados PostgreSQL com extensão PostGIS para o CARF.

## Visão Geral

- **PostgreSQL 16** - Banco de dados relacional
- **PostGIS 3.4** - Extensão geoespacial para geometrias e queries espaciais
- **Row-Level Security (RLS)** - Isolamento automático de dados entre tenants
- **Docker Compose** - Setup para desenvolvimento local

## Docker Compose

O ambiente de desenvolvimento usa a imagem postgis/postgis:16-3.4 com variáveis de ambiente para database, usuário e senha. Um volume persiste os dados e scripts de inicialização habilitam as extensões automaticamente.

Health check com pg_isready garante que o container só é considerado pronto quando aceita conexões.

## Init Scripts

O script 01-enable-postgis.sql habilita as extensões postgis e postgis_topology.

O script 02-enable-rls.sql habilita Row-Level Security nas tabelas units, holders e communities, criando policies que filtram registros automaticamente pelo tenant_id da sessão.

## Connection String

Desenvolvimento: Host=localhost;Port=5432;Database=carf;Username=postgres;Password=postgres

Produção: credenciais gerenciadas via Azure Key Vault ou secrets manager.

## Configuração GEOAPI

O DbContext é registrado com UseNpgsql e UseNetTopologySuite para suporte a tipos geoespaciais, permitindo mapear geometries PostGIS para objetos NetTopologySuite.

## Migrations

```bash
# Adicionar migration
dotnet ef migrations add MigrationName --project src/Infrastructure --startup-project src/Gateway

# Aplicar migrations
dotnet ef database update --project src/Infrastructure --startup-project src/Gateway
```

## Comandos Úteis

```bash
# Iniciar PostgreSQL
docker-compose up -d

# Parar PostgreSQL
docker-compose down

# Visualizar logs
docker logs -f carf-postgres

# Conectar ao database
docker exec -it carf-postgres psql -U postgres -d carf

# Criar backup
docker exec carf-postgres pg_dump -U postgres carf > backup.sql

# Restaurar backup
docker exec -i carf-postgres psql -U postgres -d carf < backup.sql
```


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-rls-setup](./01-rls-setup.md) | RLS Setup |
| [02-postgis-setup](./02-postgis-setup.md) | PostGIS Setup |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/INTEGRATION/DATABASE/init-scripts/README|init-scripts]]

## Documentos

### Em Revisão

- ○ [[CENTRAL/INTEGRATION/DATABASE/01-rls-setup.md|RLS Setup]]
- ○ [[CENTRAL/INTEGRATION/DATABASE/02-postgis-setup.md|PostGIS Setup]]

<!-- CARF-INDEX-END -->
