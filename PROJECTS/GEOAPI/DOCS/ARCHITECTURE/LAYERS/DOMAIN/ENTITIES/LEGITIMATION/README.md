# LEGITIMATION

Entities workflow legitimação fundiária do GEOAPI implementando processo legal REURB conforme Lei 13465/2017 com tramitação análise técnica jurídica decisão expedição título. LegitimationRequest aggregate root iniciando processo com UnitId referenciando unidade, RequestType enum (REURB_S/REURB_E) determinando modalidade elegibilidade custos, Status value object onze estados workflow (DRAFT/SUBMITTED/UNDER_TECHNICAL_REVIEW/APPROVED/REJECTED/REQUIRES_CHANGES/CONTESTED/FINAL_APPROVAL/CERTIFICATE_ISSUED), RequestedBy AccountId titular solicitante, SubmittedAt timestamp protocolo e Documents collection comprobatórios necessários modalidade, disparando domain events status transitions notificando stakeholders via SignalR. LegitimationResponse entity armazena parecer técnico com Decision enum (APPROVE/REJECT/REQUEST_CHANGES), Justification texto fundamentação legal técnica, ReviewedBy AccountId analista responsável e ReviewedAt timestamp auditoria decisão. LegitimationCertificate entity representa título legitimação posse expedido após aprovação com CertificateNumber único sequencial tenant, IssuedAt data expedição, IssuedBy autoridade competente, LegalDescription memorial descritivo área coordenadas limites confrontações, CertificateSituation enum (ACTIVE/CANCELLED/SUSPENDED) e PdfPath S3 onde documento PDF assinado digitalmente ICP-Brasil armazenado para impressão registro cartório. DescriptiveMemorial entity detalha limites confrontações com BoundaryDescription texto narrativo, Coordinates lista ordenada vértices polígono fechado, Area oficial calculada, Neighbors confrontantes lados respectivos e TechnicalResponsible Surveyor ART anotação responsabilidade técnica. LegitimationPlan agrega múltiplas LegitimationRequests community organizando tramitação lote reduzindo custos operacionais com PlanName identificador, CommunityId abrangência, TargetUnits quantidade meta, Status agregado e ProjectedCompletionDate prazo estimado conclusão.

## Arquivos

- **[14-legitimation-request.md](./14-legitimation-request.md)** - Solicitação legitimação REURB aggregate root
- **[28-legitimation-response.md](./28-legitimation-response.md)** - Parecer técnico decisão analista
- **[29-legitimation-certificate.md](./29-legitimation-certificate.md)** - Título legitimação posse expedido
- **[30-descriptive-memorial.md](./30-descriptive-memorial.md)** - Memorial descritivo limites confrontações
- **[31-legitimation-plan.md](./31-legitimation-plan.md)** - Plano tramitação lote community

---

**Última atualização:** 2026-01-12
