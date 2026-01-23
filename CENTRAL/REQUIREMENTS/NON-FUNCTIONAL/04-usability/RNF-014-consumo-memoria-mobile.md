---
id: RNF-014
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-014: Consumo de Memoria - Mobile

## Descricao

Aplicativo REURBCAD deve operar com consumo limitado de memoria RAM para funcionar em dispositivos de entrada com 2-4GB de RAM total.

## Metricas

- Uso medio de RAM: <= 150MB durante operacao tipica
- Cache local: maximo 500MB para dados offline e mapas
- Ferramenta de medicao: React Native Profiler

## Criterios de Aceitacao

1. Liberacao de memoria ao sair de telas (cleanup de listeners/timers)
2. Imagens comprimidas e dimensionadas apropriadamente
3. FlatList com virtualizacao para listagens longas
