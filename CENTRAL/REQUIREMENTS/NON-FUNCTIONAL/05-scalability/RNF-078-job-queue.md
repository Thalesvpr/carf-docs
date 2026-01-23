---
id: RNF-078
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-078: Job Queue

## Descricao

BullMQ ou similar baseado em Redis para processos assincronos. Workers escalaveis horizontalmente. Dead letter queue para falhas. Priorizacao de jobs criticos.

## Metricas

- Persistencia: jobs sobrevivem restart de workers
- Retry: exponential backoff para falhas transientes
- Priorizacao: multiplas filas por nivel de prioridade

## Criterios de Aceitacao

1. Jobs persistidos, nenhum trabalho perdido
2. Dead letter queue para jobs que falharam apos multiplas tentativas
3. Metricas de tempo de processamento, sucesso e profundidade de fila
