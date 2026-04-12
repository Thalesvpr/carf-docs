# ADR: Ortofoto como Raiz Espacial — Inversão de Eixo do Domínio

> **Status**: PROPOSTA (pendente aprovação)
> **Data**: 2026-02-24
> **Impacto**: ALTO — muda a fundação do modelo de domínio em todos os sistemas

---

## 1. Contexto e Problema

### Modelo Atual (Region → Community → Orthophoto)

```
Tenant
  └─ Region (agrupamento operacional, optional)
       └─ Community (regionId nullable)
            └─ Orthophoto (communityId nullable, status: PENDING→PROCESSING→COMPLETED→FAILED)
                  ↑ associação manual via AssociateCommunityCommand
```

**O problema**: as 3 entidades são criadas independentemente, sem relação causal entre elas. Isso gera estados inconsistentes que são válidos no sistema mas inúteis na prática:

| Estado | Válido hoje? | Útil? |
|--------|:---:|:---:|
| Community sem Orthophoto | Sim | **Não** — sem base espacial, cadastrador não pode trabalhar |
| Region sem Community | Sim | **Não** — agrupamento vazio |
| Orthophoto sem Community | Sim | Talvez — enquanto está em pipeline, ok |
| Community com Orthophoto FAILED | Sim | **Não** — comunidade existe mas é inutilizável |
| Unit com CommunityId de community sem ortofoto | Sim | **Não** — unidade sem contexto espacial |

**Evidência no código atual:**

- `Community.cs:1-25` — nenhuma referência a Orthophoto, nenhuma invariante que exija base espacial
- `CreateCommunityCommand.cs:17-26` — cria Community com nome/tipo, sem nenhuma validação de ortofoto
- `ComunidadeCreatePage.tsx:21-27` — form com name, type, regionId, municipality — zero menção a ortofoto
- `Orthophoto.cs:8` — `CommunityId` é nullable, associação é post-hoc
- `AssociateCommunityCommand.cs:6-8` — comando separado para vincular ortofoto a community depois
- `UploadOrtofotoCommand.cs:31` — upload aceita `CommunityId` opcional no request
- `useCommunityStore.ts:13-18` (REURBCAD) — store seleciona community por id/name, sem checar se tem ortofoto

### Consequência Prática

O cadastrador chega em campo, seleciona uma comunidade no mapa, e **não tem base espacial**. O sistema permite isso. O fluxo inteiro quebra silenciosamente.

---

## 2. Decisão Proposta

### Modelo Novo (Orthophoto → OperationalArea)

```
Tenant
  └─ Orthophoto (raiz — ativo espacial primário)
       status: PENDING → PROCESSING → COMPLETED → FAILED
       └─ OperationalArea (UI: "Comunidade")
            orthophotoId: required (FK → orthophoto WHERE status = COMPLETED)
            nome, tipo, configurações, permissões
            └─ Units, Holders, Teams, Blocks, Lots...
```

**Region** vira tag/agrupamento opcional sobre OperationalAreas, sem FK hierárquica.

### Regras

1. **Ortofoto é a raiz**: primeiro existe o dado espacial validado
2. **OperationalArea só pode ser criada se existir pelo menos 1 Orthophoto com status COMPLETED** associada
3. **Community na UI continua se chamando "Comunidade"** — bounded context mapping (domínio ≠ UI)
4. **Region vira label/tag**, não entidade hierárquica pai

### Semântica

| Conceito | Antes | Depois |
|----------|-------|--------|
| Ortofoto | Anexo opcional de Community | **Ativo espacial primário, raiz do fluxo** |
| Comunidade | Entidade independente, criada livremente | **Configuração operacional sobre uma ortofoto validada** |
| Região | Nível hierárquico (Region → Community) | **Tag de agrupamento (flat, opcional)** |
| Unit.CommunityId | FK para entidade possivelmente vazia | FK para OperationalArea que **garante** base espacial |

---

## 3. Diagramas Comparativos

### Modelo Atual — Fluxo de Dados
```
[Admin cria Region] ──────────────────────────────────────┐
                                                           │ (opcional)
[Admin cria Community] ──── name, type, regionId? ────────│────► Community (vazia, sem mapa)
                                                           │
[Externo faz Upload Ortofoto] ── PENDING → PROCESSING ───│
                                                           │
[Job processa] ── COMPLETED ─────────────────────────── ???
                                                           │
[Admin associa manualmente] ── AssociateCommunityCommand ──┘

⚠ Gap temporal: Community existe sem ortofoto por tempo indefinido
⚠ Gap lógico: nada impede Unit ser criada em Community sem ortofoto
```

### Modelo Proposto — Fluxo de Dados
```
[Externo faz Upload Ortofoto] ── PENDING
         │
[Job processa] ── PROCESSING → COMPLETED ✓
         │
[Sistema emite evento: OrthophotoValidated]
         │
[Admin cria OperationalArea] ── name, type, orthophotoId (required, validated)
         │                       ⛔ Bloqueado se orthophoto.Status ≠ COMPLETED
         │
[OperationalArea ativa] ── pronta para Units, Teams, campo
         │
[Tag Region opcional] ── agrupamento flat por conveniência

✅ Nenhum estado morto: sem ortofoto validada → sem área operacional → sem cadastro
```

---

## 4. Mapeamento de Impacto — Arquivo por Arquivo

### 4.1 GEOAPI (Backend .NET)

#### DOMAIN (entidades + contratos)

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `DOMAIN/Entities/Community.cs` | **RENOMEAR → OperationalArea.cs** | Adicionar `Guid OrthophotoId` required, remover `RegionId?` nullable, adicionar invariante: só cria se ortofoto COMPLETED |
| `DOMAIN/Entities/Orthophoto.cs` | **MODIFICAR** | Remover `CommunityId?` nullable → inverter: OperationalArea aponta para Orthophoto. Adicionar navigation `ICollection<OperationalArea>` |
| `DOMAIN/Entities/Region.cs` | **SIMPLIFICAR** | Remover `ICollection<Community>` navigation. Virar tag flat. Considerar remover FK de Community → adicionar junction `OperationalAreaTag` ou campo `string[] Tags` |
| `DOMAIN/Entities/Unit.cs:11` | **MODIFICAR** | `CommunityId` → `OperationalAreaId` (mesmo conceito, novo nome) |
| `DOMAIN/Entities/CommunityAuthorization.cs` | **RENOMEAR** | → `OperationalAreaAuthorization.cs` |
| `DOMAIN/Entities/Team.cs` | **VERIFICAR** | Se tem referência a Community, atualizar para OperationalArea |
| `DOMAIN/Contracts/ICommunityRepository.cs` | **RENOMEAR** | → `IOperationalAreaRepository.cs` |
| `DOMAIN/Contracts/IOrtophotoRepository.cs` | **MODIFICAR** | Adicionar `GetCompletedByIdAsync()` para validação |
| `DOMAIN/Enums/CommunityType.cs` | **MANTER** | Tipos (URBANA, RURAL, etc.) continuam válidos |
| `DOMAIN/Enums/ProcessingStatus.cs` | **MANTER** | PENDING, PROCESSING, COMPLETED, FAILED |
| `DOMAIN/Enums/RegionScopeType.cs` | **AVALIAR** | Pode ser removido se Region virar tag simples |
| `DOMAIN/Events/` | **ADICIONAR** | `OrthophotoCompletedEvent` — dispara quando job finaliza com COMPLETED |

#### APPLICATION (commands + queries + DTOs + validators)

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `APPLICATION/Commands/Communities/CreateCommunityCommand.cs` | **REESCREVER** | → `CreateOperationalAreaCommand`: exigir `OrthophotoId`, validar status COMPLETED antes de criar |
| `APPLICATION/Commands/Communities/UpdateCommunityCommand.cs` | **RENOMEAR** | → `UpdateOperationalAreaCommand` |
| `APPLICATION/Commands/Orthofotos/AssociateCommunityCommand.cs` | **DELETAR** | Não faz mais sentido — relação é inversa agora |
| `APPLICATION/Commands/Orthofotos/UploadOrtofotoCommand.cs:31` | **MODIFICAR** | Remover `CommunityId` do request — ortofoto é independente até validação |
| `APPLICATION/Commands/Orthofotos/SubmitPix4dLinkCommand.cs` | **VERIFICAR** | Remover CommunityId se presente |
| `APPLICATION/Commands/Regions/CreateRegionCommand.cs` | **SIMPLIFICAR** | Se Region vira tag |
| `APPLICATION/Commands/Regions/UpdateRegionCommand.cs` | **SIMPLIFICAR** | Idem |
| `APPLICATION/Commands/Teams/AssignCommunityCommand.cs` | **RENOMEAR** | → `AssignOperationalAreaCommand` |
| `APPLICATION/Commands/Teams/UnassignCommunityCommand.cs` | **RENOMEAR** | → `UnassignOperationalAreaCommand` |
| `APPLICATION/Commands/Units/CreateUnitCommand.cs` | **MODIFICAR** | `CommunityId` → `OperationalAreaId` |
| `APPLICATION/Commands/UploadLinks/UploadViaLinkCommand.cs` | **VERIFICAR** | Se referencia CommunityId |
| `APPLICATION/DTOs/Communities/CommunityDto.cs` | **RENOMEAR** | → `OperationalAreaDto`, adicionar `orthophotoId`, `orthophotoStatus` |
| `APPLICATION/DTOs/Orthofotos/OrtofotoDto.cs` | **MODIFICAR** | Remover `CommunityId?` do DTO |
| `APPLICATION/DTOs/Orthofotos/AssociateCommunityRequest.cs` | **DELETAR** |  |
| `APPLICATION/DTOs/Orthofotos/UploadOrtofotoRequest.cs` | **MODIFICAR** | Remover CommunityId |
| `APPLICATION/DTOs/Regions/RegionDto.cs` | **SIMPLIFICAR** | Se Region vira tag |
| `APPLICATION/DTOs/Units/UnitDto.cs` | **MODIFICAR** | `CommunityId` → `OperationalAreaId` |
| `APPLICATION/DTOs/Units/CreateUnitRequest.cs` | **MODIFICAR** | Idem |
| `APPLICATION/DTOs/Teams/TeamDto.cs` | **VERIFICAR** | Se referencia communities |
| `APPLICATION/Queries/Communities/*` | **RENOMEAR** | Todos → OperationalArea |
| `APPLICATION/Queries/Orthofotos/*` | **MODIFICAR** | Remover filtros por CommunityId, adicionar campo `hasOperationalArea` |
| `APPLICATION/Queries/Regions/*` | **SIMPLIFICAR** | Se Region vira tag |
| `APPLICATION/Validators/CreateCommunityValidator.cs` | **REESCREVER** | → Validar OrthophotoId required, status COMPLETED |
| `APPLICATION/Validators/UpdateCommunityValidator.cs` | **RENOMEAR** | → UpdateOperationalAreaValidator |
| `APPLICATION/Validators/AssignCommunityValidator.cs` | **RENOMEAR** | → AssignOperationalAreaValidator |
| `APPLICATION/Validators/CreateUnitValidator.cs` | **MODIFICAR** | Validar OperationalAreaId em vez de CommunityId |
| `APPLICATION/Mappings/MappingProfile.cs` | **ATUALIZAR** | Todos os profiles Community → OperationalArea |
| `APPLICATION/Services/UserManagementAuthorizationHelper.cs` | **VERIFICAR** | Se referencia Communities |

#### INFRA (persistence + jobs + repositories)

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `INFRA/Persistence/CARFDbContext.cs` | **MODIFICAR** | `DbSet<Community>` → `DbSet<OperationalArea>`, atualizar OnModelCreating |
| `INFRA/Persistence/Configurations/CommunityConfiguration.cs` | **RENOMEAR + REESCREVER** | → OperationalAreaConfiguration: adicionar FK OrthophotoId required |
| `INFRA/Persistence/Configurations/OrthophotoConfiguration.cs` | **MODIFICAR** | Remover FK CommunityId, adicionar HasMany(OperationalAreas) |
| `INFRA/Persistence/Configurations/RegionConfiguration.cs` | **SIMPLIFICAR** | Se Region vira tag |
| `INFRA/Persistence/Configurations/UnitConfiguration.cs` | **MODIFICAR** | FK CommunityId → OperationalAreaId |
| `INFRA/Persistence/Configurations/TeamConfiguration.cs` | **VERIFICAR** | Se referencia Community |
| `INFRA/Repositories/CommunityRepository.cs` | **RENOMEAR** | → OperationalAreaRepository |
| `INFRA/Repositories/OrtophotoRepository.cs` | **MODIFICAR** | Remover lógica de CommunityId |
| `INFRA/Repositories/RegionRepository.cs` | **SIMPLIFICAR** | Se Region vira tag |
| `INFRA/Repositories/UnitRepository.cs` | **MODIFICAR** | Filtros CommunityId → OperationalAreaId |
| `INFRA/Repositories/TeamRepository.cs` | **VERIFICAR** | Se referencia Community |
| `INFRA/Jobs/ProcessOrtofotoJob.cs` | **ADICIONAR EVENTO** | Ao completar com COMPLETED, disparar `OrthophotoCompletedEvent` |
| `INFRA/DependencyInjection.cs` | **ATUALIZAR** | Registros de repos/services renomeados |
| `INFRA/Migrations/` | **NOVA MIGRATION** | Renomear tabela `communities` → `operational_areas`, adicionar `orthophoto_id NOT NULL`, remover `orthophotos.community_id` |

#### WEBAPI (controllers)

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `WEBAPI/Controllers/CommunitiesController.cs` | **RENOMEAR** | → OperationalAreasController (rota: `/api/operational-areas` ou manter `/api/communities` por compat) |
| `WEBAPI/Controllers/OrthofotosController.cs` | **MODIFICAR** | Remover endpoint `POST /{id}/associate-community` |
| `WEBAPI/Controllers/RegionsController.cs` | **SIMPLIFICAR** | Se Region vira tag |
| `WEBAPI/Controllers/UnitsController.cs` | **MODIFICAR** | Filtro communityId → operationalAreaId |
| `WEBAPI/Controllers/TeamsController.cs` | **VERIFICAR** | Se referencia communities |
| `WEBAPI/Controllers/UploadLinksController.cs` | **VERIFICAR** | Se referencia communities |

#### TESTS

| Arquivo | Ação |
|---------|------|
| `TESTS/Domain/Entities/CommunityTests.cs` | RENOMEAR + REESCREVER |
| `TESTS/Application/Commands/AssociateCommunityCommandTests.cs` | DELETAR |
| `TESTS/Application/Commands/AssignCommunityCommandTests.cs` | RENOMEAR |
| `TESTS/Application/Commands/UnassignCommunityCommandTests.cs` | RENOMEAR |
| `TESTS/Application/Commands/CreateUnitCommandTests.cs` | MODIFICAR |
| `TESTS/Application/Queries/ListCommunitiesQueryTests.cs` | RENOMEAR |
| `TESTS/Application/Queries/GetCommunityByIdQueryTests.cs` | RENOMEAR |
| `TESTS/Application/Validators/AssignCommunityValidatorTests.cs` | RENOMEAR |
| `TESTS/Presentation/Controllers/CommunitiesControllerTests.cs` | RENOMEAR |
| `TESTS/Presentation/Controllers/UnitsControllerTests.cs` | MODIFICAR |
| `TESTS.Integration/Repositories/CommunityRepositoryTests.cs` | RENOMEAR |
| `TESTS.Integration/Api/CommunitiesApiTests.cs` | RENOMEAR |
| `TESTS.Integration/Api/*` (vários) | VERIFICAR referências a community |

### 4.2 REURBWEB (Frontend React)

#### Source Code

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `src/entities/comunidade.ts` | **REESCREVER** | Interface `Community` → adicionar `orthophotoId: string`, `orthophotoStatus: string`. `CreateCommunityRequest` → exigir `orthophotoId` |
| `src/entities/ortofoto.ts` | **MODIFICAR** | Remover `communityId` e `AssociateCommunityRequest`. Ortofoto é independente |
| `src/entities/regiao.ts` | **SIMPLIFICAR** | Se Region vira tag |
| `src/features/comunidades/api/comunidadesApi.ts` | **MODIFICAR** | Endpoints atualizados |
| `src/features/comunidades/model/useComunidades.ts` | **MODIFICAR** | Hooks atualizados |
| `src/features/comunidades/ui/ComunidadeCreatePage.tsx` | **REESCREVER** | Exigir seleção de ortofoto validada (dropdown filtrado por status COMPLETED). Bloquear submit sem ortofoto |
| `src/features/comunidades/ui/ComunidadeEditPage.tsx` | **MODIFICAR** | Mostrar ortofoto associada, permitir trocar |
| `src/features/comunidades/ui/ComunidadesListPage.tsx` | **MODIFICAR** | Mostrar coluna de ortofoto/status na tabela |
| `src/features/ortofotos/api/ortofotosApi.ts` | **MODIFICAR** | Remover `associateCommunity()` |
| `src/features/ortofotos/model/useOrtofotos.ts` | **MODIFICAR** | Remover `useAssociateCommunity` mutation |
| `src/features/ortofotos/ui/OrtofotosPage.tsx` | **MODIFICAR** | Remover botão de associar community. Adicionar botão "Criar Área Operacional" (aparece só em COMPLETED) |
| `src/features/ortofotos/ui/OrtofotoDetailPage.tsx` | **MODIFICAR** | Idem |
| `src/features/regioes/` (todos) | **SIMPLIFICAR** | Se Region vira tag |
| `src/features/equipes/api/equipesApi.ts` | **VERIFICAR** | Se referencia communityId |
| `src/features/equipes/ui/EquipesPage.tsx` | **VERIFICAR** | Idem |
| `src/features/dashboard/ui/DashboardPage.tsx` | **VERIFICAR** | Se mostra métricas por community |
| `src/app/router/index.tsx` | **AVALIAR** | Rotas de comunidades/regiões podem mudar |
| `swagger.json` | **REGENERAR** | Após mudança no backend |

### 4.3 REURBCAD (Mobile React Native)

#### Source Code

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `src/stores/useCommunityStore.ts` | **MODIFICAR** | Adicionar `orthophotoId`, `orthophotoStatus` ao state. `setCommunity` recebe ortofoto info. Download tracking já está correto (linked to id) |
| `src/components/domain/map/RegionPicker.tsx` | **MODIFICAR** | Filtrar lista: só mostrar communities com orthophoto COMPLETED |
| `app/(tabs)/mapa.tsx` | **VERIFICAR** | Se usa communityId para filtrar units/layers |
| `app/(tabs)/regiao.tsx` | **SIMPLIFICAR** | Tab pode virar "Áreas" em vez de "Região" |
| `app/(modals)/nova-unidade.tsx` | **VERIFICAR** | Se herda communityId do store |
| `app/(modals)/quadra-editor.tsx` | **VERIFICAR** | Se usa community_id no blockStore |
| `app/(modals)/croqui.tsx` | **VERIFICAR** | Se referencia community |
| `app/(modals)/preparar-regiao.tsx` | **MODIFICAR** | "Preparar Região" → "Baixar Pacote da Área". Download da ortofoto fica mais semântico |
| `src/stores/useBlockStore.ts` | **MODIFICAR** | Se referencia community_id em blocks |
| `src/stores/useUnitDraftStore.ts` | **MODIFICAR** | `communityId` → `operationalAreaId` (ou manter nome mas garantir ortofoto) |
| `src/stores/useSavedUnitsStore.ts` | **VERIFICAR** | Se armazena communityId |
| `src/database/schema.ts` | **MODIFICAR** | Tabela `blocks` tem `community_id` → renomear ou manter compat |
| `src/database/models/Block.ts` | **MODIFICAR** | Campo community_id |
| `src/hooks/useMapPin.ts` | **VERIFICAR** | Se referencia community |
| `src/hooks/useMapClusters.ts` | **VERIFICAR** | Se filtra por community |
| `src/constants/strings.ts` | **MODIFICAR** | Textos de "comunidade" → manter na UI |
| `src/constants/routes.ts` | **VERIFICAR** | Se tem rota "regiao" que precisa mudar |
| `src/constants/navigation.ts` | **VERIFICAR** | Labels de tabs |
| `app/(tabs)/_layout.tsx` | **VERIFICAR** | Tab "regiao" label |

### 4.4 LIB (Shared Libraries)

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `LIB/TS/TSCORE/DOCS/API/02-types-entities.md` | **MODIFICAR** | Tipo Community ganha orthophotoId |
| `LIB/TS/TSCORE/DOCS/API/03-types-relationships.md` | **MODIFICAR** | Relação Ortofoto→Community inverte |
| `LIB/TS/TSCORE/DOCS/API/04-types-enums.md` | **VERIFICAR** | CommunityType, RegionScopeType |
| `LIB/TS/TSCORE/DOCS/CONCEPTS/03-typescript-types.md` | **MODIFICAR** | Types atualizados |
| `LIB/TS/GEOAPI-CLIENT/DOCS/API/03a-communities-crud-api.md` | **REESCREVER** | Create exige orthophotoId |
| `LIB/TS/GEOAPI-CLIENT/DOCS/API/03b-communities-stats-geo-api.md` | **MODIFICAR** |  |
| `LIB/TS/GEOAPI-CLIENT/DOCS/API/07-orthofotos-api.md` | **MODIFICAR** | Remover associate-community endpoint |
| `LIB/TS/GEOAPI-CLIENT/DOCS/API/09-packages-api.md` | **VERIFICAR** | Se referencia community |
| `LIB/TS/UI-NATIVE/DOCS/COMPONENTS/DOMAIN/04-community-card.md` | **MODIFICAR** | Card mostra ortofoto info |
| `LIB/TS/UI-NATIVE/DOCS/COMPONENTS/DOMAIN/05-map-component.md` | **VERIFICAR** | Se filtra por community |
| `LIB/TS/UI-COMPONENTS/DOCS/COMPONENTS/DOMAIN/04-community-card.md` | **MODIFICAR** | Idem web |

### 4.5 CENTRAL (Docs de Domínio)

| Arquivo | Ação | Detalhe |
|---------|------|---------|
| `CENTRAL/DOMAIN/CONCEPTS/04-community.md` | **REESCREVER** | Comunidade = config operacional sobre ortofoto validada |
| `CENTRAL/DOMAIN/CONCEPTS/07-tenant.md` | **VERIFICAR** | Se descreve hierarquia Tenant→Region→Community |
| `CENTRAL/DOMAIN/CONCEPTS/35-ortofoto.md` | **REESCREVER** | Ortofoto = raiz espacial primária do sistema |
| `CENTRAL/DOMAIN/CONCEPTS/36-bucket-tenant.md` | **VERIFICAR** | Estrutura S3 pode mudar |
| `CENTRAL/DOMAIN/CONCEPTS/39-regiao.md` | **REESCREVER** | Região = tag flat, não hierarquia |
| `CENTRAL/DOMAIN/CONCEPTS/22-survey-processing.md` | **VERIFICAR** | Se referencia community |
| `CENTRAL/WORKFLOW-MESTRE/README.md` | **MODIFICAR** | Fluxo mestre inverte ordem |
| `CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos/README.md` | **REESCREVER** | Entrega de ortofoto é PASSO 1, precede tudo |
| `CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos/passo-01-autenticacao.md` | **VERIFICAR** |  |
| `CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos/passo-02-upload.md` | **VERIFICAR** |  |
| `CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos/passo-03-processamento.md` | **MODIFICAR** | Adicionar: ao completar, emite evento que habilita criação de área |
| `CENTRAL/WORKFLOW-MESTRE/01-entrega-ortofotos/passo-04-armazenamento.md` | **VERIFICAR** |  |
| `CENTRAL/WORKFLOW-MESTRE/04-regras-inegociaveis/regras-ordem.md` | **REESCREVER** | Ordem: ortofoto → área operacional → campo |
| `CENTRAL/WORKFLOW-MESTRE/04-regras-inegociaveis/regras-ortofotos.md` | **REESCREVER** | Ortofoto é pré-requisito para área operacional |
| `CENTRAL/WORKFLOW-MESTRE/05-conceitos-glossario/conceitos-principais.md` | **MODIFICAR** | Glossário atualizado |
| `CENTRAL/WORKFLOW-MESTRE/05-conceitos-glossario/sistemas.md` | **VERIFICAR** |  |
| `CENTRAL/WORKFLOW-MESTRE/05-conceitos-glossario/atores.md` | **VERIFICAR** |  |
| `CENTRAL/ARCHITECTURE/DIAGRAMS/01-ecosystem.md` | **MODIFICAR** | Diagrama do ecossistema |
| `CENTRAL/ARCHITECTURE/DIAGRAMS/02-data-flow.md` | **MODIFICAR** | Fluxo de dados inverte |
| `CENTRAL/ARCHITECTURE/SYSTEM/01-geoapi.md` | **MODIFICAR** | Descrição das entidades |
| `CENTRAL/ARCHITECTURE/DECISIONS/04-backend-stack.md` | **VERIFICAR** | Se menciona hierarquia |

### 4.6 GEOAPI DOCS

| Arquivo | Ação |
|---------|------|
| `DOCS/ARCHITECTURE/LAYERS/DOMAIN/ENTITIES/COMMUNITIES/04-community.md` | REESCREVER |
| `DOCS/ARCHITECTURE/LAYERS/DOMAIN/ENTITIES/GIS/20-orthophoto.md` | REESCREVER |
| `DOCS/DOMAIN/AGGREGATES/02-community-aggregate.md` | REESCREVER |
| `DOCS/DOMAIN/RELATIONSHIPS/01-entity-relationships.md` | REESCREVER |
| `DOCS/DOMAIN/VALUE-OBJECTS/11-community-type.md` | VERIFICAR |
| `DOCS/FEATURES/03-community-management.md` | REESCREVER |
| `DOCS/FEATURES/08-orthophoto-management.md` | REESCREVER |
| `DOCS/ARCHITECTURE/LAYERS/APPLICATION/COMMANDS/03-community-commands.md` | REESCREVER |
| `DOCS/ARCHITECTURE/LAYERS/APPLICATION/COMMANDS/08-ortofoto-commands.md` | MODIFICAR |
| `DOCS/ARCHITECTURE/LAYERS/APPLICATION/QUERIES/03-community-queries.md` | RENOMEAR |
| `DOCS/ARCHITECTURE/LAYERS/APPLICATION/QUERIES/08-ortofoto-queries.md` | MODIFICAR |
| `DOCS/ARCHITECTURE/LAYERS/APPLICATION/DTOS/03-community-dtos.md` | REESCREVER |
| `DOCS/ARCHITECTURE/LAYERS/APPLICATION/DTOS/08-ortofoto-dtos.md` | MODIFICAR |
| `DOCS/ARCHITECTURE/LAYERS/APPLICATION/VALIDATORS/03-community-validators.md` | REESCREVER |
| `DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/03-communities-controller.md` | REESCREVER |
| `DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/08-orthofotos-controller.md` | MODIFICAR |
| `DOCS/ARCHITECTURE/LAYERS/PRESENTATION/CONTROLLERS/12-packages-controller.md` | VERIFICAR |
| `DOCS/ARCHITECTURE/LAYERS/INFRA/PERSISTENCE/02-database-schema.md` | REESCREVER relação |
| `DOCS/ARCHITECTURE/LAYERS/INFRA/JOBS/01-background-jobs.md` | MODIFICAR (evento) |
| `DOCS/ARCHITECTURE/LAYERS/INFRA/JOBS/02-ortofoto-processing-pipeline.md` | MODIFICAR (evento) |
| `DOCS/ARCHITECTURE/LAYERS/INFRA/STORAGE/01-file-storage.md` | VERIFICAR |
| `DOCS/ARCHITECTURE/LAYERS/DOMAIN/EVENTS/06-community-created-event.md` | RENOMEAR |
| `DOCS/ARCHITECTURE/LAYERS/DOMAIN/EVENTS/07-community-boundary-changed-event.md` | RENOMEAR |
| `DOCS/ARCHITECTURE/LAYERS/DOMAIN/EVENTS/11-community-archived-event.md` | RENOMEAR |
| `DOCS/PATTERNS/02-gis-spatial-patterns.md` | VERIFICAR |
| `DOCS/PATTERNS/07-frontend-patterns.md` | VERIFICAR |
| `DOCS/ARCHITECTURE/LAYERS/PRESENTATION/MIDDLEWARES/02-error-codes.md` | VERIFICAR |

### 4.7 KEYCLOAK DOCS

| Arquivo | Ação |
|---------|------|
| `PROJECTS/KEYCLOAK/DOCS/INTEGRATION/RBAC/01-roles-hierarchy.md` | VERIFICAR se permissões referenciam "community" |
| `PROJECTS/KEYCLOAK/DOCS/INTEGRATION/RBAC/03-permissions.md` | VERIFICAR idem |

### 4.8 USE CASES (todos os projetos)

| Arquivo | Ação |
|---------|------|
| `GEOAPI/USE-CASES/UC-P1-001-entregar-ortofoto/` | REESCREVER — ortofoto vira passo 1 do sistema inteiro |
| `GEOAPI/USE-CASES/UC-P1-002-processar-ortofoto/` | MODIFICAR — adicionar evento OrthophotoCompleted |
| `GEOAPI/USE-CASES/UC-P1-003-disponibilizar-ortofoto-tenant/` | REESCREVER — "disponibilizar" = criar OperationalArea |
| `GEOAPI/USE-CASES/README.md` | MODIFICAR — ordem dos UCs |
| `REURBCAD/USE-CASES/UC-P3-002-download-pacote-temporario/` | MODIFICAR — pacote = ortofoto + metadados da área |
| `REURBCAD/USE-CASES/UC-P3-003-selecionar-comunidade/` | MODIFICAR — seleção filtra por ortofoto COMPLETED |

---

## 5. Prompt/Plano para Atualizar Documentação

> **Use este prompt com um agente de documentação para aplicar as mudanças. Pode ser executado em paralelo por sistema.**

### Prompt Mestre

```
CONTEXTO:
O domínio CARF sofreu uma inversão de eixo fundamental conforme ADR em ADR-ORTOFOTO-COMO-RAIZ.md.

MUDANÇA PRINCIPAL:
- ANTES: Region → Community → Orthophoto (entidades independentes, associação manual)
- DEPOIS: Orthophoto (raiz) → OperationalArea (requer ortofoto validada). Region = tag flat opcional.

REGRAS PARA TODA ALTERAÇÃO:
1. "Comunidade" continua sendo o termo na UI/labels — o rename é no domínio técnico
2. OperationalArea SÓ pode existir se tiver orthophotoId apontando para Orthophoto com status COMPLETED
3. AssociateCommunityCommand é DELETADO — relação agora é OperationalArea que aponta para Orthophoto
4. Region perde hierarquia — vira tag/agrupamento flat
5. Todo arquivo que diz "community_id" em Orthophoto deve inverter para "orthophoto_id" em OperationalArea
6. Novos eventos: OrthophotoCompletedEvent (quando job termina com COMPLETED)
7. Status enum da Orthophoto NÃO muda (PENDING, PROCESSING, COMPLETED, FAILED)
8. Na UI mobile, RegionPicker só mostra áreas com ortofoto COMPLETED
9. CreateCommunity/OperationalArea DEVE validar que orthophoto.Status == COMPLETED

SEÇÕES A ATUALIZAR POR SISTEMA:
```

### Prompt GEOAPI-DOCS (30 docs)
```
Atualize os docs em PROJECTS/GEOAPI/DOCS/ conforme a seção 4.6 do ADR.
Para cada arquivo listado como REESCREVER: reescreva o conteúdo inteiro mantendo o formato
(frontmatter → descrição → tabela propriedades → relacionamentos → invariantes).
Para MODIFICAR: edite apenas as seções afetadas.
Para RENOMEAR: mude referências internas ao nome antigo.
Para DELETAR: remova o arquivo e referências a ele.
Mantenha status: review em todos.
```

### Prompt CENTRAL-DOCS (20 docs)
```
Atualize os docs em CENTRAL/ conforme seção 4.5 do ADR.
Foco: DOMAIN/CONCEPTS/ (04-community, 35-ortofoto, 39-regiao) e WORKFLOW-MESTRE/.
O workflow mestre deve refletir: ortofoto validada ANTES de qualquer coisa organizacional.
regras-ordem.md deve explicitar: "Sem ortofoto validada, nenhuma área operacional pode ser criada."
```

### Prompt REURBWEB-DOCS (2 docs)
```
Atualize os docs em PROJECTS/REURBWEB/DOCS/ conforme seção 4.2 do ADR.
Foco: features/04-gis-integration.md e qualquer referência a community que assume criação independente.
```

### Prompt REURBCAD-DOCS (7 docs)
```
Atualize os docs em PROJECTS/REURBCAD/DOCS/ conforme seção 4.3 do ADR.
Foco: CONCEPTS/05-map-integration.md, ARCHITECTURE/02-lib-integration.md, ARCHITECTURE/04-state-management.md.
Adicionar: RegionPicker filtra por ortofoto COMPLETED.
useCommunityStore passa a ter orthophotoId no state.
```

### Prompt LIB-DOCS (11 docs)
```
Atualize os docs em PROJECTS/LIB/ conforme seção 4.4 do ADR.
Foco: TSCORE types (Community ganha orthophotoId), GEOAPI-CLIENT APIs (communities endpoint exige orthophotoId,
orthofotos endpoint perde associate-community), UI-NATIVE (community-card mostra ortofoto).
```

### Prompt USE-CASES (6 docs)
```
Atualize os use cases conforme seção 4.8 do ADR.
UC-P1-001: ortofoto é o primeiro passo do sistema.
UC-P1-003: "disponibilizar ortofoto para tenant" = criar OperationalArea vinculada.
UC-P3-002: pacote de download = ortofoto + metadados da área.
UC-P3-003: seleção filtra por áreas com ortofoto COMPLETED.
```

---

## 6. Contagem de Impacto

| Sistema | Arquivos Código | Arquivos Docs | Total |
|---------|:-:|:-:|:-:|
| GEOAPI backend (.cs) | ~50 (rename/modify) | ~30 | ~80 |
| REURBWEB frontend (.ts/.tsx) | ~18 | ~2 | ~20 |
| REURBCAD mobile (.ts/.tsx) | ~20 | ~7 | ~27 |
| LIB shared | — | ~11 | ~11 |
| CENTRAL docs | — | ~20 | ~20 |
| USE-CASES | — | ~6 | ~6 |
| KEYCLOAK docs | — | ~2 | ~2 |
| **TOTAL** | **~88** | **~78** | **~166** |

---

## 7. Ordem de Execução Recomendada

```
FASE 1 — Domínio (1 sessão)
  └─ GEOAPI: Domain entities + enums + contracts + migration

FASE 2 — Application (1 sessão)
  └─ GEOAPI: Commands + Queries + DTOs + Validators + Mappings

FASE 3 — Infra + API (1 sessão)
  └─ GEOAPI: Repositories + Configurations + Controllers + DI + Jobs

FASE 4 — Frontends (paralelo)
  ├─ REURBWEB: entities + features + router
  └─ REURBCAD: stores + components + screens + database

FASE 5 — Libs (1 sessão)
  └─ TSCORE types + GEOAPI-CLIENT docs + UI components docs

FASE 6 — Documentação (paralelo, 6 agentes)
  ├─ GEOAPI DOCS
  ├─ CENTRAL DOCS
  ├─ REURBWEB DOCS
  ├─ REURBCAD DOCS
  ├─ LIB DOCS
  └─ USE-CASES
```

---

## 8. Riscos e Mitigações

| Risco | Mitigação |
|-------|-----------|
| Migration pesada (rename tabela + FK) | Fazer em transaction, testar em staging primeiro |
| Breaking change na API | Manter `/api/communities` como alias temporário → deprecate em 30 dias |
| Mobile com dados locais em community_id antigo | Migration no WatermelonDB: rename column ou manter compat |
| Ortofoto em PROCESSING quando admin quer criar área | UI mostra "Aguarde validação" com status em tempo real |
| Multiple ortofotos por área no futuro | Modelar 1:N desde já (OperationalArea tem FK, não Orthophoto) |

---

## 9. Alternativas Consideradas

### A) Manter modelo atual + adicionar validação soft
- Adicionar check no frontend: "warning: community sem ortofoto"
- **Rejeitado**: não elimina estados inválidos, apenas avisa. Cadastrador ainda pode chegar em campo sem base.

### B) Orthophoto embedded em Community (1:1 strict)
- Community TEM exatamente 1 Orthophoto, criados juntos
- **Rejeitado**: ortofoto pode ser re-uploadada, versionada, ter histórico. Embedding impede evolução.

### C) Modelo proposto (Orthophoto → OperationalArea)
- **Aceito**: elimina estados inválidos por design, permite evolução (múltiplas ortofotos, versionamento), semântica clara.
