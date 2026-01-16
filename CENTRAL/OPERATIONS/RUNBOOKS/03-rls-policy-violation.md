# RLS Policy Violation

Runbook para resolver erros de Row-Level Security onde usuário não consegue acessar dados do seu tenant ou está vendo dados de outro tenant incorretamente.

## Diagnóstico

```sql
-- Verificar políticas RLS ativas na tabela
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
FROM pg_policies
WHERE tablename = 'units';

-- Verificar se RLS está habilitado
SELECT relname, relrowsecurity, relforcerowsecurity
FROM pg_class
WHERE relname IN ('units', 'holders', 'communities', 'processes');

-- Testar acesso como tenant específico
SET SESSION "app.current_tenant_id" = 'uuid-do-tenant';
SELECT count(*) FROM units;
RESET "app.current_tenant_id";
```

## Verificar Configuração de Sessão

```bash
# Logs do GEOAPI mostrando tenant_id extraído do JWT
kubectl logs -l app=geoapi --tail=100 | grep -i "tenant\|rls"

# Verificar se middleware está setando session variable
kubectl exec -it deploy/geoapi -- cat /app/appsettings.json | jq '.MultiTenancy'
```

## Problemas Comuns

### 1. Tenant não está sendo setado na sessão

```csharp
// Middleware deve fazer isso no início de cada request
await using var conn = await _pool.GetConnectionAsync();
await conn.ExecuteAsync($"SET SESSION \"app.current_tenant_id\" = '{tenantId}'");
```

### 2. Policy usando função errada

```sql
-- Policy correta usando current_setting
CREATE POLICY tenant_isolation ON units
FOR ALL
USING (tenant_id = current_setting('app.current_tenant_id')::uuid);

-- ERRADO: usando session_user ou current_user
```

### 3. Conexão pooled vazando tenant anterior

```sql
-- PgBouncer em transaction mode deve limpar session vars
-- Verificar se reset_query está configurado
-- pgbouncer.ini:
-- server_reset_query = DISCARD ALL
```

## Ações Imediatas

```sql
-- Recriar policy se corrompida
DROP POLICY IF EXISTS tenant_isolation ON units;
CREATE POLICY tenant_isolation ON units
FOR ALL
USING (tenant_id = current_setting('app.current_tenant_id', true)::uuid);

-- Forçar RLS em tabela
ALTER TABLE units FORCE ROW LEVEL SECURITY;

-- Verificar dados órfãos (sem tenant_id)
SELECT count(*) FROM units WHERE tenant_id IS NULL;
```

## Validação

```bash
# Teste end-to-end com dois tenants diferentes
curl -H "Authorization: Bearer $TOKEN_TENANT_A" https://api.carf.com.br/api/units | jq length
curl -H "Authorization: Bearer $TOKEN_TENANT_B" https://api.carf.com.br/api/units | jq length
# Resultados devem ser diferentes (cada tenant vê apenas seus dados)
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
