# DOCUMENTS

Entity gerenciamento documentos anexos do GEOAPI armazenando metadados arquivos uploadados S3-compatible storage vinculados entidades via polymorphic relationship. Document contém EntityType enum (UNIT/HOLDER/LEGITIMATION/COMMUNITY) e EntityId Guid identificando owner, DocumentType enum (PHOTO/PDF/DEED/ID_CARD/UTILITY_BILL) categorizando, FileName original preservado, FileSize bytes para validação limits quotas, MimeType validado whitelist prevenindo upload executáveis maliciosos, StoragePath string key S3 onde blob armazenado formato tenant_id/entity_type/entity_id/filename_guid.ext organizando hierarquicamente, UploadedAt timestamp e UploadedBy AccountId auditando origem. Métodos behavior incluem GeneratePresignedUrl() retornando URL temporária download direto S3 sem proxy API reduzindo bandwidth, MarkAsVerified() workflow analista confirmou autenticidade documento digitado e Delete() soft marcando IsDeleted mas mantendo StoragePath para compliance retention policies LGPD permitindo recuperação auditorias antes garbage collection S3 lifecycle rules removerem fisicamente após período legal.

## Arquivos

- **[10-document.md](./10-document.md)** - Documento anexo arquivo S3 vinculado entidades

---

**Última atualização:** 2026-01-12
