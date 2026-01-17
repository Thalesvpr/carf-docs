# Document

Entidade representando arquivo digital (foto PDF DWG) vinculado polimorficamente qualquer entidade sistema via EntityType e EntityId armazenando metadados storage informações captura. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem EntityType indicando tipo entidade pai (UNIT HOLDER SURVEY_POINT), EntityId Guid, DocumentType categorizando (PHOTO_FRONT DOC_CPF PLANT MEMORIAL) determinando validações, FileName string original preservado, MimeType string e FileSize long bytes controle quota.

Campos storage incluem StoragePath string caminho S3 (tenant-id/entity-type/entity-id/uuid.ext), ThumbnailPath string nullable preview imagens, Width Height int nullable dimensões pixels. Campos geolocalização Latitude Longitude decimal nullable geotag GPS, CapturedAt DateTime nullable quando foto tirada extraído EXIF e UploadedBy Guid Account upload.

Métodos incluem GenerateStoragePath() path único S3, GenerateThumbnail() preview 200x200px, ExtractExifData() lendo metadados câmera GPS timestamp, ValidateFileSize() verificando limite Type e IsImage()/IsPdf()/IsTechnical() helpers categorização. Integra IFileStorage abstraindo S3 local storage, valida MIME type extensão whitelist e DocumentUploadedEvent dispara processamento assíncrono thumbnail extração metadados Hangfire job.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
