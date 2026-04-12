---
type: leaf
status: review
updated: 2026-02-08
---

# Teams API - Gerenciamento de Equipes

A Teams API fornece operacoes para consulta de equipes de campo, metricas de produtividade e comunidades autorizadas. Acessada via propriedade teams da instancia GeoApiClient. Tipos Team, TeamMember e TeamRole importados de @carf/tscore/types. Endpoints conforme [API Reference](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/00-api-reference.md).

## Endpoints

| Metodo HTTP | Rota | Descricao | Sucesso | Erros | Roles |
|:------------|:-----|:----------|:--------|:------|:------|
| GET | /api/teams | Listar equipes do tenant | 200 | - | manager+ |
| GET | /api/teams/{id} | Obter equipe com membros | 200 | 404 | manager+, coordinator (propria equipe) |
| GET | /api/teams/{id}/metrics | Metricas de produtividade | 200 | 404 | manager+, coordinator (propria equipe) |
| GET | /api/teams/{id}/communities | Comunidades autorizadas | 200 | 404 | todos da equipe |

## list (GET /api/teams)

Lista equipes do tenant. Restrito a roles manager ou superior. Retorna PaginatedResponse de Team com paginacao padrao (page, limit).

## getById (GET /api/teams/{id})

Busca equipe por ID incluindo membros. Aceita id string. Retorna Team com array de TeamMember populado, cada membro contendo accountId, role (COORDINATOR ou CADASTRATOR), joinedAt e leftAt. Acessivel por managers e pelo coordinator da propria equipe. Lanca NotFoundError 404 se nao existir.

## getMetrics (GET /api/teams/{id}/metrics)

Obtem metricas de produtividade da equipe. Aceita teamId string e query param period como enum (TODAY, WEEK, MONTH, ALL) com default WEEK. Acessivel por managers e pelo coordinator da propria equipe.

Response retorna TeamMetrics:

| Campo | Tipo TS | Descricao |
|:------|:--------|:----------|
| totalUnits | number | Total de unidades cadastradas pela equipe no periodo |
| byStatus | objeto | Contagem por cada attendanceStatus (AUSENTE, PRESENTE, NAO_QUIS, ASSINADO) |
| byMember | array de MemberMetric | Metricas individuais por membro |
| dailyProgress | array de DailyCount | Dados para grafico de evolucao diaria |

Cada MemberMetric contem memberId (string), memberName (string), unitsCount (number) e completionPercentage (number de 0 a 100). Cada DailyCount contem date (string ISO 8601) e count (number).

## getCommunities (GET /api/teams/{id}/communities)

Lista comunidades para as quais a equipe tem autorizacao conforme CommunityAuthorization. Aceita teamId string. Retorna array de CommunityListItemDto contendo id, code, name, communityType e permissionLevel (READ, WRITE ou ADMIN). Acessivel por todos os membros da equipe. Usado pelo REURBCAD para determinar quais comunidades o usuario pode acessar no mapa e na sincronizacao.
