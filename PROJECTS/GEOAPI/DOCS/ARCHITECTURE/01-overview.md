# Overview

GEOAPI é o backend REST API do ecossistema CARF construído em .NET 9 seguindo Clean Architecture, Domain-Driven Design e CQRS Pattern via MediatR. Clientes GEOWEB React, REURBCAD React Native, ADMIN React e GEOGIS Python conectam via HTTPS/REST através de API Gateway Nginx com load balancing para múltiplos pods GEOAPI, cada um contendo as 4 camadas Gateway Application Domain Infrastructure, persistindo em PostgreSQL 16 com PostGIS 3.4 e Row-Level Security multi-tenant, integrando Keycloak OAuth2/OIDC para autenticação JWT e RBAC.

Gateway Layer expõe endpoints REST com Controllers UnitsController HoldersController CommunitiesController LegitimationController ReportsController AuthenticationController recebendo requisições HTTP validando DTOs delegando para Application, Middlewares AuthenticationMiddleware validando JWT TenantMiddleware extraindo tenant_id ExceptionHandlerMiddleware tratamento global erros LoggingMiddleware logs estruturados, e Filters ValidationFilter FluentValidation AuthorizationFilter RBAC roles permissions.

Application Layer orquestra lógica negócio implementando use cases via CQRS com Commands escrita CreateUnitCommand UpdateUnitCommand DeleteUnitCommand CreateHolderCommand StartLegitimationCommand ApproveLegitimationCommand, Queries leitura GetUnitByIdQuery ListUnitsQuery SearchUnitsQuery GetHolderByIdQuery ListCommunitiesQuery GetLegitimationByIdQuery, Handlers MediatR processando commands queries retornando DTOs CreateUnitDto UpdateUnitDto UnitDto HolderDto CommunityDto LegitimationDto, e Validators FluentValidation validando regras negócio antes persistência.

Domain Layer contém regras negócio puras sem dependências externas com Entities Unit Holder Community LegitimationRequest Team Account Tenant representando conceitos domínio, Value Objects CPF CNPJ Email Address GeoPolygon GeoPoint imutáveis com validação construtor, Aggregates Unit como root agregando Holders Documents garantindo consistência transacional, Domain Events UnitCreatedEvent HolderLinkedEvent LegitimationApprovedEvent comunicação assíncrona, e Contracts interfaces IUnitRepository IHolderRepository ICommunityRepository ITenantProvider ICurrentUser implementadas Infrastructure.

Infrastructure Layer implementa detalhes técnicos com Repositories EF Core UnitRepository HolderRepository CommunityRepository implementando interfaces Domain, DbContext AppDbContext mapeando entities tabelas PostgreSQL configurando RLS policies, Migrations EF Core criando atualizando schema banco, External Services KeycloakClient autenticação EmailService notificações SmsService mensagens FileStorage S3 documentos, e Configuration appsettings.json secrets connection strings JWT settings.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
