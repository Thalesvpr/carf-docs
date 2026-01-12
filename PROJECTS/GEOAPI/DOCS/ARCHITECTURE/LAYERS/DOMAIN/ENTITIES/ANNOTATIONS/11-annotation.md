# Annotation

Entidade representando anotação observação vinculada polimorficamente qualquer entidade permitindo registro notas alertas problemas lembretes com rastreamento resolução prazos. Herda de BaseEntity fornecendo auditoria soft delete. Campos principais incluem EntityType indicando entidade anotada, EntityId Guid, AuthorId Guid FK Account autor, Content string texto markdown, AnnotationType (NOTE WARNING ISSUE REMINDER) determinando comportamento e Priority nullable obrigatório ISSUE REMINDER.

Campos resolução incluem IsResolved bool aplicável ISSUE se solucionado, ResolvedAt DateTime nullable quando resolvido, ResolvedBy Guid nullable Account resolveu e DueDate DateTime nullable obrigatório REMINDER prazo. Métodos incluem Resolve(accountId) marcando ISSUE resolvido validando tipo, Unresolve() reabrindo, UpdateContent(newContent) editando, IsOverdue() verificando REMINDER passou DueDate e Validate() garantindo campos obrigatórios preenchidos conforme Type.

Dispara AnnotationCreatedEvent ao criar, AnnotationResolvedEvent ao resolver ISSUE e AnnotationDueEvent quando REMINDER atinge prazo Hangfire scheduled job. Apresentado sidebars entidades agrupado Type, filtrado dashboards ISSUEs pendentes responsável e REMINDER vencidos notificações push garantindo follow-up pendências críticas.

---

**Última atualização:** 2026-01-12
