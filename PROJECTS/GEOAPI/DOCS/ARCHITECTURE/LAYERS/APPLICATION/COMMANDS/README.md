# COMMANDS

Commands CQRS do GEOAPI representando intenções de alterar estado do sistema (writes), organizados por feature (Units, Holders, Communities, Teams, Legitimation, Surveying) e seguindo convenção de nomenclatura CreateXCommand/UpdateXCommand/DeleteXCommand. Cada command é record imutável contendo apenas dados necessários para operação validados por validator FluentValidation correspondente antes de execução pelo handler. Handlers implementam IRequestHandler<TCommand, Result<TResponse>> do MediatR, recebem command validado, coordenam operações de domínio delegando lógica para entities/aggregates, persistem via IUnitOfWork e retornam Result<T> indicando sucesso com dados ou erro com messages para tratamento explícito sem exceptions. Commands não acessam DbContext diretamente mas apenas via repositories garantindo que todas alterações passem por lógica de domínio encapsulada nas entidades, mantendo consistência e permitindo domain events serem disparados apropriadamente.

## Arquivos Principais (a criar)

**Units:**
- 01-create-unit-command.md
- 02-update-unit-command.md
- 03-delete-unit-command.md
- 04-change-unit-status-command.md

**Holders:**
- 05-create-holder-command.md
- 06-update-holder-command.md
- 07-link-holder-to-unit-command.md
- 08-unlink-holder-from-unit-command.md

**Communities:**
- 09-create-community-command.md
- 10-update-community-command.md

**Teams:**
- 11-create-team-command.md
- 12-add-team-member-command.md
- 13-remove-team-member-command.md

**Legitimation:**
- 14-create-legitimation-request-command.md
- 15-submit-legitimation-request-command.md
- 16-approve-legitimation-command.md
- 17-reject-legitimation-command.md

**Documents:**
- 18-upload-document-command.md
- 19-delete-document-command.md

---

**Última atualização:** 2026-01-12
