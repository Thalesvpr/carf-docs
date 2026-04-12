---
type: leaf
status: review
updated: 2026-02-08
---

# Database Migrations - GEOAPI

Guia completo para gerenciamento de migrations do Entity Framework Core no GEOAPI, incluindo criacao, aplicacao, reversao, convencoes de nomenclatura e troubleshooting.

---

## Visao Geral

O GEOAPI utiliza EF Core Code-First Migrations para gerenciar o schema do PostgreSQL + PostGIS. As migrations sao geradas a partir das entity configurations na camada Infrastructure e aplicadas ao banco de dados via EF Core CLI.

### Caminhos Importantes

| Item | Caminho |
|------|---------|
| Projeto de migrations | `src/Carf.GeoApi.Infrastructure/` |
| Startup project | `src/Carf.GeoApi.Gateway/` |
| Pasta de migrations geradas | `src/Carf.GeoApi.Infrastructure/Persistence/Migrations/` |
| Entity configurations | `src/Carf.GeoApi.Infrastructure/Persistence/Configurations/` |
| DbContext | `src/Carf.GeoApi.Infrastructure/Persistence/AppDbContext.cs` |

---

## Comandos Principais

### Referencia Rapida

| Comando | Descricao | Exemplo | Notas |
|---------|-----------|---------|-------|
| `dotnet ef migrations add` | Criar nova migration | `dotnet ef migrations add AddHolderPhone ...` | Gera arquivos .cs na pasta Migrations |
| `dotnet ef database update` | Aplicar migrations pendentes | `dotnet ef database update ...` | Aplica todas ate a mais recente |
| `dotnet ef database update <Name>` | Aplicar/reverter ate migration especifica | `dotnet ef database update AddHolderPhone ...` | Pode reverter se migration ja foi aplicada |
| `dotnet ef migrations remove` | Remover ultima migration (nao aplicada) | `dotnet ef migrations remove ...` | Falha se migration ja foi aplicada ao banco |
| `dotnet ef migrations list` | Listar todas as migrations | `dotnet ef migrations list ...` | Marca as ja aplicadas |
| `dotnet ef migrations script` | Gerar script SQL | `dotnet ef migrations script --idempotent ...` | Para aplicacao em CI/CD ou DBA review |

> **Nota:** Todos os comandos abaixo assumem execucao a partir da raiz do repositorio (`PROJECTS/GEOAPI/SRC-CODE/`).

---

## Criar Nova Migration

### Comando Completo

```bash
dotnet ef migrations add NomeDaMigration \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway \
  --context AppDbContext
```

### Exemplo Pratico

```bash
dotnet ef migrations add 2024_03_15_AddHolderPhoneColumn \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

**Saida esperada:**

```
Build started...
Build succeeded.
Done. To undo this action, use 'ef migrations remove'
```

**Arquivos gerados:**

```
src/Carf.GeoApi.Infrastructure/Persistence/Migrations/
├── 20240315120000_2024_03_15_AddHolderPhoneColumn.cs          ← Up() e Down()
├── 20240315120000_2024_03_15_AddHolderPhoneColumn.Designer.cs ← Snapshot parcial
└── AppDbContextModelSnapshot.cs                                ← Atualizado
```

### O que verificar apos criar

1. Abrir o arquivo da migration gerada e inspecionar `Up()` e `Down()`
2. Verificar que `Down()` reverte corretamente todas as alteracoes de `Up()`
3. Conferir que nao foram geradas alteracoes indesejadas (diff de propriedades nav, indices, etc.)
4. Verificar que o `AppDbContextModelSnapshot.cs` reflete o estado esperado

---

## Aplicar Migrations

### Aplicar todas as migrations pendentes

```bash
dotnet ef database update \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

### Aplicar ate uma migration especifica

```bash
dotnet ef database update 2024_03_15_AddHolderPhoneColumn \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

### Verificar migrations aplicadas

```bash
dotnet ef migrations list \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

**Saida esperada:**

```
20240101000000_Initial (applied)
20240115000000_AddPostGISExtension (applied)
20240315120000_2024_03_15_AddHolderPhoneColumn (applied)
20240401000000_AddTeamEntity (pending)        ← nao aplicada ainda
```

### Verificar no banco diretamente

```bash
docker exec -it geoapi-db psql -U geoapi -d geoapi_dev \
  -c "SELECT \"MigrationId\", \"ProductVersion\" FROM \"__EFMigrationsHistory\" ORDER BY \"MigrationId\";"
```

---

## Reverter Migration

### Reverter para migration anterior (desfaz a ultima)

```bash
dotnet ef database update NomeDaMigrationAnterior \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

**Exemplo:** Se a ultima migration aplicada e `AddHolderPhoneColumn` e a anterior e `AddPostGISExtension`:

```bash
dotnet ef database update AddPostGISExtension \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

Isso executa o metodo `Down()` da migration `AddHolderPhoneColumn`.

### Reverter todas as migrations (voltar ao zero)

```bash
dotnet ef database update 0 \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

> **Cuidado:** Isso executa `Down()` de TODAS as migrations, removendo todas as tabelas.

---

## Remover Ultima Migration

Remove o arquivo da ultima migration (nao aplicada) e restaura o snapshot:

```bash
dotnet ef migrations remove \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway
```

> **Nota:** Este comando falha se a migration ja foi aplicada ao banco. Neste caso, reverter primeiro com `database update` e depois usar `migrations remove`.

---

## Gerar Script SQL

### Script idempotente (recomendado para producao)

```bash
dotnet ef migrations script --idempotent \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway \
  --output migrations.sql
```

O script gerado contem verificacoes `IF NOT EXISTS` e pode ser aplicado com seguranca mesmo se algumas migrations ja foram executadas.

### Script de uma migration especifica para outra

```bash
dotnet ef migrations script AddPostGISExtension AddHolderPhoneColumn \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway \
  --output delta.sql
```

### Uso do script em producao

```bash
# Via DBA review
psql -h prod-host -U geoapi -d geoapi_prod -f migrations.sql

# Ou via pipeline CI/CD (ver secao CI/CD abaixo)
```

---

## Convencoes de Nomenclatura

### Formato de Nome

```
YYYY_MM_DD_DescricaoDoQueAcontece
```

### Exemplos

| Nome da Migration | O que faz |
|-------------------|-----------|
| `2024_01_01_Initial` | Schema inicial (tabelas, indices, constraints) |
| `2024_01_15_AddPostGISExtension` | Instala extensao PostGIS |
| `2024_02_10_AddHolderEmailColumn` | Adiciona coluna email na tabela holders |
| `2024_03_01_CreateTeamsTable` | Cria tabela teams e relacionamentos |
| `2024_03_15_AddUnitStatusIndex` | Adiciona indice na coluna status de units |
| `2024_04_01_RenameBlockToQuadra` | Renomeia coluna/tabela |
| `2024_04_15_AddRLSPolicies` | Cria policies Row-Level Security |
| `2024_05_01_SeedInitialData` | Insere dados iniciais (seed) |
| `2024_05_15_AddVersionColumnForSync` | Adiciona coluna version para sync offline |

### Regras

1. **Sempre prefixar com data** no formato `YYYY_MM_DD` para ordenacao cronologica
2. **Usar verbos de acao**: `Add`, `Create`, `Remove`, `Rename`, `Update`, `Seed`
3. **Descrever a mudanca de forma sucinta** - o que, nao o porque
4. **Uma migration por alteracao logica** - nao misturar criacao de tabela com seed data
5. **Nunca editar migration ja aplicada** - criar nova migration para correcoes

---

## PostGIS e Extensions

### Migration inicial para PostGIS

A migration inicial deve incluir a criacao da extensao PostGIS:

```csharp
// Em Up()
migrationBuilder.Sql("CREATE EXTENSION IF NOT EXISTS postgis;");
migrationBuilder.Sql("CREATE EXTENSION IF NOT EXISTS postgis_topology;");

// Em Down()
migrationBuilder.Sql("DROP EXTENSION IF EXISTS postgis_topology;");
migrationBuilder.Sql("DROP EXTENSION IF EXISTS postgis;");
```

### Colunas Geoespaciais

Para adicionar colunas geometry/geography nas migrations:

```csharp
// Via EF Core NTS (NetTopologySuite)
migrationBuilder.AddColumn<Geometry>(
    name: "boundary",
    table: "communities",
    type: "geometry(Polygon, 4326)",
    nullable: true);

// Criar indice espacial
migrationBuilder.CreateIndex(
    name: "IX_communities_boundary",
    table: "communities",
    column: "boundary")
    .Annotation("Npgsql:IndexMethod", "gist");
```

---

## Seed Data

### HasData() em Entity Configuration (preferido para dados estaticos)

```csharp
// Em src/Carf.GeoApi.Infrastructure/Persistence/Configurations/CommunityTypeConfiguration.cs
builder.HasData(
    new { Id = 1, Name = "Quilombola", Code = "QUI" },
    new { Id = 2, Name = "Ribeirinha", Code = "RIB" },
    new { Id = 3, Name = "Indigena", Code = "IND" }
);
```

- Vantagem: Versionado junto com migrations, rastreavel
- Uso: Dados de referencia (enums, tipos, categorias)

### SQL Scripts (para dados volumosos ou complexos)

```csharp
// Em Up() da migration
migrationBuilder.Sql(@"
    INSERT INTO community_types (id, name, code) VALUES
    (1, 'Quilombola', 'QUI'),
    (2, 'Ribeirinha', 'RIB'),
    (3, 'Indigena', 'IND')
    ON CONFLICT (id) DO NOTHING;
");
```

- Vantagem: Mais flexivel, suporta `ON CONFLICT`
- Uso: Dados de seed mais complexos, bulk inserts

---

## Row-Level Security (RLS) em Migrations

O GEOAPI utiliza RLS para isolamento de dados por tenant. As policies sao criadas via SQL em migrations:

```csharp
// Em Up()
migrationBuilder.Sql(@"
    ALTER TABLE units ENABLE ROW LEVEL SECURITY;

    CREATE POLICY units_tenant_isolation ON units
        USING (tenant_id = current_setting('app.current_tenant')::uuid)
        WITH CHECK (tenant_id = current_setting('app.current_tenant')::uuid);

    -- Conceder permissoes ao role da aplicacao
    GRANT ALL ON units TO geoapi;
");

// Em Down()
migrationBuilder.Sql(@"
    DROP POLICY IF EXISTS units_tenant_isolation ON units;
    ALTER TABLE units DISABLE ROW LEVEL SECURITY;
");
```

> **Importante:** Toda tabela que contiver `tenant_id` deve ter policy RLS correspondente.

---

## CI/CD e Migrations

### Verificar migrations pendentes no pipeline

```bash
# Retorna exit code > 0 se houver migrations pendentes
dotnet ef migrations list \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway \
  | grep "(pending)"
```

### Aplicar em ambiente de staging/producao

```bash
# Gerar script idempotente
dotnet ef migrations script --idempotent \
  --project src/Carf.GeoApi.Infrastructure \
  --startup-project src/Carf.GeoApi.Gateway \
  --output /tmp/migrations.sql

# Aplicar via psql (com credenciais seguras)
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -U $DB_USER -d $DB_NAME -f /tmp/migrations.sql
```

### Validacao pos-migration

```sql
-- Verificar que todas as tabelas esperadas existem
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;

-- Verificar policies RLS ativas
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE schemaname = 'public';

-- Verificar extensoes
SELECT extname, extversion FROM pg_extension;
```

---

## Troubleshooting

| Sintoma | Causa Provavel | Solucao |
|---------|---------------|---------|
| `The migration has already been applied` ao tentar `remove` | Migration ja aplicada ao banco | Reverter primeiro com `dotnet ef database update <MigrationAnterior>` e depois `remove` |
| `relation "xxx" already exists` | Migration aplicada parcialmente (crash durante apply) | Reverter migration anterior: `dotnet ef database update <MigrationAnterior>`. Se nao funcionar, corrigir manualmente no banco e registrar na `__EFMigrationsHistory` |
| `There is already an object named 'xxx'` | Conflito entre migration gerada e estado real do banco | Comparar schema real vs esperado. Optar por `--idempotent` script ou corrigir manualmente |
| `Model snapshot is out of date` | Merge conflict no snapshot | Deletar `AppDbContextModelSnapshot.cs`, remover ultima migration, re-criar |
| `No migrations configuration type was found` | Projeto errado no parametro `--project` | Verificar que `--project` aponta para Infrastructure (onde esta o DbContext) |
| `Unable to create an object of type 'AppDbContext'` | Falta Design-time factory ou startup project incorreto | Verificar que `--startup-project` aponta para Gateway. Verificar `IDesignTimeDbContextFactory` se necessario |
| `Npgsql.PostgresException: permission denied` | Usuario sem permissao para ALTER/CREATE | Verificar que o usuario de conexao e owner do schema. Executar: `ALTER SCHEMA public OWNER TO geoapi;` |
| `Could not find type mapping for PostGIS` | Package NTS nao instalado | `dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL.NetTopologySuite` |
| Conflito de migrations apos merge de branches | Duas branches criaram migrations concorrentes | Ver secao "Resolver Conflitos de Migration" abaixo |
| Migration muito lenta | Tabela grande, operacao bloqueante | Usar `CONCURRENTLY` para indices. Considerar aplicar fora do horario de pico |

### Resolver Conflitos de Migration

Quando duas branches criam migrations concorrentes e sao mergeadas:

1. **Identificar o conflito:**
   ```bash
   git diff main...HEAD -- src/Carf.GeoApi.Infrastructure/Persistence/Migrations/AppDbContextModelSnapshot.cs
   ```

2. **Resolver:**
   - Manter ambas as migrations (ajustar timestamps se necessario)
   - Deletar `AppDbContextModelSnapshot.cs`
   - Criar migration vazia para regenerar snapshot:
     ```bash
     dotnet ef migrations add MergeSnapshot \
       --project src/Carf.GeoApi.Infrastructure \
       --startup-project src/Carf.GeoApi.Gateway
     ```
   - Verificar que a migration gerada esta vazia (apenas regenerou o snapshot)
   - Se nao estiver vazia, ha divergencia - revisar manualmente

3. **Testar:** Aplicar no banco limpo para garantir que ambas as migrations funcionam em sequencia.

---

## Boas Praticas

1. **Sempre gerar script SQL antes de aplicar em producao** - `dotnet ef migrations script --idempotent`
2. **Nunca editar migration ja aplicada** - criar nova migration corretiva
3. **Testar Down() tambem** - reverter e re-aplicar para garantir que Down() funciona
4. **Uma migration = uma mudanca logica** - facilita reversao granular
5. **Revisar migration gerada antes de commitar** - EF Core pode gerar alteracoes inesperadas
6. **Adicionar coluna version em tabelas com sync mobile** - `units`, `holders`, `communities`, `documents`
7. **Criar indice espacial para toda coluna geometry** - usando `.Annotation("Npgsql:IndexMethod", "gist")`
8. **Incluir RLS policy para toda tabela com tenant_id** - ver secao RLS acima

---

## Referencias

| Recurso | Link |
|---------|------|
| EF Core Migrations Overview | learn.microsoft.com/ef/core/managing-schemas/migrations |
| EF Core CLI Reference | learn.microsoft.com/ef/core/cli/dotnet |
| Npgsql + PostGIS | npgsql.org/efcore/mapping/nts.html |
| PostgreSQL RLS | postgresql.org/docs/16/ddl-rowsecurity.html |
| Setup ambiente | [01-setup-dev-environment.md](./01-setup-dev-environment.md) |
| Docker Compose | [04-docker-compose-reference.md](./04-docker-compose-reference.md) |
