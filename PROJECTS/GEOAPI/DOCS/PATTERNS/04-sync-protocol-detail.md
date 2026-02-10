---
type: leaf
status: review
updated: 2026-02-08
---

# Sync Protocol Detail

Especificacao detalhada do protocolo de sincronizacao entre o app mobile REURBCAD (WatermelonDB) e a GEOAPI (PostgreSQL). O protocolo implementa delta sync bidirecional com push-then-pull, deteccao de conflitos por versao e resolucao configuravel por campo.

## Visao Geral do Fluxo

O ciclo de sync segue a ordem: (1) push de operacoes locais pendentes, (2) pull de mudancas do servidor, (3) resolucao de conflitos se necessario. Essa ordem garante que o servidor tenha os dados mais recentes do cliente antes de enviar suas mudancas, minimizando conflitos.

## Push Request

O push envia operacoes locais pendentes ao servidor via POST /api/sync/push. Cada request contem um batch de operacoes identificado por batchId unico para idempotencia.

**Endpoint:** `POST /api/sync/push`
**Autenticacao:** Bearer token JWT (roles: FIELD_CADASTRATOR, FIELD_COORDINATOR)
**Content-Type:** application/json

**Payload:**

```json
{
  "clientId": "device-uuid-abc123",
  "batchId": "batch-uuid-def456",
  "operations": [
    {
      "localId": "local-uuid-789",
      "entityType": "unit",
      "operation": "CREATE",
      "payload": {
        "code": "UNI-2024-00001",
        "status": "DRAFT",
        "area": 150.5,
        "geometry": { "type": "Polygon", "coordinates": [[[-43.17, -22.90], [-43.16, -22.90], [-43.16, -22.89], [-43.17, -22.89], [-43.17, -22.90]]] },
        "observation": "Lote na esquina",
        "custom_data": {}
      },
      "clientTimestamp": "2024-03-15T14:30:00Z",
      "baseVersion": null
    },
    {
      "localId": "local-uuid-790",
      "entityType": "holder",
      "operation": "UPDATE",
      "payload": {
        "name": "Maria da Silva Santos",
        "phone": "(21) 99999-1234"
      },
      "clientTimestamp": "2024-03-15T14:31:00Z",
      "baseVersion": 2
    },
    {
      "localId": "local-uuid-791",
      "entityType": "document",
      "operation": "CREATE",
      "payload": {
        "entity_id": "unit-uuid-abc",
        "entity_type": "UNIT",
        "file_key": "photos/2024/03/photo-001.jpg",
        "file_name": "fachada-lote-001.jpg",
        "content_type": "image/jpeg",
        "size_bytes": 2048576
      },
      "clientTimestamp": "2024-03-15T14:32:00Z",
      "baseVersion": null
    }
  ]
}
```

**Campos do Push Request:**

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|------------|-----------|
| clientId | UUID | Sim | Identificador unico do dispositivo (gerado na primeira execucao do app) |
| batchId | UUID | Sim | Identificador unico do batch para idempotencia |
| operations | Array | Sim | Lista de operacoes a processar |
| operations[].localId | UUID | Sim | ID local da operacao (gerado pelo WatermelonDB) |
| operations[].entityType | String | Sim | Tipo da entidade: unit, holder, unit_holder, document, community |
| operations[].operation | String | Sim | Tipo de operacao: CREATE, UPDATE, DELETE |
| operations[].payload | Object | Sim | Dados da entidade (campos sincronizaveis apenas) |
| operations[].clientTimestamp | DateTime | Sim | Timestamp da operacao no dispositivo (ISO 8601 UTC) |
| operations[].baseVersion | Integer/null | Condicional | Versao do registro no momento da leitura pelo cliente. Null para CREATE |

## Push Response

O servidor processa operacoes sequencialmente e retorna status individual por operacao.

**Response (200 OK) - Sucesso total:**

```json
{
  "batchId": "batch-uuid-def456",
  "serverTimestamp": "2024-03-15T14:30:05Z",
  "results": [
    {
      "localId": "local-uuid-789",
      "serverId": "server-uuid-abc",
      "status": "ACCEPTED",
      "serverVersion": 1,
      "serverTimestamp": "2024-03-15T14:30:05Z"
    },
    {
      "localId": "local-uuid-790",
      "serverId": "holder-uuid-existing",
      "status": "ACCEPTED",
      "serverVersion": 3,
      "serverTimestamp": "2024-03-15T14:30:05Z"
    },
    {
      "localId": "local-uuid-791",
      "serverId": "doc-uuid-new",
      "status": "ACCEPTED",
      "serverVersion": 1,
      "serverTimestamp": "2024-03-15T14:30:06Z"
    }
  ],
  "conflicts": []
}
```

**Response (200 OK) - Com conflitos:**

```json
{
  "batchId": "batch-uuid-def456",
  "serverTimestamp": "2024-03-15T14:30:05Z",
  "results": [
    {
      "localId": "local-uuid-789",
      "serverId": "server-uuid-abc",
      "status": "ACCEPTED",
      "serverVersion": 1,
      "serverTimestamp": "2024-03-15T14:30:05Z"
    }
  ],
  "conflicts": [
    {
      "localId": "local-uuid-790",
      "serverId": "holder-uuid-existing",
      "status": "CONFLICT",
      "conflictType": "VERSION_MISMATCH",
      "serverVersion": 5,
      "clientBaseVersion": 2,
      "divergentFields": [
        {
          "field": "name",
          "serverValue": "Maria da Silva",
          "clientValue": "Maria da Silva Santos",
          "strategy": "CLIENT_WINS",
          "autoResolved": true
        },
        {
          "field": "cpf",
          "serverValue": "123.456.789-00",
          "clientValue": "123.456.789-00",
          "strategy": "SERVER_WINS",
          "autoResolved": true
        }
      ],
      "resolvedPayload": {
        "name": "Maria da Silva Santos",
        "cpf": "123.456.789-00",
        "phone": "(21) 99999-1234"
      },
      "autoResolvedCompletely": true
    }
  ]
}
```

**Response (200 OK) - Conflito com resolucao manual necessaria:**

```json
{
  "batchId": "batch-uuid-def456",
  "serverTimestamp": "2024-03-15T14:30:05Z",
  "results": [],
  "conflicts": [
    {
      "localId": "local-uuid-792",
      "serverId": "unit-uuid-xyz",
      "status": "CONFLICT",
      "conflictType": "VERSION_MISMATCH",
      "serverVersion": 3,
      "clientBaseVersion": 1,
      "divergentFields": [
        {
          "field": "observation",
          "serverValue": "Alterado pelo analista",
          "clientValue": "Alterado em campo",
          "strategy": "CLIENT_WINS",
          "autoResolved": true
        },
        {
          "field": "geometry",
          "serverValue": { "type": "Polygon", "coordinates": [[[-43.17, -22.90], [-43.16, -22.90], [-43.16, -22.89], [-43.17, -22.89], [-43.17, -22.90]]] },
          "clientValue": { "type": "Polygon", "coordinates": [[[-43.175, -22.905], [-43.165, -22.905], [-43.165, -22.895], [-43.175, -22.895], [-43.175, -22.905]]] },
          "strategy": "MANUAL",
          "autoResolved": false
        }
      ],
      "autoResolvedCompletely": false
    }
  ]
}
```

## Pull Request

O pull solicita mudancas do servidor desde o ultimo sync bem-sucedido.

**Endpoint:** `GET /api/sync/changes`
**Autenticacao:** Bearer token JWT (roles: FIELD_CADASTRATOR, FIELD_COORDINATOR)

**Query Parameters:**

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|------------|-----------|
| since | DateTime | Sim | Timestamp ISO 8601 UTC do ultimo sync bem-sucedido |
| entities | String | Nao | Lista separada por virgula de entidades a sincronizar. Default: todas |
| limit | Integer | Nao | Maximo de registros por entidade. Default: 1000 |

**Exemplo:** `GET /api/sync/changes?since=2024-03-15T14:00:00Z&entities=units,holders,documents`

## Pull Response

**Response (200 OK):**

```json
{
  "timestamp": "2024-03-15T14:35:00Z",
  "changes": {
    "units": {
      "created": [
        {
          "id": "unit-uuid-new",
          "code": "UNI-2024-00050",
          "status": "PENDING",
          "area": 200.0,
          "geometry": { "type": "Polygon", "coordinates": [[]] },
          "observation": "Unidade criada por analista",
          "custom_data": {},
          "version": 1
        }
      ],
      "updated": [
        {
          "id": "unit-uuid-existing",
          "code": "UNI-2024-00001",
          "status": "APPROVED",
          "area": 150.5,
          "geometry": { "type": "Polygon", "coordinates": [[]] },
          "observation": "Lote na esquina - aprovado",
          "custom_data": {},
          "version": 3
        }
      ],
      "deleted": ["unit-uuid-removed-1", "unit-uuid-removed-2"]
    },
    "holders": {
      "created": [],
      "updated": [
        {
          "id": "holder-uuid-abc",
          "name": "Joao da Silva",
          "cpf": "123.456.789-00",
          "email": "joao@email.com",
          "phone": "(21) 98765-4321",
          "holder_type": "INDIVIDUAL",
          "version": 4
        }
      ],
      "deleted": []
    },
    "documents": {
      "created": [
        {
          "id": "doc-uuid-new",
          "entity_id": "unit-uuid-existing",
          "entity_type": "UNIT",
          "file_key": "documents/2024/03/certidao-001.pdf",
          "file_name": "certidao-nascimento.pdf",
          "content_type": "application/pdf",
          "size_bytes": 524288,
          "version": 1
        }
      ],
      "updated": [],
      "deleted": []
    }
  },
  "hasMore": false
}
```

O campo `timestamp` deve ser armazenado pelo cliente como referencia para o proximo pull. O campo `hasMore` indica se ha mais registros alem do limite; se true, o cliente deve fazer outro pull com o timestamp retornado.

## Resolucao de Conflitos Manual

Quando o push retorna conflitos com `autoResolvedCompletely: false`, o cliente deve apresentar a interface de resolucao e submeter as escolhas do usuario.

**Endpoint:** `POST /api/sync/resolve-conflict`
**Autenticacao:** Bearer token JWT

**Payload:**

```json
{
  "conflictId": "unit-uuid-xyz",
  "resolutions": [
    {
      "field": "geometry",
      "choice": "CLIENT",
      "value": { "type": "Polygon", "coordinates": [[]] }
    }
  ],
  "clientTimestamp": "2024-03-15T15:00:00Z"
}
```

Os valores possiveis para `choice` sao: `SERVER` (manter valor do servidor), `CLIENT` (manter valor do cliente) e `CUSTOM` (valor editado manualmente pelo usuario, informado no campo `value`).

## Deduplicacao

O servidor utiliza a combinacao `localId + clientTimestamp` como chave de idempotencia. Se o cliente reenvia um batch ja processado (por exemplo, apos timeout sem receber resposta), o servidor detecta a duplicata e retorna o resultado anterior sem reprocessar.

Hashes de operacoes processadas sao armazenados no Redis com TTL de 7 dias. Apos esse periodo, um reenvio seria tratado como operacao nova, mas a deteccao de conflito por version impede duplicacao de dados.

## Particao de Rede e Atomicidade

Cada operacao dentro de um batch e atomica por entidade, processada em transacao individual. Se um batch de 5 operacoes falha na operacao 3:

| Operacao | Status | Resultado |
|----------|--------|-----------|
| 1 | ACCEPTED | Commitada no banco |
| 2 | ACCEPTED | Commitada no banco |
| 3 | ERROR | Rollback desta operacao, erro retornado |
| 4 | NOT_PROCESSED | Nao executada |
| 5 | NOT_PROCESSED | Nao executada |

O cliente recebe a resposta parcial e deve reenviar a partir da operacao 3. As operacoes 1 e 2 nao serao reprocessadas gracas a deduplicacao. A operacao 3 deve ter seus dados corrigidos (se erro de validacao) ou simplesmente reenviada (se erro transiente).

## Limites de Batch

| Parametro | Valor | Justificativa |
|-----------|-------|---------------|
| Max operacoes por push | 50 | Evitar timeouts em conexoes lentas (3G/4G) |
| Max payload por push | 5 MB | Limite pratico para upload mobile |
| Max registros por pull | 1000 por entidade | Evitar respostas muito grandes para memoria do dispositivo |
| Timeout do request | 60 segundos | Tolerancia para conexoes instáveis |

Para batches maiores que 50 operacoes, o cliente divide automaticamente em multiplos pushes sequenciais, aguardando confirmacao de cada batch antes de enviar o proximo. O batchId e unico por push, permitindo rastreamento individual.

## Upload de Arquivos

Documentos com arquivos binarios (fotos, PDFs) seguem fluxo separado do sync de metadados:

1. O push do sync envia apenas os metadados do documento (file_key, file_name, content_type, size_bytes)
2. O servidor retorna status ACCEPTED com serverId
3. O cliente inicia upload do arquivo binario via `POST /api/documents/{serverId}/upload` (multipart/form-data)
4. O servidor valida content_type, tamanho e armazena no MinIO/S3
5. Enquanto o upload nao completa, o documento fica com status PENDING_UPLOAD no servidor

Esse desacoplamento permite que o sync de metadados seja rapido mesmo com muitas fotos pendentes, e os uploads podem acontecer em background com retry independente.

## Diagrama de Sequencia

```
Cliente (REURBCAD)          Servidor (GEOAPI)          PostgreSQL
       |                          |                          |
       |--- POST /sync/push ---->|                          |
       |    [operations batch]    |                          |
       |                          |--- BEGIN TX ------------->|
       |                          |--- SET LOCAL tenant ---->|
       |                          |--- process op 1 -------->|
       |                          |--- COMMIT TX ----------->|
       |                          |--- BEGIN TX ------------->|
       |                          |--- process op 2 -------->|
       |                          |--- COMMIT TX ----------->|
       |                          |                          |
       |<-- 200 {results} -------|                          |
       |                          |                          |
       |--- GET /sync/changes -->|                          |
       |    ?since=timestamp      |                          |
       |                          |--- SELECT changes ------>|
       |                          |    WHERE updated > since  |
       |                          |<-- resultset ------------|
       |<-- 200 {changes} -------|                          |
       |                          |                          |
       |--- [apply changes       |                          |
       |     to WatermelonDB]    |                          |
       |                          |                          |
```