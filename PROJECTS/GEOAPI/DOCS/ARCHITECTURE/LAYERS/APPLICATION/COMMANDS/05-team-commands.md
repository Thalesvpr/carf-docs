---
type: leaf
status: review
updated: 2026-02-08
---

# Team Commands

Os commands de equipes representam operacoes de escrita sobre as tabelas teams, team_members e community_authorizations. Os handlers coordenam validacoes de limite de membros, unicidade e autorizacoes por comunidade.

---

## CreateTeamCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Name | string | sim | Nome da equipe |
| Description | string | nao | Descricao opcional |

O handler cria a entidade Team no tenant do usuario autenticado. A equipe e criada vazia, sem membros. Retorna TeamDto com id gerado.

---

## AddMemberCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| TeamId | Guid | sim | Identificador da equipe |
| AccountId | Guid | sim | UUID do usuario no Keycloak |
| Role | string | sim | COORDINATOR ou CADASTRATOR |

O handler valida tres regras antes de adicionar o membro. Primeira, verifica que o par (TeamId, AccountId) nao existe em team_members para impedir duplicidade (constraint UNIQUE). Segunda, se o role e COORDINATOR, verifica que a equipe nao possui outro coordenador ativo (left_at IS NULL), limitando a 1 coordenador por equipe. Terceira, se o role e CADASTRATOR, verifica que a equipe nao excede 4 cadastradores ativos. Ao satisfazer todas as regras, cria o registro em team_members com joined_at como timestamp atual.

Erros possiveis: DUPLICATE para membro ja existente, MAX_COORDINATORS para limite de coordenadores, MAX_CADASTRATORS para limite de cadastradores.

---

## RemoveMemberCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| TeamId | Guid | sim | Identificador da equipe |
| AccountId | Guid | sim | UUID do usuario a remover |

O handler localiza o registro em team_members e preenche left_at com timestamp atual, mantendo o historico de participacao. O membro removido perde automaticamente acesso herdado as comunidades autorizadas da equipe.

---

## AuthorizeCommunityCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| TeamId | Guid | sim | Identificador da equipe |
| CommunityId | Guid | sim | Identificador da comunidade |
| PermissionLevel | string | sim | READ, WRITE ou ADMIN |

O handler cria registro em community_authorizations vinculando a equipe a comunidade com o nivel de permissao informado. A constraint XOR garante que exatamente um entre team_id e account_id esta preenchido. Emite AccessGrantedEvent com TeamId, CommunityId e PermissionLevel.
