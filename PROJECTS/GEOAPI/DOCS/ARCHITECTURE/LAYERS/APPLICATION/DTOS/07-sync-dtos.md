---
type: leaf
status: review
updated: 2026-02-08
---

# Sync DTOs

Os Data Transfer Objects de sincronizacao definem os contratos de entrada e saida do protocolo de sync entre REURBCAD e GEOAPI.

## DTOs de Request

SyncPushRequest contem operations (lista obrigatoria de SyncOperationDto).

SyncOperationDto define cada operacao do batch.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| EntityType | string | UNIT, HOLDER ou DOCUMENT |
| LocalId | string | ID local do WatermelonDB |
| Operation | string | CREATE, UPDATE ou DELETE |
| Payload | object | Dados da entidade |
| ClientTimestamp | DateTime | Timestamp da operacao no client |

## DTOs de Resposta

SyncChangesDto e o DTO retornado pelo pull de mudancas.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Units | SyncCollectionDto | Mudancas em unidades |
| Holders | SyncCollectionDto | Mudancas em titulares |
| Communities | SyncCollectionDto | Mudancas em comunidades |
| ServerTimestamp | DateTime | Timestamp para proximo pull |
| HasMore | bool | Se existem mais mudancas |

SyncCollectionDto contem Created (array de registros novos com todos os campos), Updated (array de registros modificados com version) e Deleted (array de UUIDs removidos).

SyncPushResultDto contem Results (lista de SyncOperationResultDto).

SyncOperationResultDto define o resultado de cada operacao.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| LocalId | string | ID local para correlacao |
| Status | string | SUCCESS, CONFLICT ou ERROR |
| ServerId | Guid | UUID atribuido em CREATE (nullable) |
| ConflictData | ConflictDto | Dados de conflito (nullable) |

ConflictDto contem ServerVersion (object com campos do servidor) e ClientVersion (object com campos do client divergentes).

SyncStatusDto contem LastSyncAt (DateTime), PendingConflicts (int) e PendingOperations (int).
