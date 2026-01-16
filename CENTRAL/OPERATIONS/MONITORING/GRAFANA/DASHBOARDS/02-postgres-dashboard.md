# PostgreSQL Dashboard

Dashboard de monitoramento do banco de dados PostgreSQL do CARF.

## Visão Geral

Dashboard para acompanhamento de saúde, performance e capacidade do PostgreSQL com métricas coletadas via postgres_exporter.

## Panels

### Row: Overview

| Panel | Tipo | Query | Thresholds |
|-------|------|-------|------------|
| Connections | Stat | `postgres:connections:active` | <50 green, <80 yellow, >80 red |
| Cache Hit Ratio | Gauge | `postgres:cache_hit_ratio * 100` | >99% green, >95% yellow, <95% red |
| Transactions/s | Stat | `postgres:transactions:rate5m` | Info only |
| DB Size | Stat | `pg_database_size_bytes{datname="carf"}` | Info only |

### Row: Connections

| Panel | Tipo | Query |
|-------|------|-------|
| Connections by State | Time Series | `postgres:connections:by_state` |
| Connection Usage % | Gauge | `pg_stat_activity_count / pg_settings_max_connections * 100` |
| Waiting Connections | Time Series | `pg_stat_activity_count{state="idle in transaction"}` |
| Blocked Queries | Time Series | `pg_locks_count{mode="ExclusiveLock",granted="f"}` |

### Row: Performance

| Panel | Tipo | Query |
|-------|------|-------|
| Transaction Rate | Time Series | `rate(pg_stat_database_xact_commit[5m])`, `rate(pg_stat_database_xact_rollback[5m])` |
| Commit Ratio | Time Series | `postgres:commit_ratio:rate5m * 100` |
| Tuple Operations | Time Series | `postgres:tuples_inserted:rate5m`, `postgres:tuples_updated:rate5m`, `postgres:tuples_deleted:rate5m` |

### Row: Query Performance

| Panel | Tipo | Query |
|-------|------|-------|
| Slow Queries | Table | `topk(10, pg_stat_statements_mean_time_seconds{datname="carf"})` |
| Query Duration Distribution | Histogram | `pg_stat_statements_mean_time_seconds` |
| Queries by Type | Pie Chart | Query distribution by SELECT/INSERT/UPDATE/DELETE |

### Row: Storage

| Panel | Tipo | Query |
|-------|------|-------|
| Database Size | Time Series | `pg_database_size_bytes{datname="carf"}` |
| Table Sizes | Table | `topk(10, pg_stat_user_tables_size_bytes)` |
| Index Sizes | Table | `topk(10, pg_stat_user_indexes_idx_size_bytes)` |
| Bloat Estimation | Gauge | Dead tuples percentage |

### Row: Replication (if applicable)

| Panel | Tipo | Query |
|-------|------|-------|
| Replication Lag | Time Series | `pg_replication_lag` |
| WAL Generation | Time Series | `rate(pg_stat_archiver_archived_count[5m])` |

### Row: Locks

| Panel | Tipo | Query |
|-------|------|-------|
| Lock Types | Time Series | `pg_locks_count by (mode)` |
| Deadlocks | Time Series | `rate(pg_stat_database_deadlocks[5m])` |
| Lock Waits | Time Series | `pg_stat_activity_count{wait_event_type="Lock"}` |

## Alertas Integrados

Dashboard inclui annotations para alertas:
- `DatabaseConnectionsHigh` - Conexões acima de 80
- `SlowQueries` - Queries com média > 1s
- `DeadlockDetected` - Deadlocks ocorridos

## Variables

```json
{
  "templating": {
    "list": [
      {
        "name": "database",
        "type": "query",
        "query": "label_values(pg_stat_database_tup_fetched, datname)"
      },
      {
        "name": "interval",
        "type": "interval",
        "options": ["1m", "5m", "15m", "1h"]
      }
    ]
  }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
