# Clean Architecture

Clean Architecture organiza GEOAPI em camadas concêntricas com dependências apontando sempre para dentro garantindo testabilidade e manutenibilidade implementando separação clara entre Domain Application Infrastructure Gateway. Domain núcleo contém entities (Unit Holder Community herdam BaseEntity), value objects imutáveis (CPF Email GeoPolygon), domain events (UnitCreatedEvent HolderLinkedEvent), e exceptions de negócio (ValidationException ConflictException) completamente puro sem dependências NuGet nem frameworks. Application orquestra use cases via CQRS com command handlers (CreateUnitCommandHandler modificando estado), query handlers (GetUnitByIdQueryHandler retornando DTOs), interfaces de portas (IUnitRepository via Repository pattern, IEmailService, ITenantProvider extraindo de JWT claims multi-tenancy RLS), e pipelines MediatR cross-cutting (logging validation transaction). Infrastructure implementa adaptadores concretos (UnitRepository usando EF Core, EmailService usando SendGrid, TenantProvider extraindo de JWT claims), migrations database, configurações DI, e integrações externas Keycloak RabbitMQ. Gateway API layer traduz HTTP para comandos/queries sem lógica negócio, controllers magros delegando para MediatR, DTOs request/response mapeados via AutoMapper, e middleware tratando autenticação/autorização/exception handling. Regra de dependência: Domain não conhece ninguém, Application depende só de Domain, Infrastructure depende de Application/Domain, Gateway depende de tudo mas é thin layer substituível.

## Implementação

Pattern implementado no backend GEOAPI estruturado em 4 layers físicas separadas (Domain.csproj Application.csproj Infrastructure.csproj Gateway.csproj) compilando em assemblies distintos enforcement de regra de dependência via project references unidirecionais bloqueando circular dependencies em build time, Domain layer contém aggregates como UnitAggregate encapsulando invariantes de negócio, Application layer implementa CQRS pattern separando leitura/escrita, Infrastructure layer integra com PostgreSQL+PostGIS via EF Core e Keycloak para autenticação, e Gateway layer expõe REST API consumida pelos frontends GEOWEB REURBCAD ADMIN.

---

**Última atualização:** 2026-01-10
**Status do arquivo**: Pronto
