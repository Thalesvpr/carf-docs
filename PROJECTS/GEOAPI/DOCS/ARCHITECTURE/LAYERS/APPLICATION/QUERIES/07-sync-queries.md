---
type: leaf
status: review
updated: 2026-02-08
---

# Sync Queries

As queries de sincronizacao implementam o lado de leitura do protocolo de sync entre REURBCAD e GEOAPI, fornecendo delta de mudancas e status de sincronizacao.

## GetSyncChangesQuery

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| Since | DateTime | obrigatorio | Timestamp ISO 8601 da ultima sync |

O handler consulta registros com updated_at posterior ao timestamp informado, filtrados por tenant_id do JWT e comunidades autorizadas do usuario via community_authorizations. O response retorna objeto com tres colecoes (units, holders, communities), cada uma subdividida em created (registros novos com todos os campos), updated (registros modificados com todos os campos incluindo version) e deleted (array de UUIDs removidos). Inclui serverTimestamp (timestamp do servidor para uso como since no proximo pull) e hasMore (boolean indicando se existem mais mudancas, permitindo paginacao incremental).

O handler limita cada colecao a 500 registros por pull para evitar payloads excessivos. Quando hasMore e true, o client deve fazer novo pull com o serverTimestamp retornado ate que hasMore seja false.

## GetSyncStatusQuery

Sem parametros. O handler consulta sync_logs do usuario autenticado e retorna objeto com lastSyncAt (timestamp da ultima sync bem-sucedida), pendingConflicts (contagem de conflitos com conflict_resolved false) e pendingOperations (contagem de operacoes na fila do servidor aguardando processamento).
