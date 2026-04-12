---
type: leaf
status: approved
updated: 2026-01-25
---

# Unit Status Transitions

Maquina de estados governando ciclo de vida de unidades habitacionais desde cadastro inicial ate aprovacao ou rejeicao. Estado inicial DRAFT permite cadastro incremental offline. Transicao para PENDING_ANALYSIS requer titular vinculado, geometria definida e foto anexada.

Analista assume unidade em IN_REVIEW com lock otimista de 2 horas. Pode aprovar (APPROVED), rejeitar (REJECTED) com justificativa obrigatoria, ou solicitar correcoes (REQUIRES_CHANGES). Aprovacao requer role MANAGER ou superior implementando dupla verificacao. Rejeicao retorna automaticamente para DRAFT permitindo correcoes.

## Estados e Permissoes

Estados incluem DRAFT (rascunho), PENDING_ANALYSIS (aguardando analista), IN_REVIEW (em analise), APPROVED (aprovado), REJECTED (rejeitado) e REQUIRES_CHANGES (correcoes necessarias). FIELD_COORDINATOR e FIELD_CADASTRATOR podem submeter, ANALYST pode revisar, MANAGER pode aprovar ou rejeitar. Reversao de APPROVED requer ADMIN com justificativa registrada em auditoria.

Validacoes automaticas verificam completude de campos, integridade referencial, area dentro de limites REURB (250m2 para REURB-S, 500m2 para REURB-E) e ausencia de sobreposicoes criticas com unidades vizinhas.
