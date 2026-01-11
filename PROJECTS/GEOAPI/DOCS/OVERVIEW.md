# GEOAPI - Overview de Implementação

Backend REST API .NET 9 com Clean Architecture + DDD implementando toda lógica de negócio, persistência PostgreSQL+PostGIS, autenticação Keycloak, multi-tenancy RLS e geração de relatórios PDF/Shapefile conforme Lei 13465/2017.

## Requirements Implementados

### Use Cases Principais

- [UC-001: Cadastrar Unidade](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-001-cadastrar-unidade-habitacional.md) - API POST /units
- [UC-002: Aprovar Unidade](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-002-aprovar-unidade-habitacional.md) - Workflow engine
- [UC-003: Vincular Titular](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-003-vincular-titular-unidade.md) - API /unit-holders
- [UC-005: Sincronizar Offline](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-005-sincronizar-dados-offline.md) - **CORE** - Sync engine conflict resolution
- [UC-006: Gerar Relatório](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-006-gerar-relatorio-comunidade.md) - PDF generation
- [UC-007: Exportar Dados](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-007-exportar-dados-geograficos.md) - Shapefile export
- [UC-009: Gerenciar Legitimação](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-009-gerenciar-processo-legitimacao.md) - **CORE** - Legitimation workflow
- [UC-010: Configurar WMS](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-010-configurar-camadas-wms.md) - WMS proxy

Todos os 11 UCs principais têm implementação backend parcial ou total.

## Domain Model Implementado

### Entities (todas - backend é source of truth)

Todas 35 entities de [DOMAIN-MODEL/ENTITIES](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/README.md) implementadas com Entity Framework Core:

- BaseEntity, BaseAggregateRoot (classes base)
- Unit, Holder, Community, UnitHolder (core domain)
- Tenant, Account, Team (multi-tenancy + auth)
- Document, Annotation (suporte)
- SyncLog, AuditLog (audit trail)
- LegitimationRequest, LegitimationResponse, LegitimationCertificate (Lei 13465)
- WmsServer, WmsLayer (ortofotos)
- SurveyPoint, SurveyProcessing, Monograph (topografia)

### Value Objects (todas)

Implementados como C# records imutáveis:

- CPF, CNPJ, Crea, Email, PhoneNumber, Address
- GeoPolygon, GeoPoint, Coordinates (NetTopologySuite)
- UnitStatus, SyncStatus, LegitimationStatus, Decision
- CustomDataSchema, PermissionsMatrix, SpatialOverlapMatrix

### Aggregates (todas 3)

- [UnitAggregate](../../../CENTRAL/DOMAIN-MODEL/AGGREGATES/01-unit-aggregate.md) - EF Core navigation properties
- [CommunityAggregate](../../../CENTRAL/DOMAIN-MODEL/AGGREGATES/02-community-aggregate.md) - Aggregate boundaries
- [LegitimationRequestAggregate](../../../CENTRAL/DOMAIN-MODEL/AGGREGATES/03-legitimation-request-aggregate.md) - Workflow state machine

### Domain Events (todos 20)

Implementados com MediatR:

- UnitCreatedEvent, UnitStatusChangedEvent, HolderLinkedEvent, etc.
- Handlers para notificações, audit logging, side effects

## Arquitetura Técnica

**Stack:**
- .NET 9 (C# 12, AOT compilation)
- ASP.NET Core Web API
- Entity Framework Core 8 + Npgsql + NetTopologySuite
- PostgreSQL 16 + PostGIS 3.4
- MediatR (CQRS + Domain Events)
- FluentValidation (validações)
- Keycloak Integration (OAuth2 JWT validation)
- Docker + Kubernetes (deployment)

**Arquitetura:** Clean Architecture (4 layers)
- Domain (entities, VOs, aggregates, events)
- Application (CQRS commands/queries, handlers, validators)
- Infrastructure (EF Core, PostgreSQL, Keycloak, PDF generation)
- Gateway (REST controllers, middlewares, JWT auth)

Ver [ARCHITECTURE/](./ARCHITECTURE/README.md) para detalhes de cada layer.

## Features Documentadas

Backend não tem "features" UI mas sim **endpoints API** documentados em:

- [CENTRAL/API/](../../../CENTRAL/API/README.md) - Contratos REST JSON por domínio
- OpenAPI/Swagger em `/swagger` (runtime docs)

---

**Última atualização:** 2026-01-10
