# TeamMember

Entidade representando relacionamento N:N entre Account e Team vinculando usuário equipe com papel específico data entrada permitindo organização equipes campo topografia análise. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem TeamId Guid FK para Team, AccountId Guid FK para Account, TeamRole LEADER ou MEMBER definindo responsabilidade, JoinedAt DateTime quando entrou, AddedBy Guid FK Account que adicionou e IsActive bool indicando membro ativo permitindo remoção lógica preservando histórico.

Métodos incluem PromoteToLeader() alterando Role LEADER validando equipe terá ao menos um líder, DemoteToMember() alterando MEMBER garantindo mantém LEADER ativo disparando exception se último, Deactivate() marcando IsActive false sem deletar preservando histórico participação e IsLeader() verificando Role LEADER para validações permissões.

Integra com Team através coleção Members permitindo Team.AddMember(accountId role) criando TeamMember e Team.RemoveMember(accountId) desativando, participa CommunityAuthorization onde autorizações Team propagam permissões todos Members ativos e suporta queries equipes usuário listando Teams das quais Account membro ativo com respectivos roles.

---

**Última atualização:** 2026-01-12
