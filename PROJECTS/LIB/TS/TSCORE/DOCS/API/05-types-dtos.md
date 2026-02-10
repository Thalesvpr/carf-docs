---
type: leaf
status: review
updated: 2026-02-08
---

# Tipos DTO e Versionamento

Interfaces de response e sincronizacao exportadas pelo modulo types do tscore. DTOs de request (Create*Request, Update*Request) foram removidos do tscore e sao agora gerados automaticamente pelo @carf/geoapi-client via orval a partir do swagger.json. Consulte a [documentacao do geoapi-client](../../../GEOAPI-CLIENT/DOCS/API/README.md) para os tipos de request atualizados.

## PaginatedResponse de T

Interface generica que encapsula listas paginadas retornadas por todos os endpoints de listagem da API. O tipo parametrico T representa o tipo dos itens na colecao.

| Propriedade | Tipo TS | Descricao |
|:------------|:--------|:----------|
| items | array de T | Array de resultados da pagina atual |
| total | number | Contagem absoluta de registros que atendem os filtros |
| page | number | Pagina atual, a partir de 1 |
| limit | number | Tamanho da pagina, maximo 100 |
| hasNext | boolean | Indica se existe proxima pagina |

## ErrorResponse

Interface padrao de erro retornada pela API seguindo RFC 7807 ProblemDetails.

| Propriedade | Tipo TS | Descricao |
|:------------|:--------|:----------|
| type | string | URI do tipo de erro |
| title | string | Descricao curta do erro |
| status | number | Codigo HTTP |
| detail | string | Mensagem legivel com contexto |
| errorCode | string | Codigo maquina do erro para tratamento programatico |
| fields | array de FieldError | Erros por campo quando aplicavel (validacao) |

A interface FieldError contem field (nome do campo), message (descricao do erro) e code (codigo do erro especifico do campo).

## SyncPushRequest

Contrato para envio de operacoes locais via POST /api/sync/push. O app REURBCAD coleta mudancas pendentes do WatermelonDB e envia em batch.

| Propriedade | Tipo TS | Descricao |
|:------------|:--------|:----------|
| operations | array de SyncOperation | Array de operacoes a sincronizar |

Cada SyncOperation contem entityType (UNIT, HOLDER ou DOCUMENT), localId (ID local do WatermelonDB), operation (CREATE, UPDATE ou DELETE), payload (objeto com dados da entidade) e clientTimestamp (ISO 8601 do momento da operacao local).

## SyncPullResponse

Contrato de resposta do pull de mudancas via GET /api/sync/changes. Mudancas agrupadas por tipo de entidade, cada uma subdividida em created, updated e deleted.

| Propriedade | Tipo TS | Descricao |
|:------------|:--------|:----------|
| units | SyncEntityChanges de Unit | Mudancas em unidades |
| holders | SyncEntityChanges de Holder | Mudancas em titulares |
| communities | SyncEntityChanges de Community | Mudancas em comunidades |
| serverTimestamp | string | ISO 8601 para uso como since no proximo pull |
| hasMore | boolean | Se true, existem mais mudancas para paginar |

Cada SyncEntityChanges de T contem created (array de T registros novos), updated (array de T registros modificados) e deleted (array de string UUIDs removidos).

## GeoJsonFeature

Interface representando feature GeoJSON padrao usada em exportacoes e operacoes espaciais. Retornada pelos endpoints /api/units/geojson e /api/communities/{id}/geojson.

| Propriedade | Tipo TS | Descricao |
|:------------|:--------|:----------|
| type | "Feature" | Literal type Feature |
| geometry | GeoJsonPolygon ou GeoJsonPoint | Geometria da feature |
| properties | Record de string para unknown | Propriedades da feature |

## Tabela de Versionamento

Entidades com campo version para concorrencia otimista e sincronizacao offline via WatermelonDB. O campo e incrementado a cada update pelo servidor. Clients enviam version no PATCH e o servidor retorna ConflictError 409 se a versao divergir.

| Entidade | Campo version | Motivo |
|:---------|:-------------|:-------|
| Unit | sim | Sync mobile, edicao concorrente em campo |
| Holder | sim | Sync mobile, dados coletados offline |
| Community | nao | Gerenciada apenas pelo backend, sem version na tabela |
| Block | nao | Sem campo version no schema |
| Plot | nao | Sem campo version no schema |
| Building | nao | Sem campo version no schema |
| Document | nao | Sem campo version no schema |
