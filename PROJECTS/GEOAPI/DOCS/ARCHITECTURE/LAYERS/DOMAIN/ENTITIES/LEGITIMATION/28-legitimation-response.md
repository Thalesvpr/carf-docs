# LegitimationResponse

Entidade representando parecer técnico LegitimationRequest emitido analista após avaliação solicitação legitimação fundiária contendo decisão justificativa condições permitindo aprovação rejeição solicitação correções. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem RequestId Guid FK solicitação respondida relacionamento 1:N múltiplas respostas ao longo processo, AnalystId Guid FK Account analista responsável, ResponseDate DateTime emissão e Decision (APPROVED REJECTED NEEDS_CORRECTION).

Campos parecer incluem Justification string texto detalhado citando Lei 13465/2017 normas técnicas critérios elegibilidade mínimo 100 caracteres fundamentação, Conditions string nullable ressalvas se APPROVED, RequiredDocuments JSON nullable array documentos adicionais se NEEDS_CORRECTION, DueDate DateTime nullable prazo correções tipicamente 30 dias e InternalNotes string nullable observações internas analistas.

Métodos incluem Approve(justification conditions) transitando Status APPROVED, Reject(justification) transitando REJECTED finalizando negativamente, RequestCorrection(justification requiredDocs dueDate) transitando REQUIRES_CHANGES, UpdateRequest() disparando LegitimationApprovedEvent LegitimationRejectedEvent e IsOverdue() verificando prazo expirou. Regra negócio apenas Role MANAGER ANALYST podem criar. Integra RequestId histórico completo respostas evolução processo, dispara eventos notificações automáticas email app mobile e resposta APPROVED permite geração LegitimationCertificate.

---

**Última atualização:** 2026-01-12
