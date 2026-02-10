---
type: leaf
status: review
updated: 2026-02-09
---

# Ortofoto Commands

Os commands de ortofotos representam operacoes de ingestao e processamento assincrono de imagens aereas GeoTIFF. A ingestao pode ocorrer de duas formas: upload direto de arquivo via multipart/form-data ou submissao de link Pix4D para download automatico. Ambos os fluxos armazenam o arquivo original no S3 e agendam processamento via Hangfire. O processamento gera tiles XYZ e versao otimizada para web.

---

## UploadOrtofotoCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| File | IFormFile | sim | Arquivo GeoTIFF (maximo 500MB) |
| CommunityId | Guid | nao | Comunidade vinculada |
| CaptureDate | DateTime | nao | Data do voo de captura |

O handler valida tipo MIME (aceita apenas image/tiff) e tamanho maximo (500MB). Armazena o arquivo original no S3 via IFileStorage no caminho padrao do tenant. Cria registro na tabela orthofotos com processing_status PENDING, file_size e uploaded_by. Agenda job Hangfire do tipo ProcessOrtofotoJob passando o ortofotoId. Retorna HTTP 202 Accepted com ortofotoId (UUID do registro) e jobId (UUID do job Hangfire).

Erros possiveis: FILE_TOO_LARGE para arquivos acima de 500MB, UNSUPPORTED_FORMAT para tipos MIME diferentes de image/tiff.

---

## ProcessOrtofotoCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| OrtofotoId | Guid | sim | Identificador da ortofoto a processar |

O handler e executado de forma assincrona via Hangfire. Atualiza processing_status para PROCESSING. Utiliza GDAL para extrair metadados (width, height, srid, bounds_geojson). Gera versao JPEG otimizada para visualizacao web e armazena no S3 em optimized_path. Gera tiles XYZ para zoom levels 12 a 20 como imagens PNG 256x256 pixels, armazenando no S3 sob tiles_path. Ao concluir, atualiza processing_status para COMPLETED e preenche processed_at. Em caso de erro, atualiza para FAILED e registra mensagem em processing_error.

Emite OrtofotoProcessedEvent com OrtofotoId quando COMPLETED ou OrtofotoProcessingFailedEvent quando FAILED.

---

## SubmitPix4dLinkCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Request | SubmitPix4dLinkRequest | sim | DTO contendo Url, CommunityId e CaptureDate |

O handler recebe um SubmitPix4dLinkRequest via JSON body (nao multipart). Primeiro, o SubmitPix4dLinkValidator valida que a URL usa protocolo HTTPS e possui formato valido. Segundo, o handler invoca o contrato IHttpFileDownloader.DownloadAsync(url) para baixar o arquivo apontado pelo link Pix4D. O IHttpFileDownloader e implementado por HttpFileDownloader, que executa HTTP GET com streaming, valida que o Content-Type da resposta e image/tiff e respeita o limite maximo de 500MB. Terceiro, o handler armazena o arquivo baixado no S3 via IFileStorage no caminho padrao do tenant. Quarto, cria registro na tabela orthofotos com processing_status PENDING, file_size, uploaded_by, source_type PIX4D_LINK e source_url contendo a URL original. Quinto, agenda job Hangfire do tipo ProcessOrtofotoJob passando o ortofotoId. Retorna HTTP 202 Accepted com ortofotoId (UUID do registro).

Erros possiveis: INVALID_URL para URLs que nao usam HTTPS ou possuem formato invalido, DOWNLOAD_FAILED quando o download do link falha (timeout, 404, erro de rede), UNSUPPORTED_FORMAT quando o Content-Type da resposta nao e image/tiff, FILE_TOO_LARGE quando o arquivo excede 500MB.

### IHttpFileDownloader

Contrato de dominio para download de arquivos via HTTP.

```csharp
public interface IHttpFileDownloader
{
    Task<DownloadResult> DownloadAsync(string url, CancellationToken ct = default);
}

public record DownloadResult(Stream Content, long FileSize, string ContentType);
```

A implementacao HttpFileDownloader (camada Infra) utiliza HttpClient com streaming para evitar carga em memoria. Valida Content-Type e tamanho antes de completar o download. Aplica timeout configuravel (default 5 minutos).
