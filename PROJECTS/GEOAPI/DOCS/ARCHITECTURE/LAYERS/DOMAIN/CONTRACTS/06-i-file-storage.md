---
type: leaf
status: review
updated: 2026-02-08
---

# IFileStorage

Interface abstraindo operacoes de armazenamento de arquivos permitindo upload, download e exclusao de documentos, fotos e PDFs em storage cloud (AWS S3) ou local, mantendo dominio independente de provider especifico.

## Metodos

| Metodo | Parametros | Retorno | Descricao |
| --- | --- | --- | --- |
| UploadAsync | Stream, fileName, contentType, folder | string | Faz upload retornando path completo no S3. |
| DownloadAsync | string filePath | Stream | Retorna Stream do arquivo para download. |
| DeleteAsync | string filePath | Task | Remove arquivo permanentemente. |
| GetPresignedUrlAsync | string filePath, TimeSpan expiration | string | Gera URL temporaria assinada para download direto. |
| ExistsAsync | string filePath | bool | Verifica existencia sem baixar. |

Implementada por S3FileStorage usando AWS SDK, organizando por tenant: bucket/tenant-guid/documents/. Aplica validacoes de contentType e limites de tamanho (fotos: 10MB, PDFs: 50MB). Usada em Document, LegitimationCertificate, DescriptiveMemorial e LegitimationPlan.
