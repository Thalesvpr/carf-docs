# Terminology - GEOAPI

## Glossário Técnico

### Clean Architecture

- **Gateway Layer** - Camada externa que lida com HTTP requests, dependency injection, middleware. Contém Controllers ASP.NET Core.
- **Application Layer** - Camada de use cases contendo Commands, Queries, Handlers, DTOs. Orquestra fluxo de negócio.
- **Domain Layer** - Núcleo puro da aplicação com Entities, Aggregates, Value Objects, Business Rules. Sem dependências externas.
- **Infrastructure Layer** - Camada de implementação de detalhes externos (EF Core, PostgreSQL, Keycloak, file system).

### Domain-Driven Design (DDD)

- **Aggregate** - Cluster de entidades tratadas como unidade transacional. Ex: UnitAggregate agrupa Unit + Holders + Documents.
- **Entity** - Objeto com identidade única persistida no banco (Unit, Holder, Community). Definido por ID, não por propriedades.
- **Value Object** - Objeto imutável definido apenas por valores (CPF, Email, Coordinates). Sem identidade, duas instâncias com mesmos valores são iguais.
- **Domain Event** - Evento representando algo que aconteceu no domínio (UnitCreatedEvent, LegitimationApprovedEvent). Usado para comunicação entre aggregates.
- **Bounded Context** - Fronteira explícita de um modelo de domínio. GEOAPI tem contexto de regularização fundiária (REURB).
- **Ubiquitous Language** - Linguagem compartilhada entre devs e domain experts. Termos: Unidade, Posseiro, Legitimação.
- **Specification** - Regra de negócio encapsulada testável (`UnitMustHaveValidCoordinatesSpec`). Pode ser combinada com AND/OR.

### CQRS

- **Command** - Objeto representando intenção de modificar estado (CreateUnitCommand, UpdateHolderCommand). Retorna void ou DTO.
- **Query** - Objeto representando leitura sem side effects (GetUnitByIdQuery, ListCommunitiesQuery). Retorna DTO.
- **Handler** - Classe que processa Command ou Query via MediatR. Implementa `IRequestHandler<TCommand, TResponse>`.
- **DTO (Data Transfer Object)** - Objeto para transferir dados entre camadas sem lógica de negócio (UnitDto, HolderDto).

### Repository Pattern

- **Repository** - Abstração de acesso a dados. Interface no Domain, implementação no Infrastructure.
- **Unit of Work** - Gerenciamento de transações. No GEOAPI, implementado via DbContext do EF Core.

### Multi-Tenancy

- **Tenant** - Organização cliente do sistema (município). Cada tenant tem dados isolados.
- **RLS (Row-Level Security)** - Policy PostgreSQL que filtra rows baseado em usuário/tenant. Aplicada automaticamente em todas as queries.
- **Tenant Isolation** - Isolamento de dados entre tenants. Garantido por RLS no banco.

### Entity Framework Core

- **DbContext** - Sessão com o banco de dados. Gerencia conexão, change tracking, transações.
- **Migration** - Script de mudança de schema do banco. Versionado no código (`dotnet ef migrations add`).
- **Fluent API** - Configuração de mapeamento via código (`modelBuilder.Entity<Unit>()`). Alternativa a Data Annotations.
- **Change Tracker** - Rastreia mudanças em entidades carregadas. Gera SQL UPDATE/DELETE automaticamente.
- **AsNoTracking()** - Desabilita change tracking para queries read-only. Melhora performance.

### MediatR

- **IRequest<TResponse>** - Interface para Commands/Queries. Define tipo de retorno.
- **IRequestHandler<TRequest, TResponse>** - Interface para Handlers. Processa request.
- **INotification** - Interface para Domain Events. Múltiplos handlers podem subscrever.
- **INotificationHandler<TNotification>** - Handler para Domain Events.

### Keycloak

- **Realm** - Namespace isolado no Keycloak. GEOAPI usa realm `carf`.
- **Client** - Aplicação registrada no Keycloak (geoweb-client, admin-client).
- **Role** - Permissão atribuída a usuários (ADMIN, ANALYST, FIELD_AGENT).
- **JWT (JSON Web Token)** - Token de autenticação contendo claims (roles, tenant_id, user_id).

### PostgreSQL + PostGIS

- **PostGIS** - Extensão PostgreSQL para dados geoespaciais. Suporta geometrias (Point, Polygon, LineString).
- **SRID** - Spatial Reference System Identifier. GEOAPI usa SRID 4326 (WGS84 lat/lon).
- **Geometry** - Tipo de dado geoespacial. Armazenado em coluna `geometry` tipo `GEOMETRY(POLYGON, 4326)`.
- **Spatial Index** - Índice GiST para queries geoespaciais rápidas (`CREATE INDEX ON units USING GIST(geometry)`).

### Testes

- **Unit Test** - Testa classe isolada mockando dependências. Rápido, sem I/O.
- **Integration Test** - Testa múltiplas camadas juntas (Application + Infrastructure). Usa banco de teste.
- **In-Memory Database** - Banco temporário em memória para testes (SQLite in-memory ou Testcontainers PostgreSQL).

## Termos do Domínio REURB

- **REURB** - Regularização Fundiária Urbana. Processo de legalizar ocupações informais.
- **Unidade** - Lote ou terreno sendo regularizado (Unit entity).
- **Posseiro** - Pessoa que ocupa a unidade (Holder entity).
- **Núcleo Urbano Informal** - Conjunto de unidades (Community entity).
- **Legitimação Fundiária** - Instrumento de regularização que transfere propriedade (LegitimationRequest).
- **CRI** - Cartório de Registro de Imóveis. Registra propriedade.

