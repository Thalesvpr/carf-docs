---
type: leaf
status: review
updated: 2026-02-21
---

# Orthofotos API - Gerenciamento de Ortofotos

A Orthofotos API fornece operacoes para upload, processamento assincrono e consulta de imagens ortorretificadas usadas como base cartografica para demarcacao de unidades no mapa. Acessada via propriedade orthofotos da instancia GeoApiClient. Tipo Orthophoto importado de @carf/tscore/types conforme [02-types-entities](../../TSCORE/DOCS/API/02-types-entities.md). Endpoints conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| POST | /api/orthofotos/upload | Upload de ortofoto GeoTIFF | 202 Accepted | 413 FILE_TOO_LARGE, 415 UNSUPPORTED_FORMAT | analyst+ |
| GET | /api/orthofotos/{id} | Obter metadados | 200 | 404 | todos autenticados |
| GET | /api/orthofotos | Listar ortofotos do tenant | 200 | - | todos autenticados |
| GET | /api/orthofotos/jobs/{jobId} | Status do processamento | 200 | 404 | analyst+ |

## upload (POST /api/orthofotos/upload)

Faz upload de ortofoto para processamento assincrono via Hangfire. Aceita multipart/form-data com campo file contendo arquivo GeoTIFF (tipo aceito: image/tiff, tamanho maximo 500MB), communityId como UUID opcional e captureDate como string ISO 8601 opcional.

Response retorna HTTP 202 Accepted (processamento assincrono) com body:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| ortofotoId | string | UUID do registro criado para a ortofoto |
| jobId | string | UUID do job Hangfire para acompanhamento |

O processamento gera versao JPEG otimizada para web. O client deve usar o jobId para consultar o progresso via getJobStatus.

## list (GET /api/orthofotos)

Lista ortofotos do tenant com paginacao padrao. Aceita query params page, limit e opcionalmente communityId e processingStatus para filtrar. Retorna PaginatedResponse de Orthophoto. Acessivel por todos os usuarios autenticados.

## getById (GET /api/orthofotos/{id})

Busca ortofoto por ID. Aceita id string, retorna Promise de Orthophoto com todos os campos incluindo boundsGeojson quando processamento concluido. Lanca NotFoundError 404 se nao existir.

## getJobStatus (GET /api/orthofotos/jobs/{jobId})

Consulta status de processamento assincrono. Aceita jobId string, retorna:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| status | string | PENDING, PROCESSING, COMPLETED ou FAILED |
| progress | number | Percentual estimado de progresso (0 a 100) |
| error | string ou null | Mensagem de erro quando status FAILED |
| ortofotoId | string | UUID da ortofoto para referencia cruzada |

O client deve fazer polling periodico (recomendado a cada 5 segundos) enquanto status for PENDING ou PROCESSING. Quando COMPLETED, o campo optimizedPath da Orthophoto estara preenchido. Restrito a roles analyst ou superior.
