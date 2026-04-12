---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-077: Cache Distribuido

## Descricao

Redis Cluster ou Sentinel para alta disponibilidade. Replicacao para read scaling. Eviction policy LRU remove dados menos usados. Hash slots para distribuicao uniforme.

## Metricas

- Replicacao: read replicas para distribuir leituras
- Eviction: LRU quando memoria atinge limite
- Particionamento: hash slots consistentes

## Criterios de Aceitacao

1. Adicao/remocao de nos sem interrupcao de servico
2. Failover automatico em caso de falha do primario
3. Metricas de hit rate, latencia e memoria monitoradas
