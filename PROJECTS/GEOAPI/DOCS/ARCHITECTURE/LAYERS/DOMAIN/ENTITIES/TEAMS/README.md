---
type: readme
status: review
updated: 2026-01-12
---

# TEAMS

Entities gerenciamento equipes técnicas campo do GEOAPI organizando field agents e autorizando acesso comunidades específicas. Team representa grupo profissionais com Name identificador, LeaderId AccountId do líder responsável coordenação, Description opcional e IsActive status operacional, agregando collection TeamMembers relacionamento N:N entre Team e Account especificando role membro (LEADER/MEMBER/OBSERVER) e DateJoined/DateLeft rastreando histórico participação permitindo reconstituir composição passada para auditoria. CommunityAuthorization junction entity concedendo Team permissão trabalhar Community específica com GrantedAt timestamp e GrantedBy AccountId auditando quem autorizou quando, prevenindo equipes acessarem dados comunidades não atribuídas através authorization policy verificando CommunityAuthorizations antes permitir operações criar/editar Units dentro Community garantindo segregação dados nível mais granular que tenant.

## Arquivos

- **[05-team.md](./05-team.md)** - Equipe técnica field agents com líder
- **[18-team-member.md](./18-team-member.md)** - Membro equipe relacionamento Team Account
- **[19-community-authorization.md](./19-community-authorization.md)** - Autorização team acessar community específica

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (3)

| Documento | Status |
|-----------|--------|
| [Team](./05-team.md) | ⚠ |
| [TeamMember](./18-team-member.md) | ⚠ |
| [CommunityAuthorization](./19-community-authorization.md) | ⚠ |

<!-- CARF-INDEX-END -->
