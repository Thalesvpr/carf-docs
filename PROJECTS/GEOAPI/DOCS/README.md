# GEOAPI - Backend REST API .NET

**[📋 Overview de Implementação](./OVERVIEW.md)** - Mapeamento completo de requirements, domain model e arquitetura técnica

API REST backend .NET 9 do sistema CARF fornecendo endpoints HTTP+JSON para operações CRUD de unidades habitacionais, comunidades, titulares, processos de legitimação fundiária e relatórios, implementando Clean Architecture + DDD conforme [ADR-008](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-008-clean-architecture-ddd.md) com camadas Domain (entities, aggregates, value objects), Application (use cases, commands, queries CQRS via MediatR), Infrastructure (repositories EF Core, PostgreSQL+PostGIS persistence, integração Keycloak), e Presentation (controllers ASP.NET Core minimal APIs). Backend conecta ao banco geoespacial PostgreSQL+PostGIS via Entity Framework Core com Row-Level Security implementando multi-tenancy isolando dados por tenant conforme [ADR-005](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md), autenticação via Keycloak OAuth2/OIDC conforme [ADR-003](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md) validando tokens JWT em cada request, autorização via policies role-based usando claims tenant_id e roles extraídos do token, validações server-side usando FluentValidation, logging estruturado via Serilog, background jobs via Hangfire conforme [ADR-021](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-021-hangfire-background-jobs.md), e deployment via Docker containers orquestrados em Kubernetes com health checks, metrics Prometheus, e tracing distribuído OpenTelemetry.

## Documentação

- **[Arquitetura](./ARCHITECTURE/README.md)** - Decisões técnicas e estrutura de camadas Domain/Application/Infrastructure/Presentation
- **[Conceitos](./CONCEPTS/README.md)** - Conceitos fundamentais de Clean Architecture, CQRS, Event Sourcing, DDD aplicados no GEOAPI
- **[Guias Práticos](./HOW-TO/README.md)** - Tutoriais e instruções para setup local, migrations, testes, troubleshooting

## Stack Tecnológico

- **Framework:** .NET 9 + ASP.NET Core conforme [ADR-001](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-001-dotnet-9-backend.md)
- **Database:** PostgreSQL 16 + PostGIS 3.4 conforme [ADR-002](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md)
- **ORM:** Entity Framework Core 9 + Npgsql
- **Authentication:** Keycloak OAuth2/OIDC conforme [ADR-003](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)
- **CQRS:** MediatR conforme [ADR-009](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-009-cqrs-pattern.md)
- **Validation:** FluentValidation
- **Logging:** Serilog + Seq
- **Background Jobs:** Hangfire conforme [ADR-021](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-021-hangfire-background-jobs.md)
- **API Docs:** Swagger/OpenAPI
- **Testing:** xUnit + FluentAssertions + Testcontainers

## Funcionalidades Principais

**CRUD Geoespacial** - Endpoints REST para criar, ler, atualizar e deletar unidades habitacionais com geometrias Polygon/MultiPolygon validadas via PostGIS ST_IsValid, cálculo automático de área via ST_Area, queries espaciais ST_Contains ST_Intersects para buscar unidades dentro de comunidades ou polígonos arbitrários, importação/exportação GeoJSON Shapefile conforme [UC-008](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-008-importar-shapefile.md).

**Multi-tenancy RLS** - Isolamento de dados por tenant usando Row-Level Security PostgreSQL configurando sessão SET app.tenant_id extraído de JWT claim, policies automáticas filtrando todas queries por tenant_id sem código duplicado, validação tenant_id em comandos criação impedindo cross-tenant data leakage, e auditoria completa rastreando AccountId/TenantId em todas operações conforme [ADR-005](../../../CENTRAL/ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md).

**Autenticação OAuth2** - Validação tokens JWT Keycloak em middleware ASP.NET Core verificando assinatura chaves públicas JWKS endpoint, extração claims user_id username email roles tenant_id allowed_tenants, autorização policies RequireRole RequireTenant RequirePermission, refresh token automático frontend detectando 401 Unauthorized, e admin endpoints /api/admin/* restritos role super-admin consumindo Keycloak Admin Client API gerenciando usuários tenants via backend confidential client protegendo client_secret conforme documentado em [Admin Security](./ARCHITECTURE/02-admin-security.md).

**Background Processing** - Jobs assíncronos Hangfire processando operações longas como geração relatórios PDF/Excel de comunidades inteiras com milhares de unidades, importação shapefiles grandes splitting em batches 500 features, sincronização dados offline mobile detectando conflitos aplicando estratégia merge, e envio notificações email via SendGrid ou SMTP server scheduling cron expressions daily/weekly executions.

**APIs Consumidores** - Frontend GEOWEB React consome via [@carf/geoapi-client](../../LIB/TS/GEOAPI-CLIENT/DOCS/README.md) HTTP client TypeScript, mobile REURBCAD React Native sincroniza offline WatermelonDB, plugin GEOGIS QGIS Python consome WFS/WMS endpoints PostGIS, console ADMIN React gerencia usuários/tenants via endpoints /api/admin/*, e portal WEBDOCS VitePress exibe exemplos código documentação interativa.

## Código Fonte

Ver [carf-geoapi README](../SRC-CODE/carf-geoapi/README.md) para instruções de build, instalação e desenvolvimento local.

---

**Última atualização:** 2026-01-10
