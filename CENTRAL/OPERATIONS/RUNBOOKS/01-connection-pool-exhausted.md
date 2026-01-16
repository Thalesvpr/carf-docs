# Connection Pool Exhausted

Runbook para resolver o erro de pool de conexões esgotado no PostgreSQL, indicado por mensagens como "too many connections" ou "connection pool exhausted" nos logs do GEOAPI.

## Diagnóstico

```sql
-- Verificar conexões ativas por aplicação
SELECT application_name, state, count(*)
FROM pg_stat_activity
WHERE datname = 'carf'
GROUP BY application_name, state
ORDER BY count DESC;

-- Verificar conexões idle há muito tempo
SELECT pid, now() - state_change as idle_time, query
FROM pg_stat_activity
WHERE state = 'idle'
AND now() - state_change > interval '5 minutes'
ORDER BY idle_time DESC;
```

## Verificar PgBouncer

```bash
# Status do pool
psql -h localhost -p 6432 -U pgbouncer pgbouncer -c "SHOW POOLS;"

# Conexões ativas
psql -h localhost -p 6432 -U pgbouncer pgbouncer -c "SHOW CLIENTS;"

# Config atual
psql -h localhost -p 6432 -U pgbouncer pgbouncer -c "SHOW CONFIG;" | grep pool
```

## Ações Imediatas

```bash
# Matar conexões idle antigas (cuidado em produção)
psql -d carf -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND now() - state_change > interval '10 minutes'
AND pid <> pg_backend_pid();"

# Reiniciar PgBouncer se necessário
sudo systemctl restart pgbouncer

# Verificar se GEOAPI está fazendo retry
kubectl logs -l app=geoapi --tail=100 | grep -i "connection\|pool"
```

## Configuração Recomendada

PgBouncer (`pgbouncer.ini`):
```ini
[databases]
carf = host=postgres port=5432 dbname=carf

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 50
reserve_pool_size = 10
reserve_pool_timeout = 3
server_idle_timeout = 300
```

GEOAPI (`appsettings.json`):
```json
{
  "ConnectionStrings": {
    "Default": "Host=pgbouncer;Port=6432;Database=carf;Pooling=true;Minimum Pool Size=5;Maximum Pool Size=50;Connection Idle Lifetime=300"
  }
}
```

## Prevenção

Monitorar métrica `pg_stat_activity_count` no Prometheus com alerta quando conexões ativas ultrapassarem 80% do limite configurado.

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
