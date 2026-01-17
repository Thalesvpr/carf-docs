# CQRS

Command Query Responsibility Segregation separa operações write (commands modificando estado) de read (queries consultando dados) permitindo otimizações independentes. Commands representam intenções negócio (CreateUnitCommand, LinkHolderCommand, ApproveUnitCommand) validados por FluentValidation, processados por handlers retornando Unit/Result sem dados completos, disparam domain events após SaveChanges, executam em transações garantindo atomicidade, e invalidam cache após sucesso. Queries retornam DTOs flat (UnitDetailDto, UnitListItemDto) otimizados para UI sem lazy loading, permitem projeções EF Select minimizando dados trafegados, habilitam cache agressivo Redis (TTL 5min queries estáticas, 30s queries dinâmicas), suportam paginação cursor-based para datasets grandes, e nunca modificam estado sendo seguras idempotentes. Write model usa aggregates fortes (Unit aggregate root coordenando UnitHolders), valida invariantes negócio, aplica event sourcing parcial (audit log eventos importantes), e escala verticalmente (transações ACID PostgreSQL). Read model desnormaliza joins frequentes, cria views materialized para dashboards complexos, replica para read replicas reduzindo carga master, e escala horizontalmente cache distribuído. MediatR desacopla controllers de handlers permitindo trocar implementação, adicionar behaviors pipeline (logging, caching, retry), e testar use cases isoladamente mockando dependencies.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
