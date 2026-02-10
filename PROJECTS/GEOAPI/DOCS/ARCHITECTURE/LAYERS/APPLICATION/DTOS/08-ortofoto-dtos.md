---
type: leaf
status: review
updated: 2026-02-09
---

# Ortofoto DTOs

Os Data Transfer Objects de ortofotos definem os contratos de entrada e saida da API para operacoes de upload, processamento e servico de tiles.

## DTOs de Resposta

OrtofotoDto e o DTO completo retornado em operacoes de leitura individual.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico |
| CommunityId | Guid | Comunidade vinculada (nullable) |
| FileSize | long | Tamanho do original em bytes |
| Width | int | Largura em pixels (nullable, preenchido apos processamento) |
| Height | int | Altura em pixels (nullable) |
| Srid | int | Sistema de referencia espacial (nullable) |
| BoundsGeoJson | object | Limites geograficos em GeoJSON Polygon (nullable) |
| CaptureDate | DateTime | Data do voo (nullable) |
| ProcessingStatus | string | PENDING, PROCESSING, COMPLETED, FAILED |
| ProcessingError | string | Mensagem de erro (nullable) |
| SourceType | string | Origem da ortofoto: UPLOAD ou PIX4D_LINK |
| SourceUrl | string | URL original do link Pix4D (nullable, preenchido apenas quando SourceType e PIX4D_LINK) |
| UploadedAt | DateTime | Momento do upload |
| ProcessedAt | DateTime | Quando processamento concluiu (nullable) |

OrtofotoListItemDto e o DTO reduzido para listagens contendo Id, CommunityId, CaptureDate, FileSize, ProcessingStatus e UploadedAt.

ProcessingJobStatusDto e retornado pela consulta de status do job.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Status | string | PENDING, PROCESSING, COMPLETED, FAILED |
| Progress | int | Percentual estimado |
| Error | string | Mensagem de erro (nullable) |
| OrtofotoId | Guid | Referencia cruzada |

UploadOrtofotoResponseDto e retornado pelo upload com OrtofotoId (UUID do registro) e JobId (UUID do job Hangfire).

## DTOs de Request

UploadOrtofotoRequest e recebido como multipart/form-data contendo file (IFormFile obrigatorio, GeoTIFF maximo 500MB), communityId (UUID opcional) e captureDate (ISO 8601 opcional).

SubmitPix4dLinkRequest e recebido como JSON body para submissao de ortofoto via link Pix4D.

| Propriedade | Tipo | Obrigatorio | Descricao |
|-------------|------|-------------|-----------|
| Url | string | sim | URL HTTPS do link Pix4D apontando para o arquivo GeoTIFF |
| CommunityId | Guid | nao | Comunidade vinculada |
| CaptureDate | DateTime | nao | Data do voo de captura (ISO 8601) |

A validacao e feita por SubmitPix4dLinkValidator, que verifica que Url e uma URL valida com protocolo HTTPS.

SubmitPix4dLinkResponseDto e retornado pelo endpoint from-link com OrtofotoId (UUID do registro criado).
