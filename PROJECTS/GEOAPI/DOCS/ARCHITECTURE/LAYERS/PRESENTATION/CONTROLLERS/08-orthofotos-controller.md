---
type: leaf
status: review
updated: 2026-02-09
---

# Orthofotos Controller

O OrthofotosController gerencia upload, consulta e servico de tiles de ortofotos aereas. A rota base e /api/orthofotos. O upload e restrito a roles analyst ou superior. Tiles sao servidos como imagem PNG para qualquer usuario autenticado.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| POST | /api/orthofotos/upload | Upload GeoTIFF multipart | 202 Accepted | 413 FILE_TOO_LARGE, 415 UNSUPPORTED_FORMAT | analyst+ |
| POST | /api/orthofotos/from-link | Submeter link Pix4D para download | 202 Accepted | 400 INVALID_URL, 422 DOWNLOAD_FAILED, 415 UNSUPPORTED_FORMAT, 413 FILE_TOO_LARGE | analyst+ |
| GET | /api/orthofotos/{id} | Obter metadados | 200 | 404 | todos autenticados |
| GET | /api/orthofotos | Listar ortofotos do tenant | 200 | - | todos autenticados |
| GET | /api/orthofotos/{id}/tiles/{z}/{x}/{y} | Obter tile PNG | 200 image/png | 404 | todos autenticados |
| GET | /api/orthofotos/jobs/{jobId} | Status do processamento | 200 | 404 | analyst+ |

## Comportamento

O endpoint de upload aceita multipart/form-data com campo file (GeoTIFF, maximo 500MB), communityId (UUID opcional) e captureDate (ISO 8601 opcional). O handler armazena o arquivo original no S3, cria registro na tabela orthofotos com processing_status PENDING, source_type UPLOAD e agenda job Hangfire para processamento. Retorna HTTP 202 Accepted com ortofotoId e jobId.

O endpoint from-link aceita JSON body com SubmitPix4dLinkRequest contendo url (string HTTPS obrigatoria), communityId (UUID opcional) e captureDate (ISO 8601 opcional). O handler valida a URL via SubmitPix4dLinkValidator, baixa o arquivo via IHttpFileDownloader com streaming, valida Content-Type image/tiff e tamanho maximo 500MB. Armazena o arquivo no S3, cria registro com processing_status PENDING, source_type PIX4D_LINK e source_url contendo a URL original. Agenda job Hangfire para processamento. Retorna HTTP 202 Accepted com ortofotoId. Diferente do upload, nao retorna jobId pois o download ja foi concluido no momento da resposta.

O endpoint de tiles serve imagens PNG 256x256 pixels com zoom level z entre 12 e 20, coordenadas x e y. O Content-Type e image/png e o Cache-Control define max-age de 86400 segundos (1 dia). Tiles inexistentes retornam 404. O endpoint de status do job retorna objeto com status, progress (percentual), error (nullable) e ortofotoId.

## Autorizacao

Upload, submissao de link Pix4D e consulta de status de processamento requerem role analyst, manager, admin ou super-admin. Consulta de metadados, listagem e servico de tiles sao acessiveis por qualquer usuario autenticado do tenant.
