# Team

Entidade aggregate root representando equipe trabalho agrupando usuários Account para atribuição acesso comunidades específicas permitindo organização equipes campo topografia análise controle granular permissões. Herda de BaseAggregateRoot suportando domain events TeamCreatedEvent TeamMemberAddedEvent TeamMemberRemovedEvent despachados após SaveChanges. Campos principais incluem Name string nome equipe, Description string nullable opcional e IsActive bool indicando equipe ativa.

Relacionamentos principais são coleção TeamMember relacionamento Account incluindo TeamRole LEADER ou MEMBER e JoinedAt timestamp entrada e CommunityAuthorization vinculando equipe inteira Community com permissões específicas CanEdit CanCreate CanRead.

Métodos negócio incluem AddMember(accountId role) validando account existe não duplicado, RemoveMember(accountId) mantendo ao menos um líder, PromoteToLeader(accountId) DemoteToMember(accountId) gerenciando papéis. Permite múltiplas equipes acessarem mesma comunidade, equipe acessar múltiplas comunidades e autorizações individuais Account sobrescreverem autorizações Team quando necessário suportando trabalho colaborativo isolamento contexto sincronização offline.

---

**Última atualização:** 2026-01-12
