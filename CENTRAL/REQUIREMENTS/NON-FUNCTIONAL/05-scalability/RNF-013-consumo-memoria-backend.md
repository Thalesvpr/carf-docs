---
id: RNF-013
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-013: Consumo de Memoria - Backend

## Descricao

Container GEOAPI deve operar com ate 2GB RAM em operacao normal e 4GB em pico. Memory profiling regular identifica alocacoes ineficientes. Ausencia de memory leaks obrigatoria.

## Metricas

- Uso normal: <= 2GB RAM
- Uso em pico: <= 4GB RAM
- Memory leaks: zero tolerancia

## Criterios de Aceitacao

1. Memory profiling regular com dotMemory/PerfView
2. Garbage collector otimizado para aplicacao servidora
3. Limites configurados no Kubernetes para prevenir consumo descontrolado
