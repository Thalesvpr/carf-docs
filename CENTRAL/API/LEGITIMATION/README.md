# LEGITIMATION

Schemas JSON para processos de legitimação fundiária do CARF. LegitimationProcessCreateRequest (unit_id, process_type enum REURB-S/REURB-E conforme Lei 13.465/2017, documents array de DocumentUploadRequest com type/file_url, notes), LegitimationProcessResponse (id UUID, unit relação, process_type, status enum Iniciado/Em Análise/Aprovado/Rejeitado/Cancelado, documents array, workflow_history array de status transitions com timestamp/user/comments, started_at, completed_at, tenant_id), TransitionStatusRequest (process_id, new_status, comments obrigatório para Rejeitado), DocumentUploadRequest (type enum CPF/RG/Comprovante Residência/Planta/Foto, file objeto com name/size/mime_type, upload_url pre-signed S3). Workflow: Iniciado → Em Análise (requer role Técnico) → Aprovado/Rejeitado (requer role Fiscal). Validações: documentos obrigatórios conforme process_type, critérios Lei 13.465 (área max, renda, tempo ocupação).

## Implementação e Uso

Endpoint de Processos de Legitimação implementado pelo backend [GEOAPI](../../../PROJECTS/GEOAPI/DOCS/ARCHITECTURE/01-overview.md) usando aggregate [LegitimationRequestAggregate](../../DOMAIN-MODEL/AGGREGATES/03-legitimation-request-aggregate.md) com workflow state machine conforme [regras de transição de status](../../DOMAIN-MODEL/BUSINESS-RULES/WORKFLOW-RULES/legitimation-status-transitions.md) validando fluxo de aprovação documentado em [UC-009: Gerenciar Processo de Legitimação](../../REQUIREMENTS/USE-CASES/UC-009-gerenciar-processo-legitimacao.md), consumido por [GEOWEB](../../../PROJECTS/GEOWEB/DOCS/README.md) para interface de aprovação administrativa e [ADMIN](../../../PROJECTS/ADMIN/DOCS/README.md) para audit trail via endpoint admin-specific `/api/admin/legitimation` documentado em [GEOAPI Admin Security](../../../PROJECTS/GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md).

---

**Última atualização:** 2025-12-29
