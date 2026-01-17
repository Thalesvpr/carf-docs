# Scrape Configs

Configuração de scrape targets do Prometheus para coleta de métricas do CARF.

## Configuração Base

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'carf-prod'
    environment: 'production'

scrape_configs:
  # GEOAPI Application Metrics
  - job_name: 'geoapi'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names: ['carf']
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: geoapi
        action: keep
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        target_label: __address__
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
    metrics_path: /metrics

  # PostgreSQL Exporter
  - job_name: 'postgres'
    static_configs:
      - targets: ['postgres-exporter:9187']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'carf-postgres'

  # Keycloak Metrics
  - job_name: 'keycloak'
    metrics_path: /metrics
    static_configs:
      - targets: ['keycloak:8080']
    relabel_configs:
      - source_labels: [__address__]
        target_label: instance
        replacement: 'carf-keycloak'

  # Node Exporter (infra)
  - job_name: 'node'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - source_labels: [__address__]
        regex: (.+):10250
        target_label: __address__
        replacement: $1:9100

  # Kubernetes Pods (generic)
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
```

## Métricas Coletadas por Target

### GEOAPI

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| http_requests_total | Counter | Total de requests por endpoint/status |
| http_request_duration_seconds | Histogram | Latência de requests |
| db_query_duration_seconds | Histogram | Tempo de queries SQL |
| cache_hits_total | Counter | Cache hits Redis |
| cache_misses_total | Counter | Cache misses Redis |
| active_connections | Gauge | Conexões ativas |

### PostgreSQL

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| pg_stat_activity_count | Gauge | Conexões por estado |
| pg_stat_database_tup_* | Counter | Tuplas inserted/updated/deleted |
| pg_stat_bgwriter_* | Counter | Operações de background writer |
| pg_locks_count | Gauge | Locks por tipo |
| pg_replication_lag | Gauge | Lag de replicação (se houver) |

### Node Exporter

| Métrica | Tipo | Descrição |
|---------|------|-----------|
| node_cpu_seconds_total | Counter | Uso de CPU por modo |
| node_memory_MemAvailable_bytes | Gauge | Memória disponível |
| node_filesystem_avail_bytes | Gauge | Espaço em disco |
| node_network_receive_bytes_total | Counter | Bytes de rede recebidos |

## Verificação

```bash
# Verificar targets ativos
curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | {job: .labels.job, health: .health}'

# Verificar scrape errors
curl -s http://prometheus:9090/api/v1/targets | jq '.data.activeTargets[] | select(.health != "up")'
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
