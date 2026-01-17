# LegitimationCertificate

Entidade representando certidão legitimação fundiária documento oficial emitido após aprovação LegitimationResponse formalizando reconhecimento propriedade Lei 13465/2017 identificação imóvel proprietário áreas situação registral permitindo registro cartório. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem ResponseId Guid FK parecer fundamenta emissão, CertificateNumber string único sequencial (CERT-2025-00123) rastreabilidade, PropertyIdentification string identificação completa imóvel endereço coordenadas e OwnerName string completo proprietários extraído Holder vinculados Unit.

Campos área incluem LegitimatedArea decimal m² ocupada regularizada, RemainingArea decimal nullable remanescente se parcial, TotalArea decimal nullable original e CertificateSituation (COVERED CONFRONTING BOTH). Campos emissão incluem LegalBasis string Lei 13465/2017 artigos, IssuedAt DateTime emissão, IssuedBy Guid FK Account autoridade, SignaturePath SealPath strings nullable S3, PdfPath S3 PDF final e QrCode string nullable verificação autenticidade.

Métodos incluem GeneratePdf() compilando template oficial IPdfGenerator cabeçalho logo texto dados assinatura selo QrCode, GenerateQrCode() URL verificação pública, Validate() campos obrigatórios e GetRelatedUnit() navegando ResponseId→RequestId→UnitId. Regra negócio CertificateNumber único tenant, LegitimatedArea não excede Unit.Area, IssuedBy MANAGER+. Dispara LegitimationCertificateIssuedEvent notificando requerente email PDF. Relaciona DescriptiveMemorial LegitimationPlan anexos técnicos.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
