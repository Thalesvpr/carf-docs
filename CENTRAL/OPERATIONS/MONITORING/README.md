# MONITORING

Configuração de observabilidade do CARF organizada em PROMETHEUS (prometheus.yml com scrape configs para GEOAPI /metrics endpoint, PostgreSQL exporter, Keycloak metrics; alerts.yml com regras de alerta para high CPU, memory, disk, error rate, latency p99), GRAFANA (subpasta dashboards/ com JSON exports de dashboards para GEOAPI (requests/sec, latency, error rate), PostgreSQL (connections, queries, cache hit ratio), e Infrastructure (CPU, memory, disk, network); provisioning/ com datasources e dashboards auto-provisionados), e LOGGING (log-aggregation.md documentando stack Loki ou ELK para centralizar logs de todos containers, structured logging JSON com correlation IDs para distributed tracing; log-retention.md com política de 90 dias para logs normais, 1 ano para audit logs). Define SLOs (Service Level Objectives: 99.5% uptime, p99 latency < 500ms) e SLIs (Service Level Indicators) monitorados.

## Estrutura

- **[PROMETHEUS/](./PROMETHEUS/README.md)** - Prometheus scrape configs, alert rules e recording rules
- **[GRAFANA/](./GRAFANA/README.md)** - Dashboards JSON e provisioning automático
- **[LOGGING/](./LOGGING/README.md)** - Agregação de logs com Loki/ELK e políticas de retention

---

**Última atualização:** 2025-12-29
