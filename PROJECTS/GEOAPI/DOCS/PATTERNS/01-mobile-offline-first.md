---
type: leaf
status: review
updated: 2026-02-08
---

# Mobile Offline-First

O padrao offline-first do REURBCAD garante que agentes de campo possam cadastrar unidades, editar titulares e capturar fotos sem conectividade, sincronizando dados quando a conexao estiver disponivel.

## Armazenamento Local

O app utiliza WatermelonDB como wrapper sobre SQLite para armazenamento local reativo. O schema local e um subconjunto do schema PostgreSQL do servidor, contendo tabelas units, holders, documents e communities com os mesmos campos essenciais. Queries observaveis via useObservable reagem automaticamente a mudancas locais, atualizando a UI sem necessidade de refresh manual. Migrations versionadas evoluem o schema local sem perder dados do usuario.

## Protocolo de Sincronizacao

O protocolo delta sync usa timestamp como watermark. O pull solicita mudancas via GET /api/sync/changes?since=timestamp, recebendo apenas registros modificados apos o ultimo sync bem-sucedido em colecoes separadas (created, updated, deleted) para units, holders e communities. O push envia operacoes locais via POST /api/sync/push em batch, cada operacao contendo entityType, localId, operation (CREATE, UPDATE, DELETE), payload e clientTimestamp. O servidor processa sequencialmente e retorna status individual por operacao.

## Resolucao de Conflitos

A deteccao de conflitos compara campo a campo usando version do registro. Campos criticos como status de unidade e dados de aprovacao seguem server-wins. Campos de rascunho como observacoes e fotos seguem client-wins. Geometrias conflitantes requerem resolucao manual com diff visual lado a lado. O app exibe interface de resolucao permitindo escolha campo a campo com serverVersion e clientVersion dos campos divergentes.

## Fila de Sincronizacao

Operacoes pendentes sao persistidas em tabela sync_queue local marcadas como needs_sync. O processamento segue ordem FIFO quando conectividade retorna, com exponential backoff para falhas transitorias e retry manual para erros de validacao. A UI exibe contador de alteracoes pendentes e badge "Modo Offline" via NetInfo listener.

## Tokens Offline

Tokens JWT do Keycloak sao configurados com refresh token de 30 dias para permitir operacao prolongada sem conectividade. O app armazena o refresh token de forma segura e tenta renovacao silenciosa quando detecta conexao.

## Schema WatermelonDB vs PostgreSQL

O schema local do WatermelonDB e um subconjunto do schema PostgreSQL do servidor. A tabela abaixo detalha o mapeamento entre tabelas, indicando quais campos sao sincronizados, quais existem apenas no servidor e quais existem apenas no mobile.

| Tabela WDB | Tabela PostgreSQL | Campos Sincronizados | Campos Apenas Server | Campos Apenas Mobile |
|------------|-------------------|---------------------|---------------------|---------------------|
| units | units | id, code, status, area, geometry, observation, custom_data, version | tenant_id, created_by, approved_by, approved_at, deleted_at | _status, _changed, needs_sync |
| holders | holders | id, name, cpf, email, phone, holder_type, version | tenant_id, deleted_at | _status, _changed |
| unit_holders | unit_holders | id, unit_id, holder_id, ownership_percentage, is_primary, version | tenant_id | _status, _changed |
| documents | documents | id, entity_id, entity_type, file_key, file_name, content_type, size_bytes, version | tenant_id, uploaded_by | _status, _changed, local_uri |
| communities | communities | id, name, type, boundary, version | tenant_id, created_by | _status, _changed |

Os campos `_status` e `_changed` sao metadados internos do WatermelonDB para rastreamento de estado de sincronizacao. O campo `_status` indica se o registro foi criado (`created`), atualizado (`updated`) ou excluido (`deleted`) localmente. O campo `_changed` lista quais colunas foram alteradas desde o ultimo sync. O campo `needs_sync` em units e um flag booleano auxiliar que indica operacoes pendentes de envio. O campo `local_uri` em documents armazena o caminho local do arquivo no dispositivo para acesso offline.

Campos do servidor como `tenant_id`, `created_by` e `deleted_at` nao sao enviados ao mobile pois representam metadados de infraestrutura, auditoria ou soft-delete controlados exclusivamente pelo backend. O campo `version` e essencial para deteccao de conflitos e esta presente em ambos os lados.

## Algoritmo de Conflict Resolution

O algoritmo de resolucao de conflitos opera campo a campo, comparando a versao base que o cliente conhecia com a versao atual do servidor. Quando nao ha divergencia de versao, a operacao e aceita diretamente. Quando ha divergencia, cada campo e analisado individualmente conforme sua estrategia configurada.

```
function resolveConflict(serverRecord, clientRecord):
    if serverRecord.version == clientRecord.baseVersion:
        return ACCEPT_CLIENT  // nenhuma alteracao no servidor desde a leitura do cliente

    conflicts = []
    for each field in SYNCABLE_FIELDS:
        serverChanged = serverRecord[field] != baseRecord[field]
        clientChanged = clientRecord[field] != baseRecord[field]

        if serverChanged AND clientChanged:
            strategy = FIELD_STRATEGIES[field]
            if strategy == SERVER_WINS:
                merged[field] = serverRecord[field]
            elif strategy == CLIENT_WINS:
                merged[field] = clientRecord[field]
            else:
                conflicts.append({field, serverValue, clientValue})
        elif serverChanged:
            merged[field] = serverRecord[field]
        elif clientChanged:
            merged[field] = clientRecord[field]

    if conflicts.length > 0:
        return MANUAL_RESOLUTION(conflicts)
    return ACCEPT_MERGED(merged)
```

O `baseRecord` e reconstruido a partir da versao que o cliente possuia antes de suas alteracoes locais (armazenada no `baseVersion`). O `FIELD_STRATEGIES` e um mapa configuravel que define a estrategia de resolucao por campo (ver `PATTERNS/05-sync-conflict-resolution.md` para tabela completa). Quando todos os conflitos sao auto-resolvidos (SERVER_WINS ou CLIENT_WINS), o merge acontece sem intervencao do usuario. Apenas campos com estrategia MANUAL requerem interacao.

## Retry com Exponential Backoff

Quando uma operacao de sync falha por erro transiente (timeout, 503, erro de rede), o app aplica retry com exponential backoff para evitar sobrecarga no servidor.

**Formula:** `delay = min(BASE_DELAY x 2^attempt, MAX_DELAY) + jitter`

Onde `BASE_DELAY = 30s`, `MAX_DELAY = 300s (5min)` e `jitter = random(0, delay x 0.1)`.

O jitter (variacao aleatoria de ate 10% do delay) previne o efeito thundering herd, onde multiplos dispositivos tentam sincronizar simultaneamente apos uma queda de servidor.

| Tentativa | Delay Base | Delay Acumulado |
|-----------|-----------|----------------|
| 1 | 30s | 30s |
| 2 | 60s | 1.5min |
| 3 | 120s | 3.5min |
| 4 | 240s | 7.5min |
| 5 | 300s (cap) | 12.5min |
| 6+ | 300s (cap) | +5min cada |

Apos 10 tentativas falhas consecutivas, a operacao e marcada como `FAILED` na sync_queue local e requer retry manual pelo usuario. O app exibe notificacao informando quais operacoes falharam e permite re-tentativa individual ou em lote. Erros de validacao (400 Bad Request) nao sao retentados automaticamente pois requerem correcao dos dados pelo usuario.
