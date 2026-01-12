# Decision

Value object enum representando decisão de analista em parecer técnico sobre solicitação de legitimação fundiária, determinando próximos passos no workflow e ações necessárias. Valores possíveis são APPROVED (aprovado sem ressalvas podendo avançar para próxima etapa), REJECTED (rejeitado com justificativa obrigatória retornando status para DRAFT), e NEEDS_CORRECTION (aprovado condicionalmente requerendo correções específicas antes de prosseguir, status vai para PENDING_DOCUMENTATION).

Métodos incluem RequiresJustification() retornando true para REJECTED e NEEDS_CORRECTION exigindo Justification preenchido, RequiresConditions() retornando true apenas para NEEDS_CORRECTION, AllowsProgression() retornando true para APPROVED permitindo avanço automático, GetNextStatus(LegitimationStatus currentStatus) determinando próximo status, e ToDisplayString() retornando descrição amigável.

Usado em LegitimationResponse.Decision registrando parecer do analista, valida que REJECTED tem justificativa detalhada e NEEDS_CORRECTION especifica correções necessárias, dispara notificações diferentes conforme decisão (parabeniza solicitante, explica motivos, lista pendências), e alimenta métricas de qualidade rastreando taxa de aprovação e tempo médio entre submissão e decisão por analista.

---

**Última atualização:** 2026-01-12
