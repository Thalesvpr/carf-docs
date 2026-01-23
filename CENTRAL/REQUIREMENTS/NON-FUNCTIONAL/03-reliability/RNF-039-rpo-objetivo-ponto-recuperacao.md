---
id: RNF-039
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-039: RPO (Recovery Point Objective)

## Descricao

Perda maxima aceitavel de dados em caso de falha catastrofica. WAL archiving garante que transacoes das ultimas 60 minutos possam ser recuperadas.

## Metricas

- RPO: maximo 1 hora
- WAL archiving: archive_timeout de 60 segundos
- Replicacao: sincrona ou assincrona para standby

## Criterios de Aceitacao

1. WAL archiving habilitado com segmentos copiados em ate 5 minutos
2. Testes de point-in-time recovery trimestrais
3. Monitoramento de lag de replicacao com alertas
