---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
  - GEOAPI
---

# RF-189: Delta Sync Incremental

## Descricao

Sistema deve implementar sincronizacao incremental eficiente que transmite apenas dados alterados desde ultima sincronizacao bem-sucedida, reduzindo drasticamente tempo de sincronizacao e consumo de banda em contextos de conectividade limitada. Implementacao mantem timestamps de ultima sincronizacao persistidos localmente e utiliza endpoint GET /api/sync/pull com parametro lastPulledAt permitindo ao servidor retornar apenas registros criados ou modificados apos aquele timestamp. Na direcao push, aplicativo envia apenas dados criados ou editados localmente identificados atraves de flags de pendencia e timestamps de modificacao no SQLite, evitando retransmissao de dados ja sincronizados. Padrao delta sync fundamental para viabilizar uso em areas com conectividade precaria onde sincronizacoes completas seriam impraticaveis.

## Criterios de Aceitacao

1. Transmissao apenas de dados alterados
2. Timestamps de ultima sincronizacao persistidos
3. Endpoint pull com parametro lastPulledAt
4. Push apenas de registros pendentes
5. Reducao significativa de consumo de banda

## Rastreabilidade

- Modulos: REURBCAD, GEOAPI
- Requisitos dependentes: RF-187, RF-192, RF-193
