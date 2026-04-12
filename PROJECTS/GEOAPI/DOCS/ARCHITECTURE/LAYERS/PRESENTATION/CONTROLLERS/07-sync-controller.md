---
type: leaf
status: review
updated: 2026-02-08
---

# Sync Controller

O SyncController gerencia a sincronizacao bidirecional entre o app mobile REURBCAD e o servidor GEOAPI. A rota base e /api/sync. Todos os endpoints sao restritos a roles field-coordinator e field-cadastrator, pois apenas agentes de campo utilizam o protocolo de sincronizacao offline.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /api/sync/changes?since= | Pull mudancas desde timestamp | 200 | 401 | field-coordinator, field-cadastrator |
| POST | /api/sync/push | Push batch de operacoes | 200 | 401, 409 SYNC_CONFLICT | field-coordinator, field-cadastrator |
| GET | /api/sync/status | Status da ultima sync | 200 | - | field-coordinator, field-cadastrator |

## Comportamento

O endpoint de pull recebe query param since como timestamp ISO 8601 e despacha GetSyncChangesQuery. O handler consulta registros com updated_at posterior ao timestamp informado, filtrados por tenant e comunidades autorizadas do usuario, retornando objeto com colecoes units, holders e communities subdivididas em created, updated e deleted, alem de serverTimestamp e hasMore. O endpoint de push recebe array operations no body, cada uma com entityType, localId, operation (CREATE, UPDATE, DELETE), payload e clientTimestamp. O handler processa sequencialmente, valida regras de negocio e detecta conflitos comparando version do registro. O response retorna array results com localId, status (SUCCESS, CONFLICT, ERROR), serverId (para CREATE) e conflictData (serverVersion e clientVersion dos campos divergentes para CONFLICT). O endpoint de status retorna lastSyncAt, pendingConflicts e pendingOperations.

## Autorizacao

Todos os endpoints sao restritos a field-coordinator e field-cadastrator. O isolamento por tenant garante que o pull retorna apenas dados do tenant do usuario. Adicionalmente, os dados sao filtrados pelas comunidades autorizadas da equipe do usuario.
