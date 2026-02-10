---
type: leaf
status: review
updated: 2026-02-08
---

# Teams Controller

O TeamsController gerencia consulta de equipes de campo, seus membros, metricas de produtividade e comunidades autorizadas. A rota base e /api/teams. Os endpoints de listagem e metricas sao restritos a roles manager ou superior, com excecao de coordenadores que podem consultar dados da propria equipe.

## Endpoints

| Metodo | Rota | Descricao | Sucesso | Erros | Roles |
|--------|------|-----------|---------|-------|-------|
| GET | /api/teams | Listar equipes do tenant | 200 | - | manager+ |
| GET | /api/teams/{id} | Obter equipe com membros | 200 | 404 | manager+, coordinator (propria) |
| GET | /api/teams/{id}/metrics | Metricas de produtividade | 200 | 404 | manager+, coordinator (propria) |
| GET | /api/teams/{id}/communities | Comunidades autorizadas | 200 | 404 | todos da equipe |

## Comportamento

O endpoint de listagem despacha ListTeamsQuery e retorna array de TeamDto com membros resumidos, filtrado por tenant via RLS. O endpoint de detalhes despacha GetTeamByIdQuery com eager loading de membros e retorna TeamDetailDto incluindo lista de team_members com account_id, role e joined_at. O endpoint de metricas aceita query param period (TODAY, WEEK, MONTH, ALL com default WEEK) e retorna objeto com totalUnits, byStatus (contagem por attendance_status), byMember (array com memberId, memberName, unitsCount, completionPercentage) e dailyProgress (array com date e count para grafico). O endpoint de comunidades retorna array de CommunityListItemDto contendo apenas comunidades para as quais a equipe tem autorizacao registrada em community_authorizations.

## Autorizacao

Listagem de equipes requer role manager, admin ou super-admin. Detalhes e metricas sao acessiveis por manager ou superior, alem de coordenadores da propria equipe validados via verificacao programatica no handler. Comunidades autorizadas sao acessiveis por qualquer membro ativo da equipe.
