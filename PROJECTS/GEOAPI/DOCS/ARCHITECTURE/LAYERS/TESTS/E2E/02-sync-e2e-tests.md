---
type: leaf
status: review
updated: 2026-02-08
---

# Sync E2E Tests

Este documento detalha os testes end-to-end do protocolo de sincronizacao entre o aplicativo mobile (REURBCAD) e a API (GEOAPI). Os testes simulam o ciclo completo de push/pull/conflito usando WebApplicationFactory com um simulador de cliente mobile.

## Infraestrutura de Teste

### Setup

Os testes de sync reutilizam a `ApiFixture` descrita em `01-api-e2e-tests.md`, com adicoes especificas:

- **WebApplicationFactory** - hospeda a API in-process com PostgreSQL+PostGIS e Redis via Testcontainers
- **MobileClientSimulator** - classe helper que encapsula o HttpClient e simula o comportamento do cliente mobile (geracao de localId, timestamps, versionamento)
- **JWT com role CADASTRATOR** - token gerado pelo helper com claims de agente de campo
- **SyncSeedHelper** - classe que cria dados pre-existentes (community, units, holders) para cenarios que dependem de dados ja sincronizados

### MobileClientSimulator

O simulador possui os seguintes metodos:

- `CreateLocalUnit(overrides)` - cria uma representacao local de unidade com localId (UUID v4 gerado no cliente), clientTimestamp e dados gerados via Bogus
- `CreateLocalHolder(overrides)` - cria representacao local de holder
- `PushBatch(operations)` - envia POST /api/sync/push com array de operacoes
- `Pull(sinceTimestamp)` - envia GET /api/sync/pull?since={timestamp} e retorna o delta
- `SetOffline()` - ativa modo offline (operacoes sao enfileiradas localmente)
- `SetOnline()` - desativa modo offline
- `FlushQueue()` - envia todas as operacoes enfileiradas em um unico batch

### Formato de Operacao de Push

Cada operacao no batch de push contem:

| Campo | Tipo | Descricao |
|-------|------|-----------|
| localId | UUID | Identificador gerado no cliente (UUID v4) |
| entityType | string | Tipo da entidade (Unit, Holder, Document) |
| operation | string | Tipo de operacao (Create, Update, Delete) |
| clientTimestamp | ISO 8601 | Timestamp da operacao no cliente |
| version | int | Versao local da entidade (para deteccao de conflito) |
| data | object | Payload da entidade (campos variam por entityType) |

### Formato de Resposta de Pull

| Campo | Tipo | Descricao |
|-------|------|-----------|
| changes | array | Lista de entidades modificadas desde o timestamp |
| deletions | array | Lista de IDs de entidades excluidas |
| serverTimestamp | ISO 8601 | Timestamp do servidor para usar no proximo pull |
| hasMore | bool | Indica se existem mais mudancas (paginacao) |

## Testes de Push

### Criar unidade offline e sincronizar

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Push create valido | Community existente no servidor | PushBatch com 1 operacao Create Unit | HTTP 200, resposta contem serverTimestamp, GET /api/units retorna a unidade com serverId mapeado para o localId |
| Push create com holder | Community e holder existentes | PushBatch com Create Unit + dados de holder | HTTP 200, unidade criada com holder vinculado |
| Push create com geometria | Community existente | PushBatch com Create Unit incluindo GeoJSON polygon | HTTP 200, geometria persistida, ST_IsValid retorna verdadeiro no banco |

### Atualizar unidade offline e sincronizar

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Push update valido | Unit existente (Draft, version=1) | PushBatch com 1 operacao Update Unit (version=1, novos dados) | HTTP 200, unit atualizada, version incrementada para 2 |
| Push update de endereco | Unit existente (Draft) | PushBatch com Update contendo novo endereco | HTTP 200, endereco atualizado, FullAddress recalculado |
| Push update de geometria | Unit existente (Draft) | PushBatch com Update contendo novo GeoJSON | HTTP 200, geometria atualizada, sem sobreposicao |

### Push com validacoes

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Push create com geometria invalida | Community existente | PushBatch com poligono auto-intersectante | HTTP 200 (batch parcial), operacao retorna erro INVALID_GEOMETRY no campo errors |
| Push create com CPF invalido | Community existente | PushBatch com holder CPF invalido | Operacao retorna erro INVALID_CPF |
| Push create com sobreposicao | Unit existente com mesma geometria | PushBatch com poligono sobreposto | Operacao retorna erro GEOMETRY_OVERLAP |

## Testes de Pull

### Pull de mudancas do servidor

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Pull apos modificacao no servidor | Unit criada no T0, modificada no T1 | Pull since=T0 | changes contem a unit modificada, version = 2 |
| Pull sem mudancas | Nenhuma modificacao apos T0 | Pull since=T0 | changes vazio, serverTimestamp >= T0 |
| Pull retorna apenas delta | 3 units criadas em T0, 1 modificada em T1 | Pull since=T0+1 | changes contem apenas 1 unit (a modificada) |
| Pull retorna delecoes | Unit existente, deletada no T1 | Pull since=T0 | deletions contem o ID da unit deletada |
| Pull respeita tenant | Units no TenantA e TenantB | Pull since=T0 (como TenantA) | changes contem apenas units do TenantA |
| Pull paginado | 200 units modificadas, pagina de 50 | Pull since=T0 | Primeira resposta com 50 changes e hasMore=true, cursor para proxima pagina |

### Pull com relacoes

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Pull inclui holders da unit | Unit com 2 holders, holder modificado em T1 | Pull since=T0 | changes inclui a unit E os holders aninhados |
| Pull inclui documentos | Unit com documento adicionado em T1 | Pull since=T0 | changes inclui referencia ao documento |

## Testes de Conflito

### Deteccao de conflito por version

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Conflito detectado | Unit version=1 no servidor, cliente envia update com version=1, mas servidor ja atualizou para version=2 | PushBatch com Update (version=1) | Resposta com status CONFLICT para essa operacao |
| Sem conflito (versoes iguais) | Unit version=1 no servidor, cliente envia update com version=1 | PushBatch com Update (version=1) | HTTP 200, operacao bem-sucedida |
| Conflito com diff por campo | Unit modificada no servidor (endereco) e no cliente (geometria) | PushBatch com Update | Resposta CONFLICT com field-level diff indicando campos divergentes |

### Formato de resposta de conflito

A resposta de conflito inclui diff por campo para permitir resolucao manual:

| Campo da Resposta | Tipo | Descricao |
|-------------------|------|-----------|
| operationIndex | int | Indice da operacao no batch |
| status | string | "CONFLICT" |
| localId | UUID | localId da operacao |
| serverVersion | int | Versao atual no servidor |
| clientVersion | int | Versao enviada pelo cliente |
| fieldDiffs | array | Lista de campos divergentes |
| fieldDiffs[].field | string | Nome do campo |
| fieldDiffs[].serverValue | any | Valor no servidor |
| fieldDiffs[].clientValue | any | Valor enviado pelo cliente |

### Cenarios de diff por campo

| Cenario | Campo Modificado (servidor) | Campo Modificado (cliente) | fieldDiffs |
|---------|---------------------------|---------------------------|------------|
| Campos diferentes | address | geometry | 2 diffs: address e geometry |
| Mesmo campo | address | address | 1 diff: address com serverValue e clientValue |
| Multiplos campos | address, status | geometry, holders | 4 diffs |

## Testes de Idempotencia

### Deduplicacao por localId + clientTimestamp

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Push duplicado ignorado | Primeira execucao do batch bem-sucedida | Segundo PushBatch identico (mesmo localId + clientTimestamp) | HTTP 200, nenhuma duplicata criada, resposta indica "already_processed" |
| Push com localId repetido mas timestamp diferente | Operacao anterior processada | PushBatch com mesmo localId mas clientTimestamp diferente | Processado como nova operacao (update) |
| Push parcialmente duplicado | Batch de 3 operacoes, primeira ja processada | PushBatch com as 3 operacoes | Primeira ignorada, segunda e terceira processadas |

### Verificacao de deduplicacao

Apos cada teste de idempotencia, o teste verifica:

- Contagem de registros no banco (nao houve duplicata)
- Log de operacoes de sync registra a deduplicacao
- Resposta do batch indica quais operacoes foram ignoradas vs processadas

## Testes de Simulacao Offline

### Fila de operacoes offline

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| 10 operacoes enfileiradas | MobileClientSimulator.SetOffline() | Criar 10 units localmente, FlushQueue() | PushBatch com 10 operacoes, todas processadas sequencialmente, 10 units persistidas |
| Ordem preservada | SetOffline() | Criar unit, vincular holder, fazer upload documento | Operacoes processadas na ordem: Create Unit → Link Holder → Upload Document |
| Mix de operacoes | SetOffline() | 3 creates, 2 updates, 1 delete | Batch com 6 operacoes, cada uma com operation type correto |
| Fila vazia | SetOffline(), SetOnline() sem operacoes | FlushQueue() | Nenhuma requisicao HTTP enviada |

### Processamento sequencial

O servidor processa as operacoes do batch sequencialmente (nao em paralelo), respeitando dependencias implicitas. Por exemplo, nao e possivel vincular um holder a uma unit que ainda nao foi criada no batch.

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Dependencia no batch | Op1: Create Unit (localId=A), Op2: Link Holder (unitLocalId=A) | PushBatch | Ambas processadas com sucesso, holder vinculado a unit recem-criada |
| Dependencia invertida | Op1: Link Holder (unitLocalId=A), Op2: Create Unit (localId=A) | PushBatch | Op1 falha (unit nao existe), Op2 sucesso |

## Testes de Particao de Rede

### Falha parcial do batch

| Cenario | Setup | Acao | Verificacao |
|---------|-------|------|-------------|
| Falha na operacao 3 de 5 | 5 operacoes validas, exceto op3 (geometria invalida) | PushBatch | Ops 1-2 commitadas, op3 reporta erro, ops 4-5 commitadas. Cada operacao e atomica individualmente |
| Timeout no servidor | Batch com 5 operacoes, simulate timeout apos op2 | PushBatch | HTTP 504/timeout, cliente nao sabe quais foram processadas |
| Retry apos timeout | Apos timeout, reenviar o mesmo batch | PushBatch | Ops 1-2 deduplicadas (ja processadas), ops 3-5 processadas |
| Transacao por operacao | Batch com 5 ops, op3 causa erro de banco | PushBatch | Ops 1-2 commitadas (transacoes individuais), op3 falha, ops 4-5 commitadas |

### Atomicidade por Operacao

Cada operacao do batch e executada em sua propria transacao de banco. Se uma operacao falhar, as anteriores (ja commitadas) nao sao revertidas, e as posteriores continuam sendo processadas.

| Cenario | Operacoes | Resultado |
|---------|-----------|-----------|
| Todas OK | Op1 OK, Op2 OK, Op3 OK | Todas commitadas |
| Falha no meio | Op1 OK, Op2 FALHA, Op3 OK | Op1 commitada, Op2 rollback, Op3 commitada |
| Primeira falha | Op1 FALHA, Op2 OK, Op3 OK | Op1 rollback, Op2 commitada, Op3 commitada |
| Ultima falha | Op1 OK, Op2 OK, Op3 FALHA | Op1 e Op2 commitadas, Op3 rollback |

## Testes de Performance de Sync

| Cenario | Volume | Threshold |
|---------|--------|-----------|
| Push batch grande | 50 operacoes Create Unit | Tempo total < 10 segundos |
| Pull delta grande | 100 units modificadas | Tempo de resposta < 5 segundos |
| Pull com geometrias | 50 units com poligonos complexos (20+ vertices) | Tempo de resposta < 8 segundos |

## Tabela Resumo

| Categoria | Total de Cenarios | Foco |
|-----------|-------------------|------|
| Push create | 3 | Criacao de entidades via sync |
| Push update | 3 | Atualizacao de entidades via sync |
| Push validacao | 3 | Rejeicao de dados invalidos |
| Pull delta | 6 | Recuperacao de mudancas incrementais |
| Pull relacoes | 2 | Inclusao de entidades relacionadas |
| Conflito | 3 | Deteccao e resolucao de conflitos |
| Conflito diff | 3 | Diff por campo |
| Idempotencia | 3 | Deduplicacao de operacoes |
| Offline queue | 4 | Fila de operacoes offline |
| Processamento sequencial | 2 | Dependencias no batch |
| Particao de rede | 4 | Falha parcial e retry |
| Atomicidade | 4 | Transacao por operacao |
| Performance | 3 | Thresholds de tempo |
| **Total** | **43** | |

## Referencias Cruzadas

- Protocolo de sync: `CENTRAL/ARCHITECTURE/INTEGRATION/02-api-communication.md`
- Entidades com version para sync: `DOMAIN/ENTITIES/` (coluna version em units, holders, communities)
- Value object SyncStatus: `DOMAIN/VALUE-OBJECTS/STATUS/09-sync-status.md`
- Sync commands: `APPLICATION/COMMANDS/07-sync-commands.md`
- Sync controller: `PRESENTATION/CONTROLLERS/07-sync-controller.md`
- Testes E2E da API: `TESTS/E2E/01-api-e2e-tests.md`
- Padrao offline-first: `PATTERNS/01-mobile-offline-first.md`
