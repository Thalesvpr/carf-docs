# Alert Rules

Regras de alerta Prometheus para detecção proativa de problemas no CARF.

## Alertas de Aplicação

```yaml
# alerts/application.yml
groups:
  - name: geoapi-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{job="geoapi",status=~"5.."}[5m]))
            /
            sum(rate(http_requests_total{job="geoapi"}[5m]))
          ) > 0.01
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Taxa de erro acima de 1%"
          description: "GEOAPI com {{ $value | humanizePercentage }} de erros 5xx nos últimos 5 minutos"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Latência p99 acima de 1 segundo"
          description: "GEOAPI p99 latency: {{ $value | humanizeDuration }}"

      - alert: HighLatencyCritical
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) > 3
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Latência p99 crítica acima de 3 segundos"

      - alert: ServiceDown
        expr: up{job="geoapi"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "GEOAPI não está respondendo"
          description: "Target {{ $labels.instance }} down por mais de 1 minuto"
```

## Alertas de Infraestrutura

```yaml
# alerts/infrastructure.yml
groups:
  - name: infrastructure-alerts
    rules:
      - alert: HighCPU
        expr: (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) > 0.80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "CPU acima de 80% no node {{ $labels.instance }}"

      - alert: HighCPUCritical
        expr: (1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) > 0.95
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "CPU crítico acima de 95%"

      - alert: HighMemory
        expr: (1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) > 0.90
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Memória acima de 90% no node {{ $labels.instance }}"

      - alert: DiskSpaceLow
        expr: (node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) < 0.10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Disco com menos de 10% livre"

      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) > 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Pod {{ $labels.pod }} reiniciando frequentemente"
```

## Alertas de Database

```yaml
# alerts/database.yml
groups:
  - name: postgres-alerts
    rules:
      - alert: DatabaseConnectionsHigh
        expr: pg_stat_activity_count{state="active"} > 80
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Conexões PostgreSQL acima de 80"

      - alert: DatabaseConnectionsCritical
        expr: pg_stat_activity_count{state="active"} > 95
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "Conexões PostgreSQL crítico - próximo do limite"

      - alert: SlowQueries
        expr: rate(pg_stat_statements_seconds_total[5m]) / rate(pg_stat_statements_calls_total[5m]) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Queries com média acima de 1 segundo"

      - alert: ReplicationLag
        expr: pg_replication_lag > 30
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Replication lag maior que 30 segundos"

      - alert: DeadlockDetected
        expr: increase(pg_stat_database_deadlocks[5m]) > 0
        for: 0m
        labels:
          severity: warning
        annotations:
          summary: "Deadlock detectado no PostgreSQL"
```

## Configuração AlertManager

```yaml
# alertmanager.yml
route:
  receiver: 'slack-notifications'
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
    - match:
        severity: warning
      receiver: 'slack-warnings'

receivers:
  - name: 'slack-notifications'
    slack_configs:
      - channel: '#ops-alerts'
        send_resolved: true

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#ops-warnings'
        send_resolved: true

  - name: 'pagerduty-critical'
    pagerduty_configs:
      - service_key: '<PAGERDUTY_KEY>'
        severity: critical
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
