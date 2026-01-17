# AnnotationType

Value object enum representando tipo de anotação que pode ser criada em qualquer entidade do sistema, determinando comportamento, campos obrigatórios e apresentação visual na interface. Valores possíveis são NOTE (observação geral informativa sem necessidade de ação ou prazo), WARNING (alerta importante destacando atenção necessária mas sem bloquear processos), ISSUE (problema identificado que requer resolução com rastreamento via IsResolved/ResolvedAt/ResolvedBy), e REMINDER (lembrete com prazo obrigatório via DueDate para ações futuras).

Métodos incluem RequiresPriority() retornando true para ISSUE e REMINDER que exigem campo Priority, RequiresDueDate() retornando true apenas para REMINDER, RequiresResolution() retornando true para ISSUE que deve ser marcado como resolvido, GetIcon() retornando ícone para UI (NOTE: info, WARNING: exclamation, ISSUE: bug, REMINDER: clock), e ToDisplayString() retornando nome amigável.

Usado em Annotation.Type controlando validações e comportamento, dispara notificações diferentes (WARNING: in-app, ISSUE: email para responsável, REMINDER: push notification no DueDate), apresenta em dashboards agrupando por tipo, e integra com workflow onde ISSUE em Unit bloqueia aprovação até resolução e REMINDER vencido aparece em lista de pendências do usuário.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
