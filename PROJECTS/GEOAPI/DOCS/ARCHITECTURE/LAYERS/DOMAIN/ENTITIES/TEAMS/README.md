# TEAMS

Entities gerenciamento equipes técnicas campo do GEOAPI organizando field agents e autorizando acesso comunidades específicas. Team representa grupo profissionais com Name identificador, LeaderId AccountId do líder responsável coordenação, Description opcional e IsActive status operacional, agregando collection TeamMembers relacionamento N:N entre Team e Account especificando role membro (LEADER/MEMBER/OBSERVER) e DateJoined/DateLeft rastreando histórico participação permitindo reconstituir composição passada para auditoria. CommunityAuthorization junction entity concedendo Team permissão trabalhar Community específica com GrantedAt timestamp e GrantedBy AccountId auditando quem autorizou quando, prevenindo equipes acessarem dados comunidades não atribuídas através authorization policy verificando CommunityAuthorizations antes permitir operações criar/editar Units dentro Community garantindo segregação dados nível mais granular que tenant.

## Arquivos

- **[05-team.md](./05-team.md)** - Equipe técnica field agents com líder
- **[18-team-member.md](./18-team-member.md)** - Membro equipe relacionamento Team Account
- **[19-community-authorization.md](./19-community-authorization.md)** - Autorização team acessar community específica

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (3 arquivos)

| ID | Titulo |
|:---|:-------|
| [05-team](./05-team.md) | Team |
| [18-team-member](./18-team-member.md) | TeamMember |
| [19-community-authorization](./19-community-authorization.md) | CommunityAuthorization |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
