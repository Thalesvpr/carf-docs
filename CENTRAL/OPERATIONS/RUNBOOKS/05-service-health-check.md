# Service Health Check

Runbook para verificar saúde de todos os serviços do ecossistema CARF e identificar componentes com problemas.

## Health Endpoints

```bash
# GEOAPI
curl -s https://api.carf.com.br/health | jq .

# Keycloak
curl -s https://keycloak.carf.com.br/health | jq .

# PostgreSQL (via GEOAPI)
curl -s https://api.carf.com.br/health/db | jq .

# Redis
curl -s https://api.carf.com.br/health/cache | jq .
```

## Kubernetes Status

```bash
# Pods em estado não-Running
kubectl get pods -A | grep -v Running | grep -v Completed

# Pods com restart recente
kubectl get pods -A -o wide | awk '$5 > 0 {print $0}'

# Eventos de erro recentes
kubectl get events -A --sort-by='.lastTimestamp' | grep -i "error\|failed\|back-off"

# Resource usage
kubectl top pods -A --sort-by=memory | head -20
```

## Database Health

```sql
-- Verificar replicação (se configurada)
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn
FROM pg_stat_replication;

-- Verificar espaço em disco
SELECT pg_database.datname,
       pg_size_pretty(pg_database_size(pg_database.datname)) as size
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;

-- Verificar locks pendentes
SELECT blocked_locks.pid AS blocked_pid,
       blocking_locks.pid AS blocking_pid,
       blocked_activity.query AS blocked_query
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

## Checklist Rápido

```bash
#!/bin/bash
echo "=== CARF Health Check ==="

echo -n "GEOAPI: "
curl -s -o /dev/null -w "%{http_code}" https://api.carf.com.br/health

echo -n "Keycloak: "
curl -s -o /dev/null -w "%{http_code}" https://keycloak.carf.com.br/health

echo -n "PostgreSQL: "
psql -h postgres -U carf -c "SELECT 1" -t -q && echo "OK" || echo "FAIL"

echo -n "Redis: "
redis-cli -h redis ping

echo -n "S3/MinIO: "
aws s3 ls s3://carf-documents --endpoint-url=$MINIO_ENDPOINT > /dev/null && echo "OK" || echo "FAIL"
```

## Alertas Críticos

Verificar no Alertmanager:
```bash
curl -s http://alertmanager:9093/api/v2/alerts | jq '.[] | select(.status.state=="active")'
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
