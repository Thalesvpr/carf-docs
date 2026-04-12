---
type: leaf
status: review
updated: 2026-02-08
---

# Monitoring

Documentacao completa da estrategia de monitoramento da GEOAPI, cobrindo metricas Prometheus, dashboards Grafana, alertas, logs e health checks.

## Metricas Prometheus

A GEOAPI expoe metricas no endpoint `/metrics` (formato Prometheus), protegido por IP whitelist (somente Prometheus scraper).

### Metricas HTTP

| Metrica | Tipo | Labels | Descricao |
|---------|------|--------|-----------|
| http_request_duration_seconds | Histogram | method, endpoint, status_code | Duracao das requisicoes HTTP |
| http_requests_total | Counter | method, endpoint, status_code | Total de requisicoes HTTP |
| http_requests_in_progress | Gauge | method | Requisicoes em andamento |
| http_request_size_bytes | Histogram | method, endpoint | Tamanho do request body |
| http_response_size_bytes | Histogram | method, endpoint | Tamanho do response body |

### Metricas de Banco de Dados

| Metrica | Tipo | Labels | Descricao |
|---------|------|--------|-----------|
| db_query_duration_seconds | Histogram | query_type, entity | Duracao de queries no banco |
| db_connections_active | Gauge | - | Conexoes ativas no pool |
| db_connections_idle | Gauge | - | Conexoes ociosas no pool |
| db_connections_max | Gauge | - | Maximo de conexoes configurado |
| db_migrations_applied | Gauge | - | Numero de migrations aplicadas |

### Metricas de Cache

| Metrica | Tipo | Labels | Descricao |
|---------|------|--------|-----------|
| cache_hits_total | Counter | entity_type, operation | Total de cache hits |
| cache_misses_total | Counter | entity_type, operation | Total de cache misses |
| cache_evictions_total | Counter | entity_type, reason | Total de evictions |
| cache_hit_ratio | Gauge | entity_type | Ratio de hits (calculado) |
| cache_latency_seconds | Histogram | operation | Latencia de operacoes no Redis |

### Metricas Hangfire

| Metrica | Tipo | Labels | Descricao |
|---------|------|--------|-----------|
| hangfire_jobs_processed_total | Counter | job_type, queue, status | Total de jobs processados |
| hangfire_jobs_failed_total | Counter | job_type, queue | Total de jobs falhados |
| hangfire_jobs_duration_seconds | Histogram | job_type, queue | Duracao de execucao dos jobs |
| hangfire_queue_depth | Gauge | queue | Profundidade da fila (jobs pendentes) |
| hangfire_workers_active | Gauge | - | Workers ativos |

### Metricas de Storage

| Metrica | Tipo | Labels | Descricao |
|---------|------|--------|-----------|
| storage_upload_duration_seconds | Histogram | document_type | Duracao de uploads para S3 |
| storage_download_duration_seconds | Histogram | document_type | Duracao de downloads do S3 |
| storage_upload_size_bytes | Histogram | document_type | Tamanho dos arquivos uploaded |
| storage_errors_total | Counter | operation, error_type | Total de erros de storage |

### Metricas de Autenticacao

| Metrica | Tipo | Labels | Descricao |
|---------|------|--------|-----------|
| auth_token_validations_total | Counter | result | Total de validacoes de token (success/failure) |
| auth_token_validation_duration_seconds | Histogram | - | Duracao da validacao de token |
| auth_unauthorized_requests_total | Counter | endpoint | Total de requisicoes 401 |
| auth_forbidden_requests_total | Counter | endpoint, role | Total de requisicoes 403 |

## Dashboards Grafana

### Dashboard 1: Request Overview

Visao geral do trafego HTTP da API.

| Painel | Query PromQL | Visualizacao |
|--------|-------------|-------------|
| Request Rate | rate(http_requests_total[5m]) | Grafico de linha |
| Latency p50 | histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m])) | Grafico de linha |
| Latency p95 | histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) | Grafico de linha |
| Latency p99 | histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) | Grafico de linha |
| Error Rate (5xx) | rate(http_requests_total{status_code=~"5.."}[5m]) / rate(http_requests_total[5m]) | Gauge |
| Error Rate (4xx) | rate(http_requests_total{status_code=~"4.."}[5m]) / rate(http_requests_total[5m]) | Gauge |
| Top Endpoints | topk(10, sum by (endpoint)(rate(http_requests_total[5m]))) | Tabela |
| Request In Progress | http_requests_in_progress | Gauge |

### Dashboard 2: Database

Monitoramento do PostgreSQL e das queries.

| Painel | Query PromQL | Visualizacao |
|--------|-------------|-------------|
| Query Duration p95 | histogram_quantile(0.95, rate(db_query_duration_seconds_bucket[5m])) | Grafico de linha |
| Connection Pool | db_connections_active / db_connections_max | Gauge |
| Active Connections | db_connections_active | Grafico de linha |
| Idle Connections | db_connections_idle | Grafico de linha |
| Slow Queries | histogram_quantile(0.99, rate(db_query_duration_seconds_bucket[5m])) > 1 | Tabela |

### Dashboard 3: Cache

Monitoramento do Redis e eficacia do cache.

| Painel | Query PromQL | Visualizacao |
|--------|-------------|-------------|
| Hit Ratio Global | sum(cache_hits_total) / (sum(cache_hits_total) + sum(cache_misses_total)) | Gauge |
| Hit Ratio por Entidade | cache_hits_total / (cache_hits_total + cache_misses_total) | Grafico de barras |
| Cache Latency p95 | histogram_quantile(0.95, rate(cache_latency_seconds_bucket[5m])) | Grafico de linha |
| Evictions Rate | rate(cache_evictions_total[5m]) | Grafico de linha |

### Dashboard 4: Hangfire Jobs

Monitoramento dos jobs assincronos.

| Painel | Query PromQL | Visualizacao |
|--------|-------------|-------------|
| Jobs Processed/hour | rate(hangfire_jobs_processed_total[1h]) * 3600 | Gauge |
| Failed Jobs | rate(hangfire_jobs_failed_total[1h]) * 3600 | Gauge |
| Queue Depth | hangfire_queue_depth | Grafico de linha (por fila) |
| Job Duration p95 | histogram_quantile(0.95, rate(hangfire_jobs_duration_seconds_bucket[5m])) | Grafico de linha |
| Workers Active | hangfire_workers_active | Gauge |

### Dashboard 5: Infrastructure

Metricas de infraestrutura do Kubernetes.

| Painel | Query PromQL | Visualizacao |
|--------|-------------|-------------|
| CPU Usage | container_cpu_usage_seconds_total{pod=~"geoapi-.*"} | Grafico de linha |
| Memory Usage | container_memory_usage_bytes{pod=~"geoapi-.*"} | Grafico de linha |
| Pod Count | count(kube_pod_info{namespace="production", app="geoapi"}) | Gauge |
| Restart Count | kube_pod_container_status_restarts_total{namespace="production", app="geoapi"} | Counter |
| Disk Usage | kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes | Gauge |

## Alertas

### Tabela de Alertas

| Metrica | Query PromQL | Threshold | Duracao | Severidade | Canal |
|---------|-------------|-----------|---------|-----------|-------|
| Error Rate 5xx | rate(http_requests_total{status_code=~"5.."}[5m]) / rate(http_requests_total[5m]) | > 1% | 5min | Critical | Slack #alerts-critical |
| Latency p99 | histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) | > 2s | 5min | Warning | Slack #alerts-warning |
| DB Connections | db_connections_active / db_connections_max | > 80% | 5min | Warning | Slack #alerts-warning |
| Cache Hit Ratio | cache_hit_ratio | < 50% | 10min | Info | Slack #alerts-info |
| Disk Usage | kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes | > 80% | 5min | Warning | Slack #alerts-warning |
| Pod Restarts | increase(kube_pod_container_status_restarts_total[1h]) | > 3 | Imediato | Critical | Slack #alerts-critical |
| Hangfire Queue Critical | hangfire_queue_depth{queue="critical"} | > 10 | 5min | Critical | Slack #alerts-critical |
| Hangfire Queue Default | hangfire_queue_depth{queue="default"} | > 100 | 15min | Warning | Slack #alerts-warning |
| Memory Usage | container_memory_usage_bytes / container_spec_memory_limit_bytes | > 90% | 5min | Warning | Slack #alerts-warning |
| Health Check Fail | up{job="geoapi"} | == 0 | 1min | Critical | Slack #alerts-critical + PagerDuty |

### Severidades

| Severidade | Descricao | Canal | Tempo de Resposta |
|-----------|-----------|-------|------------------|
| Critical | Servico indisponivel ou degradado significativamente | Slack #alerts-critical + PagerDuty | 15 min (horario comercial), 1h (fora) |
| Warning | Performance degradada mas servico funcional | Slack #alerts-warning | 4h (horario comercial) |
| Info | Informativo, pode requerer atencao futura | Slack #alerts-info | Proximo dia util |

## Log Aggregation

### Stack de Logging

```
Aplicacao (Serilog) → Elasticsearch → Kibana
```

### Configuracao Serilog

A GEOAPI utiliza Serilog com structured logging em formato JSON. Toda entrada de log inclui campos padrao.

| Campo | Fonte | Exemplo | Descricao |
|-------|-------|---------|-----------|
| @timestamp | Serilog | 2026-02-08T10:30:00Z | Data/hora UTC do log |
| Level | Serilog | Information, Warning, Error | Nivel do log |
| Message | Aplicacao | "Unit created successfully" | Mensagem descritiva |
| CorrelationId | CorrelationIdMiddleware | "a1b2c3d4-e5f6-..." | ID unico por requisicao HTTP |
| TenantId | TenantMiddleware | "tenant-uuid" | ID do tenant atual |
| UserId | CurrentUser | "user-uuid" | ID do usuario autenticado |
| RequestPath | RequestLoggingMiddleware | "/api/units" | Path da requisicao |
| RequestMethod | RequestLoggingMiddleware | "POST" | Metodo HTTP |
| StatusCode | RequestLoggingMiddleware | 201 | Status code da resposta |
| Duration | RequestLoggingMiddleware | 45.2 | Duracao em ms |
| SourceContext | Serilog | "Carf.GeoApi.Application.Commands.Units.CreateUnitHandler" | Classe que gerou o log |
| Exception | Serilog | stack trace | Stack trace em caso de excecao |

### Niveis de Log

| Nivel | Uso | Exemplos |
|-------|-----|---------|
| Verbose | Debug detalhado (somente dev) | Query SQL executada, payload completo |
| Debug | Informacoes de desenvolvimento | Cache hit/miss, mapper executado |
| Information | Eventos de negocio relevantes | Unidade criada, holder vinculado, login realizado |
| Warning | Situacoes inesperadas nao criticas | Cache miss rate alto, retry de job, token proximo de expirar |
| Error | Erros que afetam funcionalidade | Falha de conexao DB, upload S3 falhou, validacao inesperada |
| Fatal | Erros criticos que impedem funcionamento | Aplicacao nao consegue iniciar, DB inacessivel |

### Consultas Kibana Frequentes

| Cenario | Query KQL |
|---------|-----------|
| Erros de uma requisicao | CorrelationId: "a1b2c3d4-..." AND Level: "Error" |
| Todas as acoes de um usuario | UserId: "user-uuid" AND Level: "Information" |
| Erros de um tenant | TenantId: "tenant-uuid" AND Level: ("Error" OR "Fatal") |
| Requisicoes lentas (>1s) | Duration > 1000 |
| Falhas de autenticacao | RequestPath: "/api/*" AND StatusCode: 401 |
| Jobs falhados | SourceContext: "*Job*" AND Level: "Error" |

### Retencao de Logs

| Ambiente | Retencao | Indice Elasticsearch |
|----------|---------|---------------------|
| Development | 7 dias | geoapi-dev-YYYY.MM.DD |
| Staging | 30 dias | geoapi-staging-YYYY.MM.DD |
| Production | 90 dias | geoapi-prod-YYYY.MM.DD |

## Health Check Monitoring

### Monitoramento Externo

Um servico externo (ex: UptimeRobot, Pingdom) realiza verificacoes periodicas nos endpoints de saude.

| Endpoint | Intervalo | Timeout | Alertar apos |
|----------|-----------|---------|-------------|
| /health/live | 30s | 10s | 3 falhas consecutivas |
| /health/ready | 60s | 15s | 3 falhas consecutivas |
| / (homepage) | 60s | 10s | 3 falhas consecutivas |

### Acoes por Tipo de Falha

| Endpoint Falhando | Significado | Acao |
|-------------------|-----------|------|
| /health/live | Processo da aplicacao travou ou esta unresponsive | Kubernetes reinicia o pod automaticamente. Se persistir, investigar memory leak ou deadlock |
| /health/ready | Dependencia externa indisponivel | Verificar PostgreSQL, Redis, Keycloak, S3. Pod e removido do balanceador automaticamente |
| Ambos falhando | Falha completa do pod ou da rede | Verificar node Kubernetes, rede, DNS. Escalar para infra |

## Correlation ID

Toda requisicao HTTP recebe um `CorrelationId` unico (UUID v4) no middleware `CorrelationIdMiddleware`. Este ID:

1. E gerado no inicio da requisicao (ou reutilizado se vier no header `X-Correlation-Id`)
2. E propagado em todos os logs gerados durante a requisicao
3. E incluido no header de resposta `X-Correlation-Id`
4. E passado para jobs Hangfire disparados pela requisicao
5. E passado para chamadas HTTP externas (Keycloak, etc.)

Isso permite rastrear o fluxo completo de uma requisicao atraves de todos os servicos e logs, facilitando debugging em producao.

## Runbook de Incidentes

### Passo a Passo para Investigacao

1. **Identificar**: alerta recebido no Slack com detalhes da metrica violada
2. **Dashboards**: acessar Grafana e verificar os dashboards relevantes
3. **Logs**: pesquisar no Kibana usando CorrelationId ou filtros relevantes
4. **Pods**: verificar status dos pods com `kubectl get pods -n production`
5. **Recursos**: verificar consumo de CPU/memoria com `kubectl top pods -n production`
6. **Dependencias**: verificar saude das dependencias via `/health/ready`
7. **Mitigar**: escalar pods, reiniciar pod problematico, ou fazer rollback se deploy recente
8. **Documentar**: registrar incidente, causa raiz e acoes tomadas