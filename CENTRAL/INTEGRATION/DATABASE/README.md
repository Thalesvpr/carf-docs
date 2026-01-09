# PostgreSQL + PostGIS Configuration

Configuração do banco de dados PostgreSQL com extensão PostGIS para o CARF.

## Visão Geral

- **PostgreSQL 16** - Banco de dados relacional
- **PostGIS 3.4** - Extensão geoespacial
- **Row-Level Security (RLS)** - Isolamento multi-tenant
- **Docker Compose** - Setup local

## Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgis/postgis:16-3.4
    container_name: carf-postgres
    environment:
      POSTGRES_DB: carf
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

## Init Scripts

### 01-enable-postgis.sql

```sql
-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS postgis_topology;

-- Verify PostGIS version
SELECT PostGIS_Version();
```

### 02-enable-rls.sql

```sql
-- Enable Row-Level Security for multi-tenancy
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE holders ENABLE ROW LEVEL SECURITY;
ALTER TABLE communities ENABLE ROW LEVEL SECURITY;

-- Create RLS policy
CREATE POLICY tenant_isolation_policy ON units
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

CREATE POLICY tenant_isolation_policy ON holders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);

CREATE POLICY tenant_isolation_policy ON communities
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Connection String

### Desenvolvimento

```
Host=localhost;Port=5432;Database=carf;Username=postgres;Password=postgres
```

### Produção

```
Host=<azure-postgres>.postgres.database.azure.com;Port=5432;Database=carf;Username=<user>;Password=<secret>
```

## Configuração GEOAPI

### appsettings.json

```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=localhost;Port=5432;Database=carf;Username=postgres;Password=postgres"
  }
}
```

### Program.cs

```csharp
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(
        builder.Configuration.GetConnectionString("DefaultConnection"),
        x => x.UseNetTopologySuite()  // PostGIS support
    )
);
```

## Migrations

```bash
# Add migration
dotnet ef migrations add MigrationName \
  --project src/Infrastructure \
  --startup-project src/Gateway

# Apply migrations
dotnet ef database update \
  --project src/Infrastructure \
  --startup-project src/Gateway
```

## Comandos Úteis

```bash
# Start PostgreSQL
docker-compose up -d

# Stop PostgreSQL
docker-compose down

# Logs
docker logs -f carf-postgres

# Connect to database
docker exec -it carf-postgres psql -U postgres -d carf

# Backup
docker exec carf-postgres pg_dump -U postgres carf > backup.sql

# Restore
docker exec -i carf-postgres psql -U postgres carf < backup.sql
```

## Ver Também

- [GEOAPI Database Setup](../../../PROJECTS/GEOAPI/DOCS/HOW-TO/database-setup.md)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
