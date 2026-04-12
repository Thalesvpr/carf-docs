---
type: leaf
status: review
updated: 2026-02-08
---

# Team DTOs

Os Data Transfer Objects de equipes definem os contratos de saida da API para operacoes sobre teams, team_members e metricas de produtividade.

## DTOs de Resposta

TeamDto e o DTO resumido para listagens.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| Id | Guid | Identificador unico |
| Name | string | Nome da equipe |
| Description | string | Descricao (nullable) |
| MembersCount | int | Total de membros ativos |
| CommunitiesCount | int | Total de comunidades autorizadas |
| CreatedAt | DateTime | Data de criacao |

TeamDetailDto estende TeamDto adicionando Members (lista de TeamMemberDto).

TeamMemberDto contem AccountId (Guid), Name (string), Role (COORDINATOR ou CADASTRATOR) e JoinedAt (DateTime).

## DTOs de Metricas

TeamMetricsDto e o DTO retornado pelo endpoint de metricas.

| Propriedade | Tipo | Descricao |
|-------------|------|-----------|
| TotalUnits | int | Total de unidades cadastradas no periodo |
| ByStatus | object | Contagem por attendance_status |
| ByMember | lista de MemberMetricDto | Producao por membro |
| DailyProgress | lista de DailyProgressDto | Evolucao diaria |

MemberMetricDto contem MemberId (Guid), MemberName (string), UnitsCount (int) e CompletionPercentage (decimal).

DailyProgressDto contem Date (DateTime) e Count (int).
