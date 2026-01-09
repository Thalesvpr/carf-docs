# LOGGING

Agregação logs do CARF. log-aggregation.md documenta stack Loki (Promtail collecting, Loki central, Grafana Explore querying LogQL). Structured logging JSON (Serilog fields timestamp/level/message/correlation_id/tenant_id/user_id). Correlation IDs propagados headers X-Correlation-ID distributed tracing. log-retention.md política (logs 90d, audit 1yr, errors 180d, compress após 7d, archive S3). Alerting on log patterns (error spikes, new exception types).

---

**Última atualização:** 2025-12-29
