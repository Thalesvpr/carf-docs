---
status: review
updated: 2026-01-15
---

# MONITORING

Configuração de observabilidade do CARF.

O [Prometheus](./PROMETHEUS/README.md) coleta métricas do GEOAPI, PostgreSQL exporter, Keycloak e node exporter. Alertas configurados incluem HighCPU (>80%), HighMemory (>90%), HighErrorRate (5xx >1%), HighLatency (p99 >1s) e DatabaseConnectionsHigh. AlertManager roteia para Slack, email e PagerDuty.

O [Grafana](./GRAFANA/README.md) exibe dashboards para GEOAPI, PostgreSQL e Infrastructure. Datasources e dashboards são auto-provisionados via JSON exports.

O [Logging](./LOGGING/README.md) usa Loki com Promtail para agregação de logs em formato JSON estruturado. Correlation IDs permitem distributed tracing. Retenção de 90 dias para logs gerais e 1 ano para audit, com archive em S3 após 7 dias.

SLOs definidos: 99.5% uptime e p99 latency menor que 500ms.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (11 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Grafana](./GRAFANA/README.md) | 5 |
|  | [Logging](./LOGGING/README.md) | 3 |
|  | [Prometheus](./PROMETHEUS/README.md) | 3 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/OPERATIONS/MONITORING/GRAFANA/README|GRAFANA]]
- [[CENTRAL/OPERATIONS/MONITORING/LOGGING/README|LOGGING]]
- [[CENTRAL/OPERATIONS/MONITORING/PROMETHEUS/README|PROMETHEUS]]

<!-- CARF-INDEX-END -->
