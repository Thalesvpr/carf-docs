# CommunityAuthorization

Entidade representando autorização acesso Community específica concedida para Team inteiro ou Account individual com permissões granulares leitura criação edição permitindo controle fino quem pode trabalhar cada comunidade. Herda de BaseEntity fornecendo auditoria temporal. Campos principais incluem CommunityId Guid FK comunidade autorizada, TeamId Guid nullable FK se autorização equipe inteira, AccountId Guid nullable FK se autorização direta usuário individual, CanRead bool permissão leitura, CanCreate bool permissão criação e CanEdit bool permissão edição.

Campos controle incluem GrantedAt DateTime quando concedida, GrantedBy Guid FK Account que concedeu, ExpiresAt DateTime nullable expiração null se permanente e IsRevoked bool se revogada. Métodos incluem Revoke() desativando imediatamente, IsActive() verificando não expirou nem revogada, IsExpired() comparando Now ExpiresAt, IsForTeam()/IsForAccount() verificando tipo autorização e HasPermission(permission) verificando read/create/edit.

Regra negócio estabelece TeamId AccountId mutuamente exclusivos validado construtor lançando ValidationException se ambos null ou ambos preenchidos. Integra sincronização offline mobile baixando apenas comunidades autorizadas, suporta hierarquia permissões onde autorização individual Account sobrescreve Team permitindo exceções granulares e participa queries acesso validando permissão antes retornar dados executar operações CUD Unit Holder Document vinculados Community.

---

**Última atualização:** 2026-01-12
