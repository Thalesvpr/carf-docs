---
type: leaf
status: review
updated: 2026-02-08
---

# Team Queries

As queries de equipes implementam o lado de leitura do CQRS para as tabelas teams, team_members e community_authorizations, incluindo metricas de produtividade agregadas.

## ListTeamsQuery

Retorna lista de TeamDto para o tenant do usuario autenticado, incluindo id, name, description, membersCount (contagem de membros ativos com left_at IS NULL) e communitiesCount (contagem de comunidades autorizadas). Nao aceita paginacao pois o volume de equipes por tenant e baixo.

## GetTeamByIdQuery

Recebe TeamId como Guid. O handler carrega a equipe com eager loading de team_members ativos (left_at IS NULL) e retorna TeamDetailDto incluindo lista de membros com account_id, role e joined_at. Retorna 404 se nao encontrada.

## GetTeamMetricsQuery

| Parametro | Tipo | Padrao | Descricao |
|-----------|------|--------|-----------|
| TeamId | Guid | obrigatorio | Identificador da equipe |
| Period | string | WEEK | TODAY, WEEK, MONTH ou ALL |

O handler agrega dados de unidades criadas pelos membros da equipe no periodo solicitado. Retorna objeto com totalUnits (total cadastradas), byStatus (contagem por attendance_status), byMember (array com memberId, memberName, unitsCount e completionPercentage) e dailyProgress (array com date e count para grafico de evolucao).

## GetTeamCommunitiesQuery

Recebe TeamId como Guid. O handler consulta community_authorizations filtrando por team_id e retorna array de CommunityListItemDto com id, code, name, communityType e permissionLevel. Acessivel por qualquer membro ativo da equipe.
