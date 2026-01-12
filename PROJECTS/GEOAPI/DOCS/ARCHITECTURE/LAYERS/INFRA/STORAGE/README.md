# STORAGE

Implementação IFileStorage para gerenciamento arquivos (documentos, fotos, PDFs) do GEOAPI usando storage S3-compatible com MinIO em desenvolvimento e AWS S3 em produção suportando upload/download multipart streaming de arquivos grandes, URLs pré-assinadas temporárias para acesso direto sem passar pela API e organização hierárquica por tenant/feature/entity. S3FileStorage encapsula AWS SDK configurado via appsettings.json com buckets segregados por ambiente (dev/staging/prod), prefixos por tenant garantindo isolamento físico dados, e metadata customizado armazenando content-type, tenant_id, entity_id rastreável para audit. Upload chunked permite arquivos > 100MB com progress tracking e retry automático de chunks falhados, virus scanning via ClamAV antes de aceitar arquivo permanentemente e compressão/otimização automática de imagens via ImageSharp reduzindo custos storage. URLs pré-assinadas geradas com expiration 1h permitem frontend fazer upload/download direto do S3 reduzindo carga na API mas com validação prévia de permissões usuário antes de gerar URL.

## Arquivos Principais (a criar)

**Core:**
- 01-s3-file-storage.md - Implementação AWS S3/MinIO
- 02-file-metadata.md - Metadata tracking (tenant, entity, type)

**Upload:**
- 03-multipart-upload.md - Upload chunked para arquivos grandes
- 04-presigned-urls.md - URLs temporárias acesso direto

**Processing:**
- 05-image-optimization.md - Compressão/resize automático
- 06-virus-scanning.md - ClamAV integration

**Organization:**
- 07-bucket-strategy.md - Estrutura buckets e prefixos
- 08-cleanup-policies.md - Lifecycle e remoção arquivos orfãos

---

**Última atualização:** 2026-01-12
