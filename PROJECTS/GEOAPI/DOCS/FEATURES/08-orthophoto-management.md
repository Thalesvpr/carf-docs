---
type: leaf
status: review
updated: 2026-02-21
---

# Orthophoto Management Feature

A feature de gerenciamento de ortofotos permite ingestao de imagens aereas capturadas por drone em formato GeoTIFF por dois caminhos: upload direto de arquivo ou submissao de link Pix4D para download automatico. Apos ingestao, o processamento assincrono via Hangfire gera versao otimizada para web, servida para renderizacao em mapa interativo. O processamento assincrono retorna HTTP 202 Accepted com identificador para acompanhamento.

## User Stories

US-070 Upload de Ortofoto: o analista faz upload de arquivo GeoTIFF de ate 500MB via multipart/form-data, opcionalmente vinculando a uma comunidade e informando a data de captura do voo. O servidor registra o upload, agenda o processamento via Hangfire e retorna ortofotoId e jobId para acompanhamento.

US-071 Acompanhar Processamento: o analista consulta o status do processamento informando o jobId, recebendo status (PENDING, PROCESSING, COMPLETED, FAILED), percentual de progresso estimado e mensagem de erro quando aplicavel.

US-073 Submeter Link Pix4D: o analista submete uma URL HTTPS de link Pix4D apontando para um arquivo GeoTIFF processado na nuvem, opcionalmente vinculando a uma comunidade e informando a data de captura. O servidor valida a URL, baixa o arquivo via streaming, armazena no S3, registra a origem como PIX4D_LINK com a URL original, agenda processamento e retorna ortofotoId para acompanhamento. Isso elimina a necessidade de download manual seguido de upload, agilizando o fluxo para ortofotos ja processadas em plataforma cloud.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /api/orthofotos/upload | Upload GeoTIFF multipart |
| POST | /api/orthofotos/from-link | Submeter link Pix4D para download |
| GET | /api/orthofotos/{id} | Obter metadados |
| GET | /api/orthofotos | Listar ortofotos do tenant |
| GET | /api/orthofotos/jobs/{jobId} | Status do processamento |

## Regras de Negocio

RN-070: tipo MIME aceito e image/tiff (GeoTIFF). Outros formatos retornam 415 UNSUPPORTED_FORMAT. RN-071: tamanho maximo e 500MB. Arquivos maiores retornam 413 FILE_TOO_LARGE. RN-072: processamento gera versao JPEG otimizada para visualizacao web. RN-074: processamento assincrono via Hangfire permite acompanhamento por jobId com status PENDING, PROCESSING, COMPLETED ou FAILED. RN-075: metadados (width, height, srid, bounds_geojson) sao extraidos via GDAL durante processamento. RN-076: submissao de link Pix4D aceita apenas URLs com protocolo HTTPS. URLs HTTP ou invalidas retornam 400 INVALID_URL. RN-077: o download do link e feito via streaming com validacao de Content-Type (image/tiff) e tamanho maximo (500MB). Falha no download retorna 422 DOWNLOAD_FAILED. RN-078: cada ortofoto registra sua origem via source_type (UPLOAD ou PIX4D_LINK) e source_url (preenchido apenas para PIX4D_LINK).

## Permissoes

| Acao | field-cadastrator | field-coordinator | drone-operator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|----------------|---------|---------|-------|-------------|
| Upload | nao | nao | sim | sim | sim | sim | sim |
| Submeter link Pix4D | nao | nao | sim | sim | sim | sim | sim |
| Visualizar metadados | sim | sim | sim | sim | sim | sim | sim |
| Listar | sim | sim | sim | sim | sim | sim | sim |
| Status processamento | nao | nao | sim | sim | sim | sim | sim |
