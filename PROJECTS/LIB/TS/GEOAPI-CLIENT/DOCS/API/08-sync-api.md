---
type: leaf
status: review
updated: 2026-02-08
---

# Sync API - Sincronizacao Offline

A Sync API gerencia sincronizacao bidirecional entre REURBCAD mobile e GEOAPI backend usando protocolo delta-based com controle de conflitos via version field. Acessada via propriedade sync da instancia GeoApiClient. Tipos SyncLog, SyncStatus, SyncPushRequest e SyncPullResponse importados de @carf/tscore/types conforme [05-types-dtos](../../TSCORE/DOCS/API/05-types-dtos.md). Restrita a roles field-coordinator e field-cadastrator conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| GET | /api/sync/changes?since= | Pull de mudancas desde timestamp | 200 | 401 | field-coordinator, field-cadastrator |
| POST | /api/sync/push | Push de operacoes locais em batch | 200 | 401, 409 SYNC_CONFLICT | field-coordinator, field-cadastrator |
| GET | /api/sync/status | Status da ultima sincronizacao | 200 | - | field-coordinator, field-cadastrator |

## pullChanges (GET /api/sync/changes)

Obtem mudancas do servidor desde o ultimo sync bem-sucedido. Aceita parametro since como string ISO 8601 correspondente ao serverTimestamp retornado no pull anterior. Na primeira sincronizacao, since deve ser omitido ou usar "1970-01-01T00:00:00Z" para obter todos os dados.

Response retorna SyncPullResponse:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| units | SyncEntityChanges de Unit | Mudancas em unidades habitacionais |
| holders | SyncEntityChanges de Holder | Mudancas em titulares |
| communities | SyncEntityChanges de Community | Mudancas em comunidades |
| serverTimestamp | string | ISO 8601 para uso como since no proximo pull |
| hasMore | boolean | Se true, existem mais mudancas; chamar novamente com mesmo since |

Cada SyncEntityChanges contem tres arrays: created (registros novos completos com todos os campos), updated (registros modificados completos substituindo a versao local) e deleted (array de UUIDs de registros removidos via soft delete). O app REURBCAD deve iterar pelas colecoes aplicando upserts para created e updated e marcando como deletados os IDs em deleted no WatermelonDB local.

Quando hasMore e true, o client deve fazer chamadas adicionais com o mesmo since ate receber hasMore false. Isso ocorre quando ha grande volume de mudancas que excedem o tamanho maximo de resposta (paginacao implícita). Apos processar todas as paginas, o client armazena o serverTimestamp como referencia para o proximo pull.

O pull retorna apenas dados das comunidades autorizadas para o usuario conforme CommunityAuthorization. Dados de comunidades nao autorizadas nao sao incluidos, implementando isolamento de acesso no nivel da sincronizacao.

## pushChanges (POST /api/sync/push)

Envia operacoes locais pendentes para o servidor em batch. Aceita SyncPushRequest no body:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| operations | array de SyncOperation | Operacoes a sincronizar |

Cada SyncOperation contem:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| entityType | string | UNIT, HOLDER ou DOCUMENT |
| localId | string | ID local do WatermelonDB |
| operation | string | CREATE, UPDATE ou DELETE |
| payload | objeto | Dados completos da entidade conforme DTO correspondente |
| clientTimestamp | string | ISO 8601 do momento da operacao local no dispositivo |

O servidor processa operacoes sequencialmente, validando regras de negocio de cada entidade. Response retorna SyncPushResponse:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| results | array de SyncResult | Resultado por operacao |

Cada SyncResult contem:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| localId | string | ID local para correlacao com operacao enviada |
| status | string | SUCCESS, CONFLICT ou ERROR |
| serverId | string ou null | UUID atribuido pelo servidor quando CREATE com SUCCESS |
| conflictData | SyncConflict ou null | Dados de conflito quando status CONFLICT |
| error | string ou null | Mensagem de erro quando status ERROR |

SyncConflict contem serverVersion (number com version do servidor) e clientVersion (number com version enviada pelo client), alem de serverData (objeto com dados atuais do servidor para resolucao manual).

O app REURBCAD deve tratar cada resultado: para SUCCESS, atualizar o mapeamento localId-serverId e remover da fila local; para CONFLICT, apresentar ao usuario opcao de manter versao local ou aceitar versao do servidor; para ERROR, manter na fila para re-tentativa futura e logar o erro.

## getStatus (GET /api/sync/status)

Consulta status da ultima sincronizacao sem parametros. Response retorna SyncStatusResponse:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| lastSyncAt | string ou null | ISO 8601 da ultima sync bem-sucedida |
| pendingConflicts | number | Conflitos aguardando resolucao |
| pendingOperations | number | Operacoes na fila do servidor |

## Fluxo Completo de Sincronizacao

O ciclo de sincronizacao do REURBCAD segue a ordem: primeiro executa pull para obter mudancas do servidor e aplicar localmente (evitando que dados locais desatualizados causem conflitos desnecessarios), depois executa push para enviar operacoes locais pendentes, e finalmente verifica status para confirmar que nao restam conflitos. O OfflineIndicator do @carf/ui-native exibe pendingCount baseado na contagem de operacoes locais nao sincronizadas.
