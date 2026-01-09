# PROMETHEUS

Configuração Prometheus monitoring do CARF. prometheus.yml (scrape configs GEOAPI /metrics, PostgreSQL exporter, Keycloak /metrics, node exporter CPU/memory/disk). alerts.yml regras (HighCPU > 80 porcento 5min, HighMemory > 90 porcento, HighErrorRate 5xx > 1 porcento, HighLatency p99 > 1s, DatabaseConnectionsHigh). AlertManager routing Slack/email/PagerDuty. Recording rules pre-computando aggregations para Grafana.

---

**Última atualização:** 2025-12-29
