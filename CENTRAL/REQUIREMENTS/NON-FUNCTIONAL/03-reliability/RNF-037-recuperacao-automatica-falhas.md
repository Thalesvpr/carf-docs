---
id: RNF-037
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-037: Recuperacao de Falhas

## Descricao

GEOAPI deve implementar recuperacao automatica para falhas transientes sem intervencao manual. Inclui restart de containers, circuit breaker e retry com backoff.

## Metricas

- Restart: Kubernetes reinicia containers em ate 30 segundos
- Circuit breaker: abre apos 5 falhas, aguarda 60s para retry
- Backoff: exponencial de 100ms ate 30s com jitter

## Criterios de Aceitacao

1. Containers reiniciados automaticamente via health/readiness probes
2. Circuit breaker implementado com Polly para servicos externos
3. Metricas de falhas e recuperacoes expostas via Prometheus
