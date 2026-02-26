---
type: leaf
status: review
updated: 2026-02-08
---

# Team Management - Gestao de Equipes

Feature de gestao de equipes implementada como visualizacao **readonly** no mobile, permitindo field collectors consultarem equipes tecnicas atribuidas, verificarem membros e lider, e identificarem comunidades de responsabilidade, facilitando coordenacao do trabalho de campo.

## Visao Geral

Equipes sao gerenciadas exclusivamente via interfaces web (ADMIN ou REURBWEB) e sincronizadas unidirecionalmente (server -> mobile). O app mobile permite apenas consulta e filtragem, sem operacoes de escrita.

## Telas

### TeamsListScreen

`FlatList` exibindo teams sincronizadas do GEOAPI backend:

| Informacao | Descricao |
|------------|-----------|
| Nome | Nome da equipe |
| Lider | Nome do lider da equipe |
| Membros | Count de membros |
| Status | Ativa / Inativa |

### TeamDetailsScreen

Informacoes completas da team com navegacao por tabs:

#### Tab Membros (`TeamMembersTab`)

`FlatList` de membros com:

| Campo | Descricao |
|-------|-----------|
| Avatar | Foto do membro |
| Nome | Nome completo |
| Role | `COORDINATOR`, `ANALYST`, `FIELD_COORDINATOR`, `FIELD_CADASTRATOR` |
| Telefone | Contato direto |
| Email | Email para coordenacao |

Facilita contato e coordenacao de campo.

#### Tab Comunidades (`TeamCommunitiesTab`)

Lista communities assigned a team com:

| Campo | Descricao |
|-------|-----------|
| Nome | Nome da comunidade |
| Endereco | Localizacao |
| Bounding box | Area geografica |
| Map preview | Thumbnail do mapa |

Permite field collector identificar areas de responsabilidade da equipe.

#### Tab Atividades

Historico de coletas realizadas pela equipe.

### Componentes

| Componente | Descricao |
|------------|-----------|
| `TeamCard` | Badge status, nome, lider, thumbnail photos membros, count comunidades atribuidas, action view details |
| `MyTeamsFilter` | Dropdown permitindo user filtrar units/coletas por team assignment, mostrando apenas dados relevantes da equipe atual, reduzindo clutter e facilitando foco no trabalho atribuido |

## Padrao Readonly

Validacoes de CRUD nao se aplicam pois a feature e **readonly** no mobile. Teams sao gerenciadas via ADMIN ou REURBWEB web interfaces e sincronizadas down para o mobile app.

### Validacoes de Sync

| Validacao | Descricao |
|-----------|-----------|
| **Data Integrity** | Verifica teams data integrity durante pull, checando required fields (`name`, `leader_id`, `status`) presentes. Rejeita incomplete records, logging errors no sync log |
| **Relationship Integrity** | Valida `leader_id` e member `user_ids` existem localmente na WatermelonDB `users` collection antes de renderizar. Mostra placeholder "Unknown User" se user deletado no server e nao sincronizado localmente |

## Roles e Acesso

| Role | Acesso Teams | Menu Mobile | Descricao |
|------|-------------|-------------|-----------|
| `FIELD_CADASTRATOR` | Nao | Apenas mapa e formularios (sem menu) | Acesso restrito a coleta |
| `FIELD_COORDINATOR` | Sim (equipes que pertence) | Menu mobile completo | Coordenador de campo |
| `ANALYST` | Sim (todas do tenant) | Menu mobile completo | Analista |
| `MANAGER` | Sim (todas do tenant) | Menu mobile completo | Gestor |

## Sync Unidirecional (Server -> Mobile)

### Pull de Teams

- `GET /api/teams` com params `tenant_id`, `user_id`
- Retorna apenas teams onde user e member ou leader (filtragem server-side conforme permissions e backend RLS policies)
- Armazena localmente na WatermelonDB `teams` collection

### Pull de Membros

- `GET /api/teams/:id/members`
- Retorna array de user objects com `role` field
- Armazena localmente via junction `team_members`

### Pull de Comunidades

- `GET /api/teams/:id/communities`
- Retorna community objects com geolocation e boundaries
- Armazena localmente via junction `team_communities`

### Estrategia de Cache

- Teams data cached **indefinitely** localmente ate explicit refresh
- Manual pull: user inicia refresh
- Background sync: periodic attempt
- Updates do server refletidos localmente apos sync, detectando changes via `updated_at` timestamp (incremental pull apenas modified teams desde last sync)

## Filtragem por Team

Query WatermelonDB `units` collection `WHERE team_id = $selectedTeamId`, mostrando apenas units relevantes ao contexto da team atual.

Util para field collectors trabalhando em multiplas teams em diferentes dias da semana, permitindo switching do team filter conforme schedule.

## Domain Model WatermelonDB

Mapeamento da CENTRAL Team entity para WatermelonDB `@model` class `Team`:

| Campo | Tipo | Decorador | Descricao |
|-------|------|-----------|-----------|
| `name` | string | `@field` | Nome da equipe |
| `description` | string (nullable) | `@field` | Descricao da equipe |
| `leader_id` | foreign key | `@relation('leader', 'leader_id')` | Many-to-one users (lider) |
| `status` | enum (`ACTIVE`, `INACTIVE`) | `@field` | Status da equipe |
| `created_at` | Date | `@date` | Timestamp criacao |
| `updated_at` | Date | `@date` | Timestamp atualizacao |

### Relacionamentos

| Relacao | Tipo | Decorador | Escrita | Descricao |
|---------|------|-----------|---------|-----------|
| `members` | many-to-many | via junction `team_members` | readonly (writable false) | Membros da equipe |
| `communities` | many-to-many | via junction `team_communities` | readonly | Comunidades atribuidas |

## Requisitos Funcionais Implementados

Implementacao dos requisitos de visualizacao de equipes:

- Consultar teams atribuidas ao field collector
- Visualizar membros e lider da equipe
- Identificar comunidades de responsabilidade
- Filtrar units por team assignment
- Coordenar trabalho verificando assignments de colegas
- Contactar lider para duvidas e issues de campo
- Sync unidirecional server -> mobile (sem push de teams changes, pois modificacoes sao gerenciadas via web interfaces ADMIN/REURBWEB)

Rastreando requisitos: **RF-024**, **RF-026** (consulta equipes, coordenacao trabalho campo, accountability, rastreamento atribuicoes).

## Referencias

- [Offline Sync](./03-offline-sync.md)
- [GEOAPI Team Management](../../../GEOAPI/DOCS/FEATURES/05-team-management.md)
- [GEOAPI Team Commands](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/APPLICATION/COMMANDS/05-team-commands.md)
- [Team Role Enum](../../../GEOAPI/DOCS/ARCHITECTURE/LAYERS/DOMAIN/VALUE-OBJECTS/ENUMS/10-team-role.md)
- [Role Permissions](../../../../CENTRAL/DOMAIN-RULES/WORKFLOWS/03-role-permissions.md)
