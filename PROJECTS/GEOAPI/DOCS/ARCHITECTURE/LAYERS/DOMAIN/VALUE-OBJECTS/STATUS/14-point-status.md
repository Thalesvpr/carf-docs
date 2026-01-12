# PointStatus

Value object enum representando estado no workflow de processamento de pontos topográficos desde coleta em campo até aprovação final para uso em documentos técnicos de regularização. Valores possíveis são COLLECTED (ponto coletado em campo com coordenadas brutas do receptor GPS mas ainda não processado com correção diferencial), PROCESSED (coordenadas processadas usando estações RBMC base com cálculo de precisões mas aguardando validação técnica), APPROVED (ponto validado e aprovado para uso em memoriais descritivos e plantas oficiais), e REJECTED (ponto rejeitado por precisão insuficiente devendo ser recoletado).

Métodos incluem CanProcess() verificando se está em COLLECTED permitindo processamento, CanApprove() verificando se está em PROCESSED permitindo aprovação, CanUseInDocuments() retornando true apenas para APPROVED, RequiresRecollection() verificando se REJECTED exige nova ida a campo, e ValidateTransition(PointStatus newStatus) lançando exception se transição inválida.

Usado em SurveyPoint.Status controlando fluxo COLLECTED → PROCESSED → {APPROVED | REJECTED} com domain events disparados nas transições, validado em DescriptiveMemorial e LegitimationPlan garantindo que apenas pontos APPROVED têm coordenadas incluídas em documentos oficiais, e integra com Role onde FIELD_AGENT coleta pontos, SURVEYOR processa, e MANAGER aprova ou rejeita.

---

**Última atualização:** 2026-01-12
