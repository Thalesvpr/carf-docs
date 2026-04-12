---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-071: Escala Horizontal - Backend

## Descricao

GEOAPI completamente stateless para escalar horizontalmente. Estado de sessao em Redis distribuido. Load balancer distribui requisicoes. Auto-scaling baseado em metricas de CPU, memoria e latencia.

## Metricas

- Aplicacao: 100% stateless
- Sessao: armazenada em Redis
- Auto-scaling: baseado em CPU, memoria, throughput

## Criterios de Aceitacao

1. Qualquer requisicao processavel por qualquer instancia
2. Load balancer distribui carga uniformemente
3. Auto-scaling adiciona/remove instancias automaticamente
