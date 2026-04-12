---
type: leaf
status: review
description: "Runbook de monitoramento Keycloak com health checks, metricas, alertas e logs."
updated: 2026-02-07
---

# Monitoramento Keycloak

## Health Check

O endpoint /health retorna status UP ou DOWN indicando disponibilidade geral. O endpoint /health/ready verifica se a aplicacao esta pronta para receber trafego e /health/live confirma que o processo esta respondendo, ambos uteis como Kubernetes probes. Healthcheck automatizado via cron a cada cinco minutos dispara notificacao por email ao administrador caso o servico esteja indisponivel.

## Metricas

Metricas Prometheus sao expostas no endpoint /metrics incluindo contadores de sessoes ativas, taxa de logins bem-sucedidos, erros de autenticacao e histogramas de latencia de requisicoes. Prometheus coleta essas metricas a cada trinta segundos apontando para o servico Keycloak na porta 8080. Em Kubernetes, um ServiceMonitor seleciona pods com label app keycloak configurando scraping automatico via Prometheus Operator.

## Grafana e Alertas

Dashboard Grafana visualiza taxa de logins por segundo, taxa de erros, sessoes ativas e percentil noventa e cinco de latencia. Alertas criticos configurados no Alertmanager disparam se Keycloak ficar indisponivel por dois minutos, se taxa de erros de login superar dez por segundo por cinco minutos, se P95 de latencia ultrapassar dois segundos ou se disco disponivel cair abaixo de dez por cento.

## Logs e Eventos

Fluent Bit recebe logs via protocolo forward, parseia JSON estruturado e envia para Elasticsearch no indice keycloak-logs permitindo busca e analise centralizada via Kibana. Eventos Keycloak de LOGIN, LOGOUT, LOGIN_ERROR, REGISTER e UPDATE_PASSWORD sao salvos por sete dias e consultaveis via Admin API para analise de seguranca.

## Operacao Continua

O monitoramento completo exige health check executando a cada cinco minutos, metricas coletadas pelo Prometheus, dashboard Grafana configurado e alertas criticos ativos para indisponibilidade e alta taxa de erros. Logs devem estar centralizados em Elasticsearch ou CloudWatch. Backup diario automatizado com teste de restore mensal e revisao semanal de eventos completam a postura operacional.
