# Slow Query Detection

Runbook para identificar e resolver queries lentas que impactam performance do sistema, especialmente queries espaciais com PostGIS.

## Diagnóstico

```sql
-- Queries ativas há mais de 5 segundos
SELECT pid, now() - query_start as duration, state, query
FROM pg_stat_activity
WHERE state != 'idle'
AND now() - query_start > interval '5 seconds'
ORDER BY duration DESC;

-- Top 10 queries mais lentas (requer pg_stat_statements)
SELECT round(total_exec_time::numeric, 2) as total_ms,
       calls,
       round(mean_exec_time::numeric, 2) as avg_ms,
       query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Queries espaciais lentas
SELECT query, calls, total_exec_time
FROM pg_stat_statements
WHERE query ILIKE '%ST_%' OR query ILIKE '%geometry%'
ORDER BY mean_exec_time DESC
LIMIT 10;
```

## Análise de Query Específica

```sql
-- Explain analyze de query suspeita
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM units
WHERE ST_Within(geometry, ST_GeomFromGeoJSON('{"type":"Polygon",...}'));

-- Verificar se índice espacial está sendo usado
-- Deve mostrar "Index Scan using units_geometry_idx"
```

## Verificar Índices Espaciais

```sql
-- Listar índices GiST/BRIN em colunas geometry
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename IN ('units', 'communities', 'blocks', 'plots')
AND indexdef ILIKE '%gist%' OR indexdef ILIKE '%geometry%';

-- Verificar tamanho e uso dos índices
SELECT schemaname, relname, indexrelname,
       pg_size_pretty(pg_relation_size(indexrelid)) as index_size,
       idx_scan, idx_tup_read
FROM pg_stat_user_indexes
WHERE indexrelname LIKE '%geometry%';
```

## Ações Imediatas

```sql
-- Matar query travada (usar com cuidado)
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE query LIKE '%sua_query_problematica%'
AND pid <> pg_backend_pid();

-- Recriar índice espacial se corrompido
REINDEX INDEX units_geometry_idx;

-- Atualizar estatísticas (importante para query planner)
ANALYZE units;
ANALYZE communities;

-- Vacuum para recuperar espaço e atualizar visibility map
VACUUM ANALYZE units;
```

## Otimizações Comuns

```sql
-- Índice GiST para queries de contenção (ST_Within, ST_Contains)
CREATE INDEX IF NOT EXISTS units_geometry_idx ON units USING GIST(geometry);

-- Índice parcial para status específico (reduz tamanho)
CREATE INDEX IF NOT EXISTS units_geometry_active_idx ON units USING GIST(geometry)
WHERE status = 'active';

-- Simplificar geometrias para queries de preview
UPDATE units SET geometry_simplified = ST_Simplify(geometry, 0.0001)
WHERE geometry_simplified IS NULL;
```

## Métricas no Grafana

Dashboard deve mostrar:
- P95 latency de queries espaciais
- Queries por segundo
- Buffer hit ratio (deve ser > 95%)
- Índice scan vs sequential scan ratio

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
