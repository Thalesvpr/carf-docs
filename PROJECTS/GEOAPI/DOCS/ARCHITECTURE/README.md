# Arquitetura - GEOAPI

Documentação arquitetural do backend REST API do projeto CARF.

## 📚 Documentos Disponíveis

| Documento | Descrição |
|-----------|-----------|
| [01-overview.md](./01-overview.md) | Visão geral da arquitetura Clean Architecture + DDD |
| [01-keycloak-integration.md](./01-keycloak-integration.md) | Integração com Keycloak (OAuth2/OIDC) |
| [02-admin-security.md](./02-admin-security.md) | Segurança e separação frontend/backend admin |
| [03-data-flow.md](./03-data-flow.md) | Fluxo de dados (Request → CQRS → Repository → DB) |
| [04-integration.md](./04-integration.md) | Integrações externas (Keycloak, PostgreSQL, consumidores) |
| [05-deployment.md](./05-deployment.md) | Arquitetura de deployment (Docker, Kubernetes) |

## 🏛️ Visão Geral da Arquitetura

GEOAPI é construído seguindo **Clean Architecture** com **Domain-Driven Design (DDD)** e **CQRS Pattern**.

### Camadas

```
┌─────────────────────────────────────────┐
│           Gateway (API Layer)           │  Controllers, Middleware
├─────────────────────────────────────────┤
│       Application (Use Cases)           │  Commands, Queries, Handlers
├─────────────────────────────────────────┤
│          Domain (Business)              │  Entities, Aggregates, Rules
├─────────────────────────────────────────┤
│      Infrastructure (External)          │  Repositories, Database, APIs
└─────────────────────────────────────────┘
```

### Stack Tecnológico

- **.NET 9** - Framework backend
- **Entity Framework Core** - ORM
- **PostgreSQL 16 + PostGIS 3.4** - Banco de dados geoespacial
- **MediatR** - CQRS pattern
- **FluentValidation** - Validação de dados
- **Serilog** - Logging estruturado
- **Keycloak** - Autenticação e autorização
- **xUnit + Moq** - Testes

## 🎯 Padrões Arquiteturais

### Clean Architecture
Separação clara de responsabilidades em camadas, com dependências apontando sempre para dentro (Domain é o núcleo).

### Domain-Driven Design (DDD)
- **Aggregates:** Unit, Community, LegitimationRequest
- **Entities:** Possuidores de identidade única
- **Value Objects:** Objetos imutáveis (CPF, Coordinates, Address)
- **Domain Events:** Eventos de negócio (UnitCreated, HolderRegistered)

### CQRS (Command Query Responsibility Segregation)
- **Commands:** Operações que modificam estado (CreateUnit, UpdateHolder)
- **Queries:** Operações de leitura (GetUnitById, ListCommunities)
- **Handlers:** Processam comandos e queries via MediatR

### Repository Pattern
Abstração de acesso a dados, implementado na camada Infrastructure.

### Unit of Work
Gerenciamento de transações através do DbContext do EF Core.

## 🔐 Segurança

- **Autenticação:** JWT tokens via Keycloak
- **Autorização:** RBAC com 5 níveis (Admin, Analyst, Field Agent, Municipality Manager, Public)
- **Multi-tenancy:** Row-Level Security (RLS) no PostgreSQL
- **Validação:** Entrada validada em múltiplas camadas (DTO → Domain)
- **HTTPS:** TLS 1.3 obrigatório em produção

## 📊 Decisões Arquiteturais Relacionadas

- [ADR-001: .NET 9 Backend](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-001-dotnet-9-backend.md)
- [ADR-002: PostgreSQL + PostGIS](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md)
- [ADR-003: Keycloak Autenticação](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md)
- [ADR-005: Multi-tenancy RLS](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md)
- [ADR-008: Clean Architecture DDD](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-008-clean-architecture-ddd.md)
- [ADR-009: CQRS Pattern](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-009-cqrs-pattern.md)
- [ADR-010: Event-Driven Architecture](../../../../CENTRAL/ARCHITECTURE/ADRs/ADR-010-event-driven-architecture.md)

## 🔗 Referências

- [CENTRAL/API/](../../../../CENTRAL/API/README.md) - Especificação de endpoints
- [CENTRAL/DOMAIN-MODEL/](../../../../CENTRAL/DOMAIN-MODEL/README.md) - Modelo de domínio
- [CENTRAL/BUSINESS-RULES/](../../../../CENTRAL/BUSINESS-RULES/README.md) - Regras de negócio
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design (Eric Evans)](https://domainlanguage.com/ddd/)
