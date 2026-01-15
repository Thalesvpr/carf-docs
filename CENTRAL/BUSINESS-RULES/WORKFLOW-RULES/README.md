# WORKFLOW-RULES

Regras de workflow do CARF governando transições de status através de state machines que definem quais mudanças são permitidas baseadas no status atual, role do usuário e pré-condições.

O workflow de unidade habitacional possui seis estados: DRAFT, PENDING_ANALYSIS, IN_REVIEW, APPROVED, REJECTED e REQUIRES_CHANGES. Transições são controladas por role - Técnico pode cadastrar e submeter, Fiscal pode aprovar ou rejeitar. Status APPROVED é final e irreversível.

O workflow de legitimação fundiária possui onze estados conforme Lei 13.465/2017, incluindo períodos de análise documental, parecer técnico, edital público e prazo para contestações.

Os SLAs definem prazos para cada etapa com alertas automáticos. Notificações são disparadas em mudanças de status relevantes.

## Regras

- **[unit-status-transitions.md](./unit-status-transitions.md)** - State machine de unidade com seis estados
- **[legitimation-status-transitions.md](./legitimation-status-transitions.md)** - State machine de legitimação com onze estados
- **[role-permissions.md](./role-permissions.md)** - Mapeamento de roles e permissões por transição
- **[sla-rules.md](./sla-rules.md)** - Prazos e alertas de SLA
- **[notification-triggers.md](./notification-triggers.md)** - Triggers de notificação por email

---

**Última atualização:** 2026-01-14
