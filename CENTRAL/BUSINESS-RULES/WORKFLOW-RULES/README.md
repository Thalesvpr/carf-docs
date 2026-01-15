# WORKFLOW-RULES

Regras de workflow do CARF governando transições de status através de state machines que definem quais mudanças são permitidas baseadas no status atual, role do usuário e pré-condições.

O workflow de unidade habitacional possui seis estados: DRAFT, PENDING_ANALYSIS, IN_REVIEW, APPROVED, REJECTED e REQUIRES_CHANGES. Transições são controladas por role - Técnico pode cadastrar e submeter, Fiscal pode aprovar ou rejeitar. Status APPROVED é final e irreversível.

O workflow de legitimação fundiária possui onze estados conforme Lei 13.465/2017, incluindo períodos de análise documental, parecer técnico, edital público e prazo para contestações.

Os SLAs definem prazos para cada etapa com alertas automáticos. Notificações são disparadas em mudanças de status relevantes.


---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: O ramo completo ta sem numeração.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (5 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-unit-status-transitions](./01-unit-status-transitions.md) | Unit Status Transitions |
| [02-legitimation-status-transitions](./02-legitimation-status-transitions.md) | Legitimation Status Transitions |
| [03-role-permissions](./03-role-permissions.md) | Role Permissions Matrix |
| [04-sla-rules](./04-sla-rules.md) | SLA Rules |
| [05-notification-triggers](./05-notification-triggers.md) | Notification Triggers (Gatilhos de Notificação) |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
