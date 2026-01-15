# MONITORING

Configuração de observabilidade do CARF.

O [Prometheus](./PROMETHEUS/README.md) coleta métricas do GEOAPI, PostgreSQL exporter, Keycloak e node exporter. Alertas configurados incluem HighCPU (>80%), HighMemory (>90%), HighErrorRate (5xx >1%), HighLatency (p99 >1s) e DatabaseConnectionsHigh. AlertManager roteia para Slack, email e PagerDuty.

O [Grafana](./GRAFANA/README.md) exibe dashboards para GEOAPI, PostgreSQL e Infrastructure. Datasources e dashboards são auto-provisionados via JSON exports.

O [Logging](./LOGGING/README.md) usa Loki com Promtail para agregação de logs em formato JSON estruturado. Correlation IDs permitem distributed tracing. Retenção de 90 dias para logs gerais e 1 ano para audit, com archive em S3 após 7 dias.

SLOs definidos: 99.5% uptime e p99 latency menor que 500ms.

## Estrutura

- **[PROMETHEUS/](./PROMETHEUS/README.md)** - Métricas, alertas e recording rules
- **[GRAFANA/](./GRAFANA/README.md)** - Dashboards e visualizações
- **[LOGGING/](./LOGGING/README.md)** - Loki, Promtail e retention policies

---

**Última atualização:** 2026-01-14
