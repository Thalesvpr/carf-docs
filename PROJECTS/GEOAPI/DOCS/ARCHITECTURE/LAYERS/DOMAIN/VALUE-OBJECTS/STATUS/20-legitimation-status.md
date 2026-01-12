# LegitimationStatus

Value object enum representando estado no workflow completo de processo de legitimação fundiária desde solicitação inicial até emissão de certidão final, com 11 estados cobrindo toda jornada conforme Lei 13.465/2017. Estados seguem fluxo: DRAFT (rascunho da solicitação), SUBMITTED (submetido para análise inicial), UNDER_ANALYSIS (em análise técnica pelo analista), PENDING_DOCUMENTATION (aguardando documentação complementar), APPROVED_FOR_PUBLICATION (aprovado para publicação de edital), PUBLISHED (edital publicado aguardando prazo legal de contestação), CONTESTED (recebeu contestação requerendo análise jurídica), APPROVED_FOR_CERTIFICATE (aprovado para emissão de certidão), CERTIFICATE_ISSUED (certidão emitida), REGISTERED (registrado em cartório) e REJECTED (rejeitado devendo reiniciar).

Métodos incluem CanEdit() verificando se permite alteração (apenas DRAFT e PENDING_DOCUMENTATION), CanPublish() verificando se pode publicar edital, IsInLegalWaitingPeriod() verificando prazo legal, CanIssueCertificate() verificando pré-requisitos para emissão, IsFinalState() retornando true para estados finais, GetNextPossibleStatuses() retornando transições válidas, e GetLegalDeadlineDays() retornando prazo conforme legislação (PUBLISHED: 60 dias).

Usado em LegitimationRequest.Status controlando workflow com validações rigorosas de transição, dispara eventos em cada mudança notificando partes interessadas, e alimenta dashboards mostrando funil de conversão e tempo médio em cada estágio do processo de regularização fundiária.

---

**Última atualização:** 2026-01-12
