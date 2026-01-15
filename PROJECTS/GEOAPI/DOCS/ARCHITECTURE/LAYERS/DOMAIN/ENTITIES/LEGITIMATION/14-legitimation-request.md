# LegitimationRequest

Entidade aggregate root representando solicitação legitimação fundiária conforme Lei 13465/2017 com workflow completo submissão até emissão certidão coordenando análise técnica publicação edital geração documentos oficiais. Herda de BaseAggregateRoot suportando domain events LegitimationSubmittedEvent LegitimationApprovedEvent LegitimationRejectedEvent ao longo processo. Campos principais incluem UnitId Guid FK Unit objeto legitimação, RequestNumber string único processo (LEG-2025-0001), RequestDate DateTime protocolo, RequesterId Guid FK Account solicitante e LegitimationStatus 11 estados DRAFT até REGISTERED workflow.

Campos análise incluem Priority (LOW NORMAL HIGH URGENT) influenciando fila, AnalystId Guid nullable Account analista atribuído, PublishedAt DateTime nullable quando edital publicado e PublicationEndDate DateTime nullable prazo contestação 60 dias. Relacionamentos incluem Unit sendo legitimada, LegitimationResponse parecer analista, LegitimationCertificate se aprovado, DescriptiveMemorial e LegitimationPlan gerados.

Métodos incluem Submit() validando dados mudando SUBMITTED, AssignAnalyst(analystId) atribuindo responsável, Publish() publicando edital, IsWithinContestationPeriod() verificando contestações, CanIssueCertificate() validando pré-requisitos e AdvanceWorkflow(newStatus) controlando transições válidas LegitimationStatus.ValidateTransition(). Dispara eventos cada transição notificações automáticas integração sistemas publicação oficial editais.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
