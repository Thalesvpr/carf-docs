# GEOAPI Dashboard

Dashboard de monitoramento da API principal do CARF.

## Visão Geral

Dashboard para acompanhamento em tempo real de métricas da GEOAPI incluindo throughput, latência, erros e performance de endpoints.

## Panels

### Row: Overview

| Panel | Tipo | Query | Descrição |
|-------|------|-------|-----------|
| Requests/sec | Stat | `geoapi:http_requests_total:rate5m` | Taxa atual de requests |
| Error Rate | Stat | `geoapi:http_error_percentage:rate5m` | Percentual de erros 5xx |
| P99 Latency | Stat | `geoapi:http_latency:p99` | Latência percentil 99 |
| Active Pods | Stat | `count(up{job="geoapi"} == 1)` | Pods ativos |

### Row: Traffic

| Panel | Tipo | Query |
|-------|------|-------|
| Requests per Second | Time Series | `sum(rate(http_requests_total{job="geoapi"}[5m])) by (status)` |
| Requests by Endpoint | Time Series | `sum(rate(http_requests_total{job="geoapi"}[5m])) by (endpoint)` |
| HTTP Status Distribution | Pie Chart | `sum(increase(http_requests_total{job="geoapi"}[1h])) by (status)` |

### Row: Latency

| Panel | Tipo | Query |
|-------|------|-------|
| Latency Percentiles | Time Series | `geoapi:http_latency:p50`, `geoapi:http_latency:p95`, `geoapi:http_latency:p99` |
| Latency by Endpoint | Time Series | `geoapi:http_latency_by_endpoint:p95` |
| Latency Heatmap | Heatmap | `sum(rate(http_request_duration_seconds_bucket{job="geoapi"}[5m])) by (le)` |

### Row: Database

| Panel | Tipo | Query |
|-------|------|-------|
| DB Query Time | Time Series | `histogram_quantile(0.95, rate(db_query_duration_seconds_bucket[5m]))` |
| Queries per Second | Time Series | `sum(rate(db_query_duration_seconds_count[5m]))` |
| Slow Queries | Table | `topk(10, avg(db_query_duration_seconds_sum/db_query_duration_seconds_count) by (query))` |

### Row: Cache

| Panel | Tipo | Query |
|-------|------|-------|
| Cache Hit Ratio | Gauge | `geoapi:cache_hit_ratio:rate5m * 100` |
| Cache Operations | Time Series | `sum(rate(cache_hits_total[5m]))`, `sum(rate(cache_misses_total[5m]))` |

## Variables

```json
{
  "templating": {
    "list": [
      {
        "name": "environment",
        "type": "custom",
        "options": ["production", "staging"],
        "current": "production"
      },
      {
        "name": "endpoint",
        "type": "query",
        "query": "label_values(http_requests_total{job=\"geoapi\"}, endpoint)"
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

## Configurações

- **Auto-refresh**: 30s
- **Time range default**: Last 6 hours
- **Timezone**: America/Sao_Paulo

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
