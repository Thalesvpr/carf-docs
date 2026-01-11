# GRAFANA

Configuração Grafana dashboards do CARF. DASHBOARDS contém JSON exports (geoapi-dashboard.json, postgres-dashboard.json, infrastructure-dashboard.json com panels requests/latency/errors/resources). PROVISIONING contém configs auto-provision (datasources.yml Prometheus/Loki, dashboards.yml auto-import). Alerting via Grafana alerts, notification channels Slack. Variables dashboards (environment dropdown, time range, tenant filter).

## Estrutura

- **[DASHBOARDS/](./DASHBOARDS/README.md)** - Dashboards JSON exports (GEOAPI, PostgreSQL, Infrastructure)
- **[PROVISIONING/](./PROVISIONING/README.md)** - Configs de datasources, dashboards e notifiers auto-provisionados

---

**Última atualização:** 2025-12-29
