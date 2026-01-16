# RLS Setup

Configuração de Row-Level Security para isolamento multi-tenant.

## Conceito

Row-Level Security (RLS) garante que cada query retorna apenas dados do tenant do usuário autenticado, sem necessidade de filtros manuais no código.

## Variável de Sessão

```sql
-- Definir tenant no início da conexão
SET app.current_tenant_id = 'uuid-do-tenant';

-- Limpar ao final
RESET app.current_tenant_id;
```

## Habilitando RLS

```sql
-- Script: 02-enable-rls.sql

-- Habilitar RLS nas tabelas
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE holders ENABLE ROW LEVEL SECURITY;
ALTER TABLE communities ENABLE ROW LEVEL SECURITY;
ALTER TABLE legitimations ENABLE ROW LEVEL SECURITY;
ALTER TABLE unit_holders ENABLE ROW LEVEL SECURITY;
ALTER TABLE unit_photos ENABLE ROW LEVEL SECURITY;

-- Forçar RLS para owner (opcional, mais seguro)
ALTER TABLE units FORCE ROW LEVEL SECURITY;
```

## Policies

### Policy de Leitura

```sql
-- Units: ler apenas do próprio tenant
CREATE POLICY tenant_isolation_select ON units
    FOR SELECT
    USING (tenant_id::text = current_setting('app.current_tenant_id', true));

-- Holders: mesma lógica
CREATE POLICY tenant_isolation_select ON holders
    FOR SELECT
    USING (tenant_id::text = current_setting('app.current_tenant_id', true));

-- Aplicar para todas tabelas com tenant_id
```

### Policy de Insert

```sql
-- Units: inserir apenas no próprio tenant
CREATE POLICY tenant_isolation_insert ON units
    FOR INSERT
    WITH CHECK (tenant_id::text = current_setting('app.current_tenant_id', true));
```

### Policy de Update

```sql
-- Units: atualizar apenas do próprio tenant
CREATE POLICY tenant_isolation_update ON units
    FOR UPDATE
    USING (tenant_id::text = current_setting('app.current_tenant_id', true))
    WITH CHECK (tenant_id::text = current_setting('app.current_tenant_id', true));
```

### Policy de Delete

```sql
-- Units: deletar apenas do próprio tenant
CREATE POLICY tenant_isolation_delete ON units
    FOR DELETE
    USING (tenant_id::text = current_setting('app.current_tenant_id', true));
```

## Bypass para Admin

```sql
-- Usuário admin pode ver tudo
CREATE POLICY admin_bypass ON units
    FOR ALL
    TO admin_role
    USING (true)
    WITH CHECK (true);
```

## Integração com Aplicação

```csharp
// DbContext.cs - Interceptor para setar tenant
public class TenantInterceptor : DbCommandInterceptor
{
    private readonly ITenantContext _tenantContext;

    public override InterceptionResult<DbDataReader> ReaderExecuting(
        DbCommand command,
        CommandEventData eventData,
        InterceptionResult<DbDataReader> result)
    {
        SetTenantId(command.Connection);
        return base.ReaderExecuting(command, eventData, result);
    }

    private void SetTenantId(DbConnection connection)
    {
        using var cmd = connection.CreateCommand();
        cmd.CommandText = $"SET app.current_tenant_id = '{_tenantContext.TenantId}'";
        cmd.ExecuteNonQuery();
    }
}
```

## Verificação

```sql
-- Testar se RLS está funcionando
SET app.current_tenant_id = 'tenant-a';
SELECT count(*) FROM units; -- Deve retornar apenas units do tenant-a

SET app.current_tenant_id = 'tenant-b';
SELECT count(*) FROM units; -- Deve retornar apenas units do tenant-b
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
