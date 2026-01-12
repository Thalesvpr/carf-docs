# UnitStatus

Value object enum representando estados do workflow de cadastro e aprovação de unidades habitacionais, controlando transições válidas de status e permissões de edição em cada estágio do processo de regularização. Valores possíveis são DRAFT (rascunho inicial criado por técnico de campo, editável livremente), PENDING_ANALYSIS (submetido para análise técnica, não editável por campo), IN_REVIEW (em revisão por analista, pode solicitar correções), APPROVED (aprovado para emissão de certidão, imutável exceto por administradores), REJECTED (rejeitado com justificativa, retorna para DRAFT para correção) e REQUIRES_CHANGES (analista solicitou mudanças específicas).

Transições válidas seguem fluxo DRAFT → PENDING_ANALYSIS → IN_REVIEW → {APPROVED | REJECTED | REQUIRES_CHANGES}, sendo que REJECTED e REQUIRES_CHANGES retornam para DRAFT após correções. Métodos incluem CanEdit() verificando se status permite edição, CanSubmit() verificando se pode avançar para análise, CanApprove() verificando se está em estado aprovável, e ValidateTransition(UnitStatus newStatus) lançando exception se transição inválida.

Usado em Unit para controlar workflow com domain event UnitStatusChangedEvent disparado em cada transição, integrando com sistema de permissões via Role (FIELD_AGENT pode editar DRAFT, ANALYST pode analisar PENDING_ANALYSIS) e auditoria rastreando quem e quando cada mudança de status ocorreu.

---

**Última atualização:** 2026-01-12
