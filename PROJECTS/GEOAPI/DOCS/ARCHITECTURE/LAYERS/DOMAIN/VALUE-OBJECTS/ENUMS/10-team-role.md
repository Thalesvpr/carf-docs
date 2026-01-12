# TeamRole

Value object enum representando papel de um membro dentro de uma equipe de trabalho, controlando permissões e responsabilidades dentro do contexto da Team. Valores possíveis são LEADER (líder da equipe com permissões para adicionar/remover membros, promover/rebaixar outros, e gerenciar autorizações de acesso a comunidades) e MEMBER (membro regular que herda autorizações de acesso da equipe mas não pode gerenciar a equipe).

Métodos incluem CanManageTeam() retornando true apenas para LEADER, CanPromote() verificando se pode promover outros membros, CanRemoveMembers() verificando permissão de remoção, e ToDisplayString() retornando nome amigável para UI.

Usado em TeamMember.Role para definir papel de cada Account dentro da Team, validado em métodos de negócio como Team.AddMember() que permite apenas LEADER adicionar novos membros, Team.PromoteToLeader() garantindo que apenas LEADER pode promover outros, e Team.RemoveMember() impedindo remoção do último LEADER. Integra com CommunityAuthorization onde LEADER pode conceder acesso para a equipe inteira.

---

**Última atualização:** 2026-01-12
