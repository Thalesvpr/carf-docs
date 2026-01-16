# Database Vacuum e Reindex

Procedimentos de manutenção do PostgreSQL para otimizar performance e recuperar espaço em disco.

## VACUUM ANALYZE Semanal

Executado automaticamente aos domingos às 03:00 UTC via CronJob:

```sql
-- Vacuum com analyze para atualizar estatísticas
VACUUM (VERBOSE, ANALYZE) units;
VACUUM (VERBOSE, ANALYZE) holders;
VACUUM (VERBOSE, ANALYZE) communities;
VACUUM (VERBOSE, ANALYZE) documents;
VACUUM (VERBOSE, ANALYZE) processes;
```

## Verificar Bloat

```sql
-- Verificar bloat de tabelas (requer pgstattuple)
CREATE EXTENSION IF NOT EXISTS pgstattuple;

SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size,
       round(100 * n_dead_tup / nullif(n_live_tup + n_dead_tup, 0), 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_live_tup > 1000
ORDER BY n_dead_tup DESC
LIMIT 20;

-- Bloat detalhado de tabela específica
SELECT * FROM pgstattuple('units');
```

## REINDEX Trimestral

Executar quando bloat de índices ultrapassar 30%:

```sql
-- Verificar tamanho dos índices
SELECT schemaname, tablename, indexname,
       pg_size_pretty(pg_relation_size(indexrelid)) as index_size
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Reindex concorrente (não bloqueia leituras)
REINDEX INDEX CONCURRENTLY units_geometry_idx;
REINDEX INDEX CONCURRENTLY units_tenant_id_idx;
REINDEX INDEX CONCURRENTLY holders_cpf_idx;

-- Reindex tabela inteira
REINDEX TABLE CONCURRENTLY units;
```

## Autovacuum Tuning

Configurações recomendadas para tabelas grandes:

```sql
-- Tabelas com muitas atualizações (units, processes)
ALTER TABLE units SET (
  autovacuum_vacuum_scale_factor = 0.05,
  autovacuum_analyze_scale_factor = 0.02,
  autovacuum_vacuum_cost_delay = 10
);

-- Verificar configurações
SELECT relname, reloptions
FROM pg_class
WHERE relname IN ('units', 'holders', 'communities');
```

## Script de Manutenção Completa

```bash
#!/bin/bash
# maintenance.sh - Executar em janela de manutenção

echo "=== Iniciando manutenção ==="

# 1. Verificar conexões ativas
psql -c "SELECT count(*) FROM pg_stat_activity WHERE state = 'active';"

# 2. Vacuum analyze em todas tabelas
psql -c "VACUUM (VERBOSE, ANALYZE);"

# 3. Reindex se necessário (verificar bloat primeiro)
for table in units holders communities documents; do
  echo "Verificando bloat de $table..."
  bloat=$(psql -t -c "SELECT round(100 * n_dead_tup / nullif(n_live_tup, 0)) FROM pg_stat_user_tables WHERE tablename = '$table';")
  if [ "$bloat" -gt 30 ]; then
    echo "Reindexando $table (bloat: $bloat%)"
    psql -c "REINDEX TABLE CONCURRENTLY $table;"
  fi
done

# 4. Atualizar estatísticas
psql -c "ANALYZE;"

echo "=== Manutenção concluída ==="
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
