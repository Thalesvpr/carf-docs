# BASE

Classes base abstratas fornecendo funcionalidade comum para todas entities do GEOAPI implementando padrões DDD e infraestrutura técnica compartilhada. BaseEntity fornece Id Guid gerado automaticamente garantindo identificadores únicos globalmente, timestamps CreatedAt/UpdatedAt rastreando criação e última modificação auditável, DeletedAt nullable implementando soft delete permitindo recuperação e compliance LGPD e RowVersion byte array para controle de concorrência otimista detectando conflitos simultâneos via EF Core. BaseAggregateRoot estende BaseEntity adicionando coleção privada DomainEvents e método AddDomainEvent() permitindo entities dispararem eventos de domínio (UnitCreatedEvent, HolderLinkedEvent) despachados após SaveChanges para workflows assíncronos, notificações e integração com outros bounded contexts mantendo aggregates desacoplados.

## Arquivos

- **[00-base-entity.md](./00-base-entity.md)** - Classe base todas entities com Id timestamps soft delete
- **[01-base-aggregate-root.md](./01-base-aggregate-root.md)** - Aggregate root com suporte domain events

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [00-base-entity](./00-base-entity.md) | BaseEntity |
| [01-base-aggregate-root](./01-base-aggregate-root.md) | BaseAggregateRoot |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
