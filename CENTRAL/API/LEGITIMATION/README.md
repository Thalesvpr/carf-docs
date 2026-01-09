# LEGITIMATION

Schemas JSON para processos de legitimação fundiária do CARF. LegitimationProcessCreateRequest (unit_id, process_type enum REURB-S/REURB-E conforme Lei 13.465/2017, documents array de DocumentUploadRequest com type/file_url, notes), LegitimationProcessResponse (id UUID, unit relação, process_type, status enum Iniciado/Em Análise/Aprovado/Rejeitado/Cancelado, documents array, workflow_history array de status transitions com timestamp/user/comments, started_at, completed_at, tenant_id), TransitionStatusRequest (process_id, new_status, comments obrigatório para Rejeitado), DocumentUploadRequest (type enum CPF/RG/Comprovante Residência/Planta/Foto, file objeto com name/size/mime_type, upload_url pre-signed S3). Workflow: Iniciado → Em Análise (requer role Técnico) → Aprovado/Rejeitado (requer role Fiscal). Validações: documentos obrigatórios conforme process_type, critérios Lei 13.465 (área max, renda, tempo ocupação).

---

**Última atualização:** 2025-12-29
