---
type: leaf
status: review
updated: 2026-02-08
---

# Convencoes de Nomenclatura

Padroes de nomenclatura adotados em todo o projeto GEOAPI para garantir consistencia entre camadas, equipes e documentacao.

## Tabela Geral de Convencoes

| Tipo | Convencao | Exemplo | Anti-Pattern |
|------|-----------|---------|-------------|
| Entity | PascalCase singular | Unit, Holder, Community | Units, unit |
| Value Object | PascalCase | CPF, GeoPolygon, Email | CpfVO, Cpf_Value |
| Command | VerbNounCommand | CreateUnitCommand, LinkHolderCommand | UnitCreate, CreateUnit |
| Query | GetNoun(s)Query | GetUnitByIdQuery, ListUnitsQuery | UnitQuery, FetchUnit |
| Handler | CommandName + Handler | CreateUnitHandler | CreateUnitCommandHandler (redundante) |
| DTO | NounDto / NounRequest / NounResponse | UnitDto, CreateUnitRequest | UnitModel, UnitVM |
| Validator | NounValidator | CreateUnitValidator | CreateUnitCommandValidator |
| Repository Interface | INounRepository | IUnitRepository | IUnitsRepo |
| Repository Impl | NounRepository | UnitRepository | UnitsRepository |
| Controller | NounsController (plural) | UnitsController | UnitController |
| DB Table | snake_case plural | units, unit_holders | Units, unitHolder |
| DB Column | snake_case | tenant_id, created_at | TenantId, createdAt |
| Domain Event | NounVerbedEvent | UnitCreatedEvent | CreateUnitEvent |
| Exception | NounException | DomainException | DomainError |
| Configuration | NounConfiguration | UnitConfiguration | UnitMap |
| Migration | YYYYMMDD_Description | 20240315_AddHolderPhone | Migration1 |

## Nomenclatura de Arquivos

| Contexto | Convencao | Exemplo |
|----------|-----------|---------|
| Arquivo C# | PascalCase.cs | UnitRepository.cs, CreateUnitCommand.cs |
| Interface C# | IPascalCase.cs | IUnitRepository.cs, ICacheService.cs |
| Arquivo de documentacao | kebab-case.md | 01-unit-aggregate.md, 03-data-flow.md |
| Script SQL | kebab-case.sql | seed-dev-data.sql |
| Arquivo de configuracao | kebab-case ou PascalCase | docker-compose.yml, Directory.Build.props |
| Variavel de ambiente | SCREAMING_SNAKE_CASE | DATABASE_CONNECTION_STRING |
| Arquivo Kubernetes | kebab-case.yaml | geoapi-deployment.yaml |

## Nomenclatura de Namespaces

O namespace segue exatamente a estrutura de pastas do projeto:

| Camada | Padrao de Namespace | Exemplo |
|--------|-------------------|---------|
| Domain | Carf.GeoApi.Domain.{Subpasta} | Carf.GeoApi.Domain.Entities.Units |
| Application | Carf.GeoApi.Application.{Subpasta} | Carf.GeoApi.Application.Commands.Units |
| Infrastructure | Carf.GeoApi.Infrastructure.{Subpasta} | Carf.GeoApi.Infrastructure.Repositories |
| Gateway | Carf.GeoApi.Gateway.{Subpasta} | Carf.GeoApi.Gateway.Controllers |

## Nomenclatura de Commands e Queries (CQRS)

### Commands (Escrita)

| Operacao | Padrao | Exemplo Completo |
|----------|--------|-----------------|
| Criar | CreateNounCommand | CreateUnitCommand |
| Atualizar | UpdateNounCommand | UpdateUnitCommand |
| Excluir | DeleteNounCommand | DeleteUnitCommand |
| Vincular | LinkNounCommand | LinkHolderCommand |
| Desvincular | UnlinkNounCommand | UnlinkHolderCommand |
| Mudar status | VerbNounCommand | ApproveUnitCommand, RejectUnitCommand |
| Upload | UploadNounCommand | UploadDocumentCommand |
| Processar | ProcessNounCommand | ProcessOrtofotoCommand |

### Queries (Leitura)

| Operacao | Padrao | Exemplo Completo |
|----------|--------|-----------------|
| Buscar por ID | GetNounByIdQuery | GetUnitByIdQuery |
| Listar com filtros | ListNounsQuery | ListUnitsQuery |
| Buscar por criterio | GetNounByXQuery | GetHolderByCpfQuery |
| Pesquisar texto | SearchNounsQuery | SearchHoldersQuery |
| Contar | CountNounsQuery | CountUnitsByStatusQuery |
| Estatisticas | GetNounStatsQuery | GetCommunityStatsQuery |

## Nomenclatura de DTOs

| Tipo | Padrao | Uso | Exemplo |
|------|--------|-----|---------|
| Leitura | NounDto | Retorno de queries | UnitDto, HolderDto |
| Leitura resumida | NounSummaryDto | Listas paginadas | UnitSummaryDto |
| Criacao | CreateNounRequest | Body de POST | CreateUnitRequest |
| Atualizacao | UpdateNounRequest | Body de PUT/PATCH | UpdateUnitRequest |
| Resposta wrapper | NounResponse | Envelope de resposta | PagedResponse, ErrorResponse |
| Resultado generico | Result / Result<T> | Retorno de handlers | Result, Result<UnitDto> |

## Nomenclatura de Banco de Dados

### Tabelas

| Entidade | Tabela | Observacao |
|----------|--------|-----------|
| Unit | units | Plural, snake_case |
| Holder | holders | Plural, snake_case |
| UnitHolder | unit_holders | Join table, ambos plurais |
| Community | communities | Plural, snake_case |
| Block | blocks | Plural, snake_case |
| Plot | plots | Plural, snake_case |
| Document | documents | Plural, snake_case |
| Team | teams | Plural, snake_case |
| TeamMember | team_members | Plural, snake_case |
| Account | accounts | Plural, snake_case |
| Tenant | tenants | Plural, snake_case |
| Session | sessions | Plural, snake_case |
| ApiKey | api_keys | Plural, snake_case |
| LegitimationRequest | legitimation_requests | Plural, snake_case |

### Colunas Padrao

| Coluna | Tipo | Presente em | Descricao |
|--------|------|-------------|-----------|
| id | uuid | Todas | PK, gerado pela aplicacao |
| tenant_id | uuid | Todas (exceto tenants) | FK para tenants, filtro multi-tenant |
| created_at | timestamptz | Todas | Data de criacao (UTC) |
| updated_at | timestamptz | Todas | Data da ultima atualizacao (UTC) |
| created_by | uuid | Entidades auditaveis | FK para accounts |
| updated_by | uuid | Entidades auditaveis | FK para accounts |
| version | integer | Entidades sincronizaveis | Controle de versao para sync mobile |
| is_deleted | boolean | Entidades com soft delete | Flag de exclusao logica |

### Indices

| Padrao | Exemplo | Uso |
|--------|---------|-----|
| ix_{tabela}_{coluna} | ix_units_tenant_id | Indice simples |
| ix_{tabela}_{col1}_{col2} | ix_unit_holders_unit_id_holder_id | Indice composto |
| uq_{tabela}_{coluna} | uq_holders_cpf_tenant_id | Constraint unique |
| ix_{tabela}_{coluna}_gin | ix_units_geometry_gin | Indice espacial GIN/GiST |

## Nomenclatura de Domain Events

Formato: `{Entidade}{Acao no Passado}Event`

| Evento | Publicado por | Descricao |
|--------|--------------|-----------|
| UnitCreatedEvent | Unit.Create() | Unidade criada |
| UnitUpdatedEvent | Unit.Update() | Unidade atualizada |
| UnitDeletedEvent | Unit.Delete() | Unidade excluida |
| UnitStatusChangedEvent | Unit.ChangeStatus() | Status da unidade alterado |
| HolderLinkedEvent | Unit.LinkHolder() | Titular vinculado a unidade |
| HolderUnlinkedEvent | Unit.UnlinkHolder() | Titular desvinculado da unidade |
| DocumentUploadedEvent | Document.Create() | Documento uploaded |
| CommunityCreatedEvent | Community.Create() | Comunidade criada |
| CommunityBoundaryChangedEvent | Community.UpdateBoundary() | Limite da comunidade alterado |
| CommunityArchivedEvent | Community.Archive() | Comunidade arquivada |
| AccessGrantedEvent | Community.GrantAccess() | Acesso concedido a comunidade |
| AccessRevokedEvent | Community.RevokeAccess() | Acesso revogado |
| RequestSubmittedEvent | LegitimationRequest.Submit() | Pedido de legitimacao submetido |
| RequestApprovedEvent | LegitimationRequest.Approve() | Pedido aprovado |
| RequestRejectedEvent | LegitimationRequest.Reject() | Pedido rejeitado |
| CertificateIssuedEvent | LegitimationRequest.IssueCertificate() | Certidao emitida |

## Nomenclatura de Endpoints REST

| Operacao | Verbo HTTP | Rota | Exemplo |
|----------|-----------|------|---------|
| Listar | GET | /api/{noun}s | GET /api/units |
| Buscar por ID | GET | /api/{noun}s/{id} | GET /api/units/{id} |
| Criar | POST | /api/{noun}s | POST /api/units |
| Atualizar | PUT | /api/{noun}s/{id} | PUT /api/units/{id} |
| Atualizar parcial | PATCH | /api/{noun}s/{id} | PATCH /api/units/{id} |
| Excluir | DELETE | /api/{noun}s/{id} | DELETE /api/units/{id} |
| Acao especifica | POST | /api/{noun}s/{id}/{verb} | POST /api/units/{id}/approve |
| Sub-recurso | GET | /api/{noun}s/{id}/{sub}s | GET /api/units/{id}/holders |

## Regras Gerais

1. **Ingles para codigo**: todas as classes, variaveis, metodos e nomes de tabela/coluna em ingles
2. **Portugues para documentacao**: toda documentacao do repositorio CARF em portugues brasileiro
3. **Sem abreviacoes**: nomes completos (Repository, nao Repo; Configuration, nao Config — exceto em nomes de arquivos de configuracao)
4. **Consistencia**: se uma convencao for adotada, todos os casos devem segui-la — sem excecoes
5. **Namespace = pasta**: o namespace C# deve espelhar exatamente a estrutura de pastas