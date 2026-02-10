---
type: leaf
status: review
updated: 2026-02-08
---

# Ortofoto Queries

As queries de ortofotos implementam o lado de leitura do CQRS para a tabela orthofotos, incluindo consulta de metadados, servico de tiles e status de processamento.

## GetOrtofotoByIdQuery

Recebe Id da ortofoto como Guid. O handler projeta para OrtofotoDto incluindo metadados (width, height, srid, bounds_geojson), caminhos S3 e status de processamento. Retorna 404 se nao encontrada.

## ListOrthofotosQuery

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| Page | int | 1 | Pagina atual |
| Limit | int | 20 | Registros por pagina |
| CommunityId | Guid | nulo | Filtro por comunidade |
| ProcessingStatus | string | nulo | Filtro por status de processamento |

Retorna PaginatedResult de OrtofotoListItemDto contendo id, communityId, captureDate, fileSize, processingStatus e uploadedAt.

## GetOrtofotoTileQuery

| Parametro | Tipo | Descricao |
|-----------|------|-----------|
| OrtofotoId | Guid | Identificador da ortofoto |
| Z | int | Zoom level (12 a 20) |
| X | int | Coluna do tile |
| Y | int | Linha do tile |

O handler constroi o caminho S3 do tile a partir de tiles_path, z, x e y. Retorna stream da imagem PNG 256x256 pixels via IFileStorage. Retorna 404 para tiles inexistentes (areas sem dados da ortofoto). O controller define Content-Type image/png e Cache-Control max-age 86400.

## GetProcessingJobStatusQuery

Recebe JobId como Guid. O handler consulta o status do job Hangfire e retorna objeto com status (PENDING, PROCESSING, COMPLETED, FAILED), progress (percentual estimado), error (mensagem quando FAILED) e ortofotoId para referencia cruzada. Retorna 404 se o job nao existe.
