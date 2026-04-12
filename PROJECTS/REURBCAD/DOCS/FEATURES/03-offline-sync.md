---
type: leaf
status: review
updated: 2026-02-08
---

# Offline Sync - Sincronizacao

Feature de sincronizacao offline implementada via arquitetura queue-based bidirectional sync, permitindo field collectors trabalharem semanas offline acumulando changes localmente e sincronizando automaticamente quando conexao disponivel.

## Visao Geral

O sistema utiliza `SyncManager` service (singleton) gerenciando o sync lifecycle completo: pull de server changes, push de local changes, conflict resolution e retry logic. A base e o WatermelonDB sync adapter configurado com `pullChanges` e `pushChanges` methods conectando aos GEOAPI sync endpoints (`GET /api/sync/changes`, `POST /api/sync/push`).

## Arquitetura SyncManager

O `SyncManager` e um singleton que coordena todas as operacoes de sincronizacao:

- **Pull**: busca changes do servidor desde o ultimo sync
- **Push**: envia changes locais para o servidor
- **Conflict Resolution**: detecta e resolve conflitos entre versoes
- **Retry Logic**: re-tenta operacoes falhas com exponential backoff

## Modelo de Queue

`SyncQueueModel` armazenado na WatermelonDB collection `sync_queue`:

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `entity_type` | enum | `unit`, `holder`, `photo` |
| `operation_type` | enum | `create`, `update`, `delete` |
| `payload` | string (JSON serialized) | Dados da entidade |
| `timestamp` | number | Timestamp de criacao para ordem de processing |
| `retry_count` | number | Contagem de tentativas |
| `status` | enum | `pending`, `processing`, `failed` |

## Fluxo de Sincronizacao

### Pull (Server -> Client)

1. Chama `GET /api/sync/changes` com params `last_sync_timestamp` e `tenant_id`
2. Retorna JSON com arrays: `created_records`, `updated_records`, `deleted_records` (cada contendo full record data)
3. Itera arrays aplicando changes localmente via `database.batch` write: criando, updating e deletando records WatermelonDB preservando referential integrity (foreign keys)
4. Salva new `last_sync_timestamp` para proximo pull incremental (apenas changes since last sync), reduzindo payload e bandwidth

### Push (Client -> Server)

1. Itera `sync_queue` collection filtrando `status` = `pending`
2. Builds batch payload: array de operations, cada com `entity_type`, `entity_id`, `operation`, `payload`
3. Chama `POST /api/sync/push` com body batch array e `Authorization` header
4. Backend processa batch sequentially, validando cada operation, aplicando database, executando business rules
5. Retorna results array com `success` boolean, `server_id` (se created), `error_message` (se failed)
6. Client itera results:
   - **Successful**: marca `status` = `synced`, remove da queue, atualiza local records com server IDs
   - **Failed**: incrementa `retry_count`. Se `retry_count` < 3, mantem em queue. Senao marca `status` = `failed` requiring manual intervention

## Resolucao de Conflitos

| Estrategia | Descricao | Quando Usar |
|------------|-----------|-------------|
| **Last-Write-Wins** | Server record sempre vence, ignorando local changes | Dados nao-criticos, metadata |
| **Client-Wins** | Local record vence, server updated com local data via force push flag | Coletas de campo prioritarias |
| **Manual** | User escolhe field-by-field via `ConflictResolutionDialog`, constructing merged record combinando selected fields | Dados criticos, conflitos complexos |
| **Three-Way Merge** | Compara base version (common ancestor) com server e local versions, detectando concurrent changes, merging non-conflicting fields, prompting user apenas para conflicting fields | Edicoes parciais simultaneas |

### Deteccao de Conflitos

Conflitos sao detectados comparando `updated_at` timestamps: se server record e mais recente E local foi modificado since last sync, o record e marcado como conflict requiring resolution.

Duplicates sao detectados via unique constraints: server response **409 Conflict** indica record ja existe, oferecendo merge ou skip.

## Componentes UI

### SyncStatusIndicator

Badge UI component mostrando sync state:

| Estado | Icone/Cor | Descricao |
|--------|-----------|-----------|
| `idle` | Verde (green) | Tudo sincronizado |
| `syncing` | Amarelo (yellow), pulsating animation | Sincronizacao em andamento |
| `conflicts_pending` | Amarelo (yellow) | Conflitos aguardando resolucao |
| `error` | Vermelho (red) | Erro na sincronizacao |

### SyncSettingsScreen

Permite user configurar parametros de sync:

| Configuracao | Tipo | Descricao |
|--------------|------|-----------|
| `auto_sync` | boolean | Habilitar sync automatico |
| `wifi_only` | boolean | Sincronizar apenas em WiFi |
| `cellular_allowed` | boolean | Permitir sync via dados moveis |
| `sync_interval` | number (minutes) | Intervalo entre syncs automaticos |
| `background_sync` | boolean | Habilitar sync em background |

### ConflictResolutionDialog

Modal exibindo conflicting records: server version vs local version, com opcoes Keep Local, Keep Server, Merge Fields. Apresenta side-by-side comparison highlighting differences field-by-field.

### SyncLogScreen

Lista historical sync attempts com timestamps, records synced, failures e errors, facilitando debugging e troubleshooting de field issues.

## Validacoes Pre-Sync

| Validacao | Descricao | Acao se Invalido |
|-----------|-----------|-----------------|
| **Network Connectivity** | Verifica via `NetInfo` antes de iniciar sync | Aborta, mostra toast "Network unavailable", guarda battery evitando failed attempts |
| **Authentication Token** | Valida token via `AuthManager.getAccessToken`, refresh se necessario | Evita 401 errors midway sync |
| **Payload Integrity** | Verifica required fields present, geolocation valid, CPF format correct | Evita server rejections por invalid data |
| **Available Storage** | Checa via `Expo FileSystem` `getTotalDiskCapacityAsync`/`getFreeDiskStorageAsync` | Alerta user se < 100MB free, oferece clear cache/old photos |
| **Rate Limiting** | Max 50 records per batch | Evita timeout e backend overload, splits large queues em multiplos batches com sequential processing e progress indicator |

## Integracao API

### pullChanges

```
GET /api/sync/changes
  ?last_sync_timestamp={timestamp}
  &tenant_id={tenantId}

Response: {
  created_records: [...],
  updated_records: [...],
  deleted_records: [...]
}
```

### pushChanges

```
POST /api/sync/push
Authorization: Bearer {access_token}

Body: {
  batch: [
    { entity_type, entity_id, operation, payload },
    ...
  ]
}

Response: {
  results: [
    { success: boolean, server_id?, error_message? },
    ...
  ]
}
```

## Domain Model

### Sync Adapter

WatermelonDB `synchronize` function configurada recebendo:
- `database` instance
- `pullChanges` e `pushChanges` functions
- Migration strategy: `set migrate` indicando schema version (server deve enviar formato esperado pelo client)

### Sync Metadata

Collection `sync_metadata` (singleton record):

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `last_sync_timestamp` | number | Timestamp do ultimo sync bem-sucedido |
| `last_sync_status` | enum | Status do ultimo sync |
| `last_sync_error` | string (nullable) | Mensagem de erro do ultimo sync |

Habilita incremental sync e e resumable apos failures.

### Entity Versioning

Campo `version` (integer) incrementado a cada update, detectando stale updates e prevenindo lost updates por concurrent modifications.

### Soft Delete Pattern

Campo `deleted_at` (timestamp nullable) preserva records apos delete, permitindo sync de delete operations para downstream clients. Tombstone records sao cleaned up apos retention period.

### Conflict Tracking

Collection `conflicts`:

| Campo | Tipo | Descricao |
|-------|------|-----------|
| `entity_type` | string | Tipo da entidade em conflito |
| `entity_id` | UUID | ID da entidade |
| `local_data` | string (JSON) | Versao local dos dados |
| `server_data` | string (JSON) | Versao do servidor |
| `timestamp` | number | Quando o conflito foi detectado |

Conflitos nao resolvidos bloqueiam sync da entidade ate resolucao pelo usuario.

## Requisitos Funcionais Implementados

Implementacao dos requisitos de sincronizacao offline:

- Sincronizacao bidirecional: push local, pull server changes
- Deteccao automatica de conexao via `NetInfo` triggering sync
- Sync background via `Expo Background Fetch` com periodic attempts
- Conflict resolution strategies configuraveis (last-write-wins, manual)
- Retry logic com exponential backoff e max attempts
- Progress tracking com UI feedback de sync status
- Error handling e logging de failures para debugging

Rastreando requisitos: **RF-020**, **RF-021** (sync offline, queue, conflict resolution, garantindo field collectors produtivos com zero data loss e eventual consistency).

## Referencias

- [Field Collection](./01-field-collection.md)
- [Holder Management](./02-holder-management.md)
- [GEOAPI Offline-First Pattern](../../../GEOAPI/DOCS/PATTERNS/01-mobile-offline-first.md)
- [GEOAPI Sync Protocol Detail](../../../GEOAPI/DOCS/PATTERNS/04-sync-protocol-detail.md)
- [GEOAPI Sync Conflict Resolution](../../../GEOAPI/DOCS/PATTERNS/05-sync-conflict-resolution.md)
- [GEOAPI Sync Commands](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/APPLICATION/COMMANDS/07-sync-commands.md)
- [CENTRAL Offline Sync RF](../../../../CENTRAL/REQUIREMENTS/FUNCTIONAL/14-offline-sync/RF-183-download-inicial-de-dados.md)
