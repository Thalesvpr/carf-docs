# WORKFLOW-RULES

Regras de workflow de aprovação do CARF. unit-approval-flow.md define estados (Rascunho→Pendente→Em Análise→Aprovado/Rejeitado/Cancelado), transições permitidas (Rascunho→Pendente requer titular principal + coordenadas, Pendente→Em Análise requer role Técnico, Em Análise→Aprovado/Rejeitado requer role Fiscal), irreversibilidade (Aprovado é final, Rejeitado pode voltar Rascunho após correções). status-permissions.md mapeia role por transição (Técnico cadastra Rascunho, submete Pendente, move Em Análise; Fiscal aprova/rejeita). sla-rules.md define SLAs (Pendente→Em Análise: 5 dias úteis, Em Análise→Decisão: 10 dias úteis), alertas enviados 80% SLA. notifications.md especifica quando notificar (status change email titular, aprovação gera PDF título, rejeição email com motivo). Workflow implementado via state pattern em LegitimationProcess entity.

## Regras Documentadas

### State Machines
- **[unit-status-transitions.md](./unit-status-transitions.md)** - State machine de Unit (6 estados: DRAFT, PENDING_ANALYSIS, IN_REVIEW, APPROVED, REJECTED, REQUIRES_CHANGES)
- **[legitimation-status-transitions.md](./legitimation-status-transitions.md)** - State machine de LegitimationRequest (11 estados workflow conforme Lei 13465/2017)

### Permissões e Roles
- **[role-permissions.md](./role-permissions.md)** - Mapeamento de roles por transição (Técnico, Fiscal, Administrador)

### SLAs e Notificações
- **[sla-rules.md](./sla-rules.md)** - SLAs por transição (Pendente→Em Análise: 5 dias úteis, Em Análise→Decisão: 10 dias úteis)
- **[notification-triggers.md](./notification-triggers.md)** - Triggers de notificação (status change, aprovação, rejeição)

---

**Última atualização:** 2025-01-05
