---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOAPI
---

# RF-192: Endpoint de Pull

## Descricao

GEOAPI deve fornecer endpoint especializado GET /api/sync/pull que implementa sincronizacao incremental eficiente para dispositivos moveis, aceitando parametro lastPulledAt contendo timestamp ISO 8601 da ultima sincronizacao bem-sucedida. Endpoint consulta banco de dados identificando registros (unidades, titulares, fotos) criados, modificados ou deletados apos timestamp fornecido, retornando apenas subconjunto de alteracoes. Resposta estruturada em JSON agrupa alteracoes por tipo de operacao incluindo arrays created para registros novos, updated para modificados com todos campos atualizados, e deleted contendo apenas identificadores de registros removidos. Payload utiliza formato compacto omitindo campos nulos e aplicando compressao gzip no HTTP minimizando transferencia em conexoes moveis lentas. Dados filtrados por tenant_id do usuario autenticado.

## Criterios de Aceitacao

1. Endpoint GET /api/sync/pull
2. Parametro lastPulledAt em ISO 8601
3. Resposta com arrays created, updated, deleted
4. Compressao gzip
5. Filtragem por tenant_id

## Rastreabilidade

- Modulos: GEOAPI
- Requisitos dependentes: RF-017
