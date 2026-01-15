# BaseAggregateRoot

Classe base que estende BaseEntity adicionando suporte Domain Events seguindo padrão DDD aggregate roots usado por entidades raiz agregados coordenando mudanças em seu grafo objetos (Unit, Community, Team, LegitimationRequest). Além herdar todos campos métodos BaseEntity (Id timestamps soft delete concorrência otimista), adiciona lista interna eventos domínio pendentes e métodos gerenciá-los.

Método AddDomainEvent(event) adiciona domain event lista eventos pendentes despachados após persistência, propriedade DomainEvents expõe lista read-only para Infrastructure processar e ClearDomainEvents() limpa lista após dispatch. Eventos despachados pelo Infrastructure após SaveChanges bem-sucedido garantindo consistência transacional via IDomainEventDispatcher, permitindo agregados notificarem mudanças significativas (UnitCreatedEvent, HolderLinkedEvent, TeamMemberAddedEvent) para handlers processarem assíncronamente notificações invalidação cache jobs background integração sistemas externos sem acoplar domínio preocupações infraestrutura.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
