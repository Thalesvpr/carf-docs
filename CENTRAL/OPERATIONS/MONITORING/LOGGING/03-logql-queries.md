# LogQL Queries

Queries LogQL úteis para análise de logs do CARF no Grafana/Loki.

## Sintaxe Básica

```logql
# Estrutura básica
{label="value"} |= "string" | json | line_format "{{.field}}"

# Operadores de filtro
|=  # contém string
!=  # não contém string
|~  # regex match
!~  # regex não match
```

## Queries de Aplicação (GEOAPI)

### Erros

```logql
# Todos os erros
{app="geoapi"} |= "error"

# Erros por nível
{app="geoapi"} | json | level="error"

# Exceptions com stack trace
{app="geoapi"} | json | exception!=""

# Erros 5xx
{app="geoapi"} | json | status_code >= 500

# Top 10 tipos de erro
sum by (exception) (count_over_time({app="geoapi"} | json | exception!="" [1h]))
```

### Performance

```logql
# Requests lentos (> 1000ms)
{app="geoapi"} | json | duration_ms > 1000

# Requests por endpoint
sum by (endpoint) (count_over_time({app="geoapi"} | json [5m]))

# Latência média por endpoint (últimos 5min)
avg by (endpoint) (
  avg_over_time({app="geoapi"} | json | unwrap duration_ms [5m])
)

# Requests por status code
sum by (status_code) (count_over_time({app="geoapi"} | json [1h]))
```

### Tracing

```logql
# Buscar por correlation ID
{app="geoapi"} |= "abc123-correlation-id"

# Logs de um usuário específico
{app="geoapi"} | json | user_id="user-uuid-here"

# Logs de um tenant específico
{app="geoapi", tenant_id="tenant-123"}
```

## Queries de Autenticação (Keycloak)

```logql
# Falhas de login
{app="keycloak"} |= "LOGIN_ERROR"

# Logins bem sucedidos
{app="keycloak"} |= "LOGIN" |= "success"

# Tokens expirados
{app="keycloak"} |= "token" |= "expired"

# Top usuários com falha de login
topk(10, sum by (username) (count_over_time({app="keycloak"} |= "LOGIN_ERROR" | json [24h])))
```

## Queries de Database

```logql
# Slow queries do PostgreSQL
{app="postgres"} | json | duration > "1s"

# Erros de conexão
{app="geoapi"} |= "connection" |= "refused"

# Deadlocks
{app="postgres"} |= "deadlock"

# RLS violations
{app="geoapi"} |= "RLS" |= "violation"
```

## Queries de Infraestrutura

```logql
# OOMKilled pods
{namespace="carf"} |= "OOMKilled"

# Restarts de containers
{namespace="carf"} |= "Started container"

# Erros de pull de imagem
{namespace="carf"} |= "Failed to pull image"

# Probes falhando
{namespace="carf"} |= "Liveness probe failed"
```

## Métricas de Logs

```logql
# Taxa de logs por app
sum by (app) (rate({namespace="carf"} [5m]))

# Volume de erros por hora
sum(count_over_time({app="geoapi"} | json | level="error" [1h]))

# Percentual de erros
(
  sum(count_over_time({app="geoapi"} | json | level="error" [5m]))
  /
  sum(count_over_time({app="geoapi"} [5m]))
) * 100
```

## Alerting Rules (Loki)

```yaml
# loki-rules.yaml
groups:
  - name: geoapi-log-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          (sum(count_over_time({app="geoapi"} | json | level="error" [5m]))
          /
          sum(count_over_time({app="geoapi"} [5m]))) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Taxa de erro nos logs acima de 5%"

      - alert: ExceptionSpike
        expr: |
          sum(count_over_time({app="geoapi"} | json | exception!="" [5m])) > 10
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Mais de 10 exceptions em 5 minutos"
```

## Dicas de Performance

- Use labels específicos para filtrar antes de parsear
- Evite regex complexas em grandes volumes
- Use `line_format` para simplificar output
- Limite time range em queries pesadas
- Prefira `count_over_time` a `sum` para contagem

```logql
# Bom (filtra por label primeiro)
{app="geoapi", level="error"}

# Ruim (parseia tudo antes de filtrar)
{namespace="carf"} | json | app="geoapi" | level="error"
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
