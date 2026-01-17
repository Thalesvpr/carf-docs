# MONITORING

Configuração de observabilidade do CARF.

O [Prometheus](./PROMETHEUS/README.md) coleta métricas do GEOAPI, PostgreSQL exporter, Keycloak e node exporter. Alertas configurados incluem HighCPU (>80%), HighMemory (>90%), HighErrorRate (5xx >1%), HighLatency (p99 >1s) e DatabaseConnectionsHigh. AlertManager roteia para Slack, email e PagerDuty.

O [Grafana](./GRAFANA/README.md) exibe dashboards para GEOAPI, PostgreSQL e Infrastructure. Datasources e dashboards são auto-provisionados via JSON exports.

O [Logging](./LOGGING/README.md) usa Loki com Promtail para agregação de logs em formato JSON estruturado. Correlation IDs permitem distributed tracing. Retenção de 90 dias para logs gerais e 1 ano para audit, com archive em S3 após 7 dias.

SLOs definidos: 99.5% uptime e p99 latency menor que 500ms.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Grafana](./GRAFANA/README.md) | 0 |
|  | [Logging](./LOGGING/README.md) | 0 |
|  | [Prometheus](./PROMETHEUS/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
