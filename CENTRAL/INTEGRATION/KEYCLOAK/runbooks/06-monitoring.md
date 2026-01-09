# Monitoramento Keycloak

## Health Check

### Endpoint de saúde
```bash
# Health básico
curl http://localhost:8080/health

# Health detalhado
curl http://localhost:8080/health/ready
curl http://localhost:8080/health/live
```

### Healthcheck automatizado
```bash
# Via script
make health

# Via cron (alertar se falhar)
*/5 * * * * make health || echo "Keycloak down!" | mail -s "Alert" admin@carf.gov.br
```

## Métricas

### Endpoint de métricas
```bash
curl http://localhost:8080/metrics
```

### Métricas importantes
```bash
# Usuários ativos
curl -s http://localhost:8080/metrics | grep keycloak_sessions

# Logins por segundo
curl -s http://localhost:8080/metrics | grep keycloak_logins

# Erros de autenticação
curl -s http://localhost:8080/metrics | grep keycloak_login_errors

# Response time
curl -s http://localhost:8080/metrics | grep http_request_duration
```

## Prometheus

### prometheus.yml
```yaml
scrape_configs:
  - job_name: 'keycloak'
    static_configs:
      - targets: ['keycloak:8080']
    metrics_path: '/metrics'
    scrape_interval: 30s
```

### ServiceMonitor (Kubernetes)
```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: keycloak
spec:
  selector:
    matchLabels:
      app: keycloak
  endpoints:
  - port: http
    path: /metrics
```

## Grafana Dashboard

### Queries úteis
```promql
# Taxa de logins
rate(keycloak_logins_total[5m])

# Taxa de falhas
rate(keycloak_login_errors_total[5m])

# Sessões ativas
keycloak_sessions_active

# P95 response time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Uptime
up{job="keycloak"}
```

### Dashboard JSON
```json
{
  "dashboard": {
    "title": "Keycloak CARF",
    "panels": [
      {
        "title": "Login Rate",
        "targets": [{"expr": "rate(keycloak_logins_total[5m])"}]
      },
      {
        "title": "Error Rate",
        "targets": [{"expr": "rate(keycloak_login_errors_total[5m])"}]
      }
    ]
  }
}
```

## Logs

### Centralizados
```bash
# Fluent Bit config
[INPUT]
    Name              forward
    Listen            0.0.0.0
    Port              24224

[FILTER]
    Name parser
    Match keycloak.*
    Key_Name log
    Parser json

[OUTPUT]
    Name  es
    Match keycloak.*
    Host  elasticsearch
    Index keycloak-logs
```

### Queries Elasticsearch
```json
{
  "query": {
    "bool": {
      "must": [
        {"match": {"level": "ERROR"}},
        {"range": {"@timestamp": {"gte": "now-1h"}}}
      ]
    }
  }
}
```

## Alertas

### Prometheus Alertmanager
```yaml
groups:
  - name: keycloak
    rules:
      - alert: KeycloakDown
        expr: up{job="keycloak"} == 0
        for: 2m
        annotations:
          summary: "Keycloak não está respondendo"

      - alert: HighLoginErrors
        expr: rate(keycloak_login_errors_total[5m]) > 10
        for: 5m
        annotations:
          summary: "Taxa alta de erros de login"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 2
        for: 5m
        annotations:
          summary: "Response time alto (P95 > 2s)"

      - alert: DiskSpaceHigh
        expr: (node_filesystem_avail_bytes / node_filesystem_size_bytes) < 0.1
        for: 5m
        annotations:
          summary: "Disco com menos de 10% disponível"
```

## Eventos Keycloak

### Configurar Event Listeners
1. Admin Console → Events → Config
2. Save Events: ON
3. Saved Types: LOGIN, LOGOUT, LOGIN_ERROR, REGISTER, UPDATE_PASSWORD
4. Expiration: 7 days

### Query eventos via API
```bash
TOKEN=$(curl -X POST http://localhost:8080/realms/master/protocol/openid-connect/token \
  -d "client_id=admin-cli" \
  -d "username=admin" \
  -d "password=admin" \
  -d "grant_type=password" | jq -r '.access_token')

# Eventos recentes
curl -s "http://localhost:8080/admin/realms/carf/events?max=100" \
  -H "Authorization: Bearer $TOKEN" | jq

# Filtrar LOGIN_ERROR
curl -s "http://localhost:8080/admin/realms/carf/events?type=LOGIN_ERROR&max=100" \
  -H "Authorization: Bearer $TOKEN" | jq
```

## Checklist de Monitoramento

- [ ] Health check a cada 5 minutos
- [ ] Métricas coletadas pelo Prometheus
- [ ] Dashboard Grafana configurado
- [ ] Alertas críticos ativos (down, high errors)
- [ ] Logs centralizados (Elasticsearch/CloudWatch)
- [ ] Backup diário automatizado
- [ ] Teste de restore mensal
- [ ] Revisão de eventos semanalmente
