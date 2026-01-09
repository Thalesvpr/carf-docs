# Database

Documentação do schema PostgreSQL + PostGIS e políticas RLS.

## Tecnologias

- **PostgreSQL 16**: Banco de dados relacional
- **PostGIS**: Extensão geoespacial
- **Row-Level Security (RLS)**: Isolamento multi-tenant

## Schema Principal

### Tabelas Core

#### Units (Unidades Habitacionais)

```sql
CREATE TABLE units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    address TEXT NOT NULL,
    coordinates GEOMETRY(POINT, 4326) NOT NULL,
    area DECIMAL(10,2),
    holder_id UUID REFERENCES holders(id),
    community_id UUID REFERENCES communities(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- RLS Policy
ALTER TABLE units ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON units
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

#### Holders (Possuidores/Beneficiários)

```sql
CREATE TABLE holders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    name TEXT NOT NULL,
    cpf_cnpj TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE holders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON holders
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

#### Communities (Comunidades/Núcleos)

```sql
CREATE TABLE communities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    name TEXT NOT NULL,
    boundary GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

ALTER TABLE communities ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON communities
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

## Migrations

As migrations são gerenciadas via Entity Framework Core:

```bash
# Criar nova migration
dotnet ef migrations add NomeMigration \
    --project src/Infrastructure \
    --startup-project src/Gateway

# Aplicar migrations
dotnet ef database update \
    --project src/Infrastructure \
    --startup-project src/Gateway

# Reverter migration
dotnet ef database update PreviousMigrationName \
    --project src/Infrastructure \
    --startup-project src/Gateway
```

## Row-Level Security (RLS)

Cada tabela possui política RLS que filtra automaticamente por `tenant_id`:

```csharp
// No middleware, configuramos o tenant_id da sessão
await using var cmd = connection.CreateCommand();
cmd.CommandText = "SET app.tenant_id = @tenantId";
cmd.Parameters.AddWithValue("tenantId", tenantId);
await cmd.ExecuteNonQueryAsync();

// Todas as queries respeitam automaticamente o RLS
var units = await context.Units.ToListAsync(); // Filtra por tenant_id
```

## Índices

```sql
-- Índices geoespaciais
CREATE INDEX idx_units_coordinates ON units USING GIST (coordinates);
CREATE INDEX idx_communities_boundary ON communities USING GIST (boundary);

-- Índices para queries comuns
CREATE INDEX idx_units_tenant_id ON units(tenant_id);
CREATE INDEX idx_units_holder_id ON units(holder_id);
CREATE INDEX idx_units_community_id ON units(community_id);
```

## Consultas Geoespaciais

### Unidades dentro de uma comunidade

```sql
SELECT u.*
FROM units u
JOIN communities c ON ST_Within(u.coordinates, c.boundary)
WHERE c.id = 'community-uuid';
```

### Distância entre unidades

```sql
SELECT
    u1.id,
    u2.id,
    ST_Distance(u1.coordinates::geography, u2.coordinates::geography) as distance_meters
FROM units u1
CROSS JOIN units u2
WHERE u1.id != u2.id;
```

### Buffer ao redor de uma unidade

```sql
SELECT ST_Buffer(coordinates::geography, 100)::geometry as buffer_100m
FROM units
WHERE id = 'unit-uuid';
```

## Backup & Restore

```bash
# Backup
pg_dump -h localhost -U postgres carf > backup.sql

# Restore
psql -h localhost -U postgres carf < backup.sql
```

## Documentação Detalhada

Ver arquivos em `CENTRAL/ARCHITECTURE/DATABASE/` no repositório carf-docs:

- `01-schema.md` - Schema completo
- `02-migrations.md` - Gestão de migrations
- `03-rls-policies.md` - Políticas Row-Level Security
- `04-geospatial.md` - Operações geoespaciais

## Próximos Passos

- Ver [Setup](/dev/setup/)
- Consultar [API](/dev/api/)
- Ler [Arquitetura](/dev/arquitetura/)
