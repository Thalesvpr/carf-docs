---
type: leaf
status: review
updated: 2026-02-08
---

# Orthofotos API - Gerenciamento de Ortofotos

A Orthofotos API fornece operacoes para upload, processamento assincrono e consulta de imagens ortorretificadas usadas como base cartografica para demarcacao de unidades no mapa. Acessada via propriedade orthofotos da instancia GeoApiClient. Tipo Orthophoto importado de @carf/tscore/types conforme [02-types-entities](../../TSCORE/DOCS/API/02-types-entities.md). Endpoints conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| POST | /api/orthofotos/upload | Upload de ortofoto GeoTIFF | 202 Accepted | 413 FILE_TOO_LARGE, 415 UNSUPPORTED_FORMAT | analyst+ |
| GET | /api/orthofotos/{id} | Obter metadados | 200 | 404 | todos autenticados |
| GET | /api/orthofotos | Listar ortofotos do tenant | 200 | - | todos autenticados |
| GET | /api/orthofotos/{id}/tiles/{z}/{x}/{y} | Obter tile PNG 256x256 | 200 image/png | 404 | todos autenticados |
| GET | /api/orthofotos/jobs/{jobId} | Status do processamento | 200 | 404 | analyst+ |

## upload (POST /api/orthofotos/upload)

Faz upload de ortofoto para processamento assincrono via Hangfire. Aceita multipart/form-data com campo file contendo arquivo GeoTIFF (tipo aceito: image/tiff, tamanho maximo 500MB), communityId como UUID opcional e captureDate como string ISO 8601 opcional.

Response retorna HTTP 202 Accepted (processamento assincrono) com body:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| ortofotoId | string | UUID do registro criado para a ortofoto |
| jobId | string | UUID do job Hangfire para acompanhamento |

O processamento gera versao JPEG otimizada para web e tiles XYZ para exibicao no mapa. O client deve usar o jobId para consultar o progresso via getJobStatus.

## list (GET /api/orthofotos)

Lista ortofotos do tenant com paginacao padrao. Aceita query params page, limit e opcionalmente communityId e processingStatus para filtrar. Retorna PaginatedResponse de Orthophoto. Acessivel por todos os usuarios autenticados.

## getById (GET /api/orthofotos/{id})

Busca ortofoto por ID. Aceita id string, retorna Promise de Orthophoto com todos os campos incluindo tilesPath e boundsGeojson quando processamento concluido. Lanca NotFoundError 404 se nao existir.

## getTile (GET /api/orthofotos/{id}/tiles/{z}/{x}/{y})

Obtem tile individual no padrao XYZ para exibicao em mapa. Aceita id string, z (zoom level de 12 a 20), x (coluna) e y (linha). Retorna imagem PNG 256x256 pixels com Content-Type image/png. Retorna NotFoundError 404 para tiles inexistentes (areas sem dados). Response inclui Cache-Control com max-age de 86400 (1 dia) pois tiles nao mudam apos processamento. No REURBCAD mobile, tiles sao cacheados localmente para uso offline via tileOverlay do MapComponent do @carf/ui-native.

## getJobStatus (GET /api/orthofotos/jobs/{jobId})

Consulta status de processamento assincrono. Aceita jobId string, retorna:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| status | string | PENDING, PROCESSING, COMPLETED ou FAILED |
| progress | number | Percentual estimado de progresso (0 a 100) |
| error | string ou null | Mensagem de erro quando status FAILED |
| ortofotoId | string | UUID da ortofoto para referencia cruzada |

O client deve fazer polling periodico (recomendado a cada 5 segundos) enquanto status for PENDING ou PROCESSING. Quando COMPLETED, os campos optimizedPath e tilesPath da Orthophoto estarao preenchidos. Restrito a roles analyst ou superior.
