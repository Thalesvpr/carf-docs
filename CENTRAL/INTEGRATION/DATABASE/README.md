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

---

**Última atualização:** 2026-01-14

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto
