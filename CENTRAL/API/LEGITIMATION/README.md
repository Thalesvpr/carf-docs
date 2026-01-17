# LEGITIMATION

Schemas JSON para processos de legitimação fundiária do CARF conforme Lei 13.465/2017.

O LegitimationProcessCreateRequest contém unit_id, process_type (REURB-S ou REURB-E), documents array e notes. O LegitimationProcessResponse inclui status, workflow_history com transições e timestamps.

Workflow: Iniciado → Em Análise (requer role Técnico) → Aprovado/Rejeitado (requer role Fiscal). Transição para Rejeitado requer comentários obrigatórios.

Validações: documentos obrigatórios conforme modalidade, critérios da Lei 13.465 (área máxima, renda, tempo de ocupação).

## Endpoints

- POST /api/legitimation - Iniciar processo
- GET /api/legitimation/{id} - Obter processo com histórico
- POST /api/legitimation/{id}/transition - Transicionar status
- POST /api/legitimation/{id}/documents - Upload de documentos

## Schemas

- LegitimationProcessCreateRequest / LegitimationProcessResponse
- TransitionStatusRequest
- DocumentUploadRequest

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review
