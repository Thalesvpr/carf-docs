---
id: RNF-072
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-072: Usuarios Simultaneos

## Descricao

Sistema deve suportar 500 usuarios simultaneos sem degradacao significativa. Testes de carga com k6/JMeter simulam fluxos realistas. Mecanismos de protecao: rate limiting, circuit breakers, graceful degradation.

## Metricas

- Usuarios: >= 500 simultaneos
- Latencia p95: <= 2x baseline sob carga
- Error rate: < 1% sob carga

## Criterios de Aceitacao

1. Load tests com 500 usuarios virtuais executam fluxos realistas
2. Protecao contra sobrecarga previne indisponibilidade total
3. Testes executados regularmente no pipeline CI/CD
