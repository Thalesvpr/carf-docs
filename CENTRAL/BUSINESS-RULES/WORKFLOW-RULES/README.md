# WORKFLOW-RULES

Regras workflow aprovação CARF incluindo unit-status-transitions state machine Unit seis estados DRAFT PENDING_ANALYSIS IN_REVIEW APPROVED REJECTED REQUIRES_CHANGES transições permitidas DRAFT para PENDING_ANALYSIS requer titular principal coordenadas PENDING_ANALYSIS para IN_REVIEW requer role Técnico IN_REVIEW para APPROVED REJECTED requer role Fiscal irreversibilidade APPROVED final REJECTED pode voltar DRAFT após correções legitimation-status-transitions state machine LegitimationRequest onze estados workflow conforme Lei 13465/2017 DRAFT SUBMITTED UNDER_ANALYSIS DOCUMENT_REVIEW TECHNICAL_REVIEW PUBLIC_NOTICE CONTESTATION_PERIOD RESOLUTION APPROVED REJECTED NEEDS_CORRECTION role-permissions mapeia role por transição Técnico cadastra DRAFT submete PENDING_ANALYSIS move IN_REVIEW Fiscal aprova rejeita sla-rules define SLAs PENDING_ANALYSIS para IN_REVIEW cinco dias úteis IN_REVIEW para Decisão dez dias úteis alertas enviados oitenta por cento SLA notification-triggers especifica quando notificar status change email titular aprovação gera PDF título rejeição email com motivo workflow implementado via state pattern LegitimationProcess entity.

## Regras

- **[legitimation-status-transitions.md](./legitimation-status-transitions.md)** - State machine LegitimationRequest onze estados Lei 13465/2017
- **[notification-triggers.md](./notification-triggers.md)** - Triggers notificações email status changes aprovação rejeição
- **[role-permissions.md](./role-permissions.md)** - Mapeamento roles permissions transições Técnico Fiscal
- **[sla-rules.md](./sla-rules.md)** - SLAs workflow prazos cinco dez dias alertas
- **[unit-status-transitions.md](./unit-status-transitions.md)** - State machine Unit seis estados transições permitidas

---

**Última atualização:** 2026-01-11
