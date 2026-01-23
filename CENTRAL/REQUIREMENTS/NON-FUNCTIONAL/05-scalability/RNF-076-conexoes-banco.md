---
id: RNF-076
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-076: Conexoes de Banco

## Descricao

Pool de conexoes otimizado via pgBouncer ou similar. Minimo 10 conexoes permanentes, maximo 100 simultaneas. Timeout para conexoes ociosas permite reciclagem automatica.

## Metricas

- Pool minimo: 10 conexoes
- Pool maximo: 100 conexoes
- Monitoramento: utilizacao, tempo de espera, reciclagem

## Criterios de Aceitacao

1. Carga normal opera sem filas de espera
2. Carga de pico degrada com timeouts controlados
3. Conexoes abandonadas detectadas e recuperadas
