# Recording Rules

Recording rules do Prometheus para pré-computar agregações frequentes e otimizar queries de dashboards.

## Regras de Aplicação

```yaml
# rules/application-recording.yml
groups:
  - name: geoapi-recording
    interval: 30s
    rules:
      # Request rate por endpoint
      - record: geoapi:http_requests:rate5m
        expr: sum(rate(http_requests_total{job="geoapi"}[5m])) by (endpoint, method, status)

      # Request rate total
      - record: geoapi:http_requests_total:rate5m
        expr: sum(rate(http_requests_total{job="geoapi"}[5m]))

      # Error rate
      - record: geoapi:http_errors:rate5m
        expr: sum(rate(http_requests_total{job="geoapi",status=~"5.."}[5m]))

      # Error percentage
      - record: geoapi:http_error_percentage:rate5m
        expr: |
          (geoapi:http_errors:rate5m / geoapi:http_requests_total:rate5m) * 100

      # Latência percentis
      - record: geoapi:http_latency:p50
        expr: histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) by (le))

      - record: geoapi:http_latency:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) by (le))

      - record: geoapi:http_latency:p99
        expr: histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) by (le))

      # Latência por endpoint
      - record: geoapi:http_latency_by_endpoint:p95
        expr: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) by (le, endpoint))

      # Cache hit ratio
      - record: geoapi:cache_hit_ratio:rate5m
        expr: |
          sum(rate(cache_hits_total{job="geoapi"}[5m]))
          /
          (sum(rate(cache_hits_total{job="geoapi"}[5m])) + sum(rate(cache_misses_total{job="geoapi"}[5m])))
```

## Regras de Database

```yaml
# rules/database-recording.yml
groups:
  - name: postgres-recording
    interval: 30s
    rules:
      # Conexões por estado
      - record: postgres:connections:by_state
        expr: sum(pg_stat_activity_count) by (state)

      # Total conexões ativas
      - record: postgres:connections:active
        expr: pg_stat_activity_count{state="active"}

      # Transaction rate
      - record: postgres:transactions:rate5m
        expr: sum(rate(pg_stat_database_xact_commit[5m]) + rate(pg_stat_database_xact_rollback[5m])) by (datname)

      # Commit ratio
      - record: postgres:commit_ratio:rate5m
        expr: |
          rate(pg_stat_database_xact_commit[5m])
          /
          (rate(pg_stat_database_xact_commit[5m]) + rate(pg_stat_database_xact_rollback[5m]))

      # Cache hit ratio
      - record: postgres:cache_hit_ratio
        expr: |
          pg_stat_database_blks_hit
          /
          (pg_stat_database_blks_hit + pg_stat_database_blks_read)

      # Tuple operations
      - record: postgres:tuples_inserted:rate5m
        expr: sum(rate(pg_stat_database_tup_inserted[5m])) by (datname)

      - record: postgres:tuples_updated:rate5m
        expr: sum(rate(pg_stat_database_tup_updated[5m])) by (datname)

      - record: postgres:tuples_deleted:rate5m
        expr: sum(rate(pg_stat_database_tup_deleted[5m])) by (datname)
```

## Regras de Infraestrutura

```yaml
# rules/infrastructure-recording.yml
groups:
  - name: infrastructure-recording
    interval: 30s
    rules:
      # CPU usage por node
      - record: node:cpu_usage:rate5m
        expr: 1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)

      # Memory usage por node
      - record: node:memory_usage:ratio
        expr: 1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)

      # Disk usage por node
      - record: node:disk_usage:ratio
        expr: 1 - (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"})

      # Network throughput
      - record: node:network_receive:rate5m
        expr: sum(rate(node_network_receive_bytes_total[5m])) by (instance)

      - record: node:network_transmit:rate5m
        expr: sum(rate(node_network_transmit_bytes_total[5m])) by (instance)

      # Pod restarts
      - record: kube:pod_restarts:rate1h
        expr: sum(increase(kube_pod_container_status_restarts_total[1h])) by (namespace, pod)
```

## Uso em Dashboards

Recording rules permitem queries mais eficientes nos dashboards:

```promql
# Antes (computado em cada refresh)
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) by (le))

# Depois (pré-computado)
geoapi:http_latency:p99
```

Benefícios:
- Reduz carga no Prometheus durante visualização
- Queries mais rápidas em dashboards
- Consistência entre alertas e visualizações
- Permite histórico de métricas agregadas

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
