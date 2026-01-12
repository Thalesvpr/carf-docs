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

Implementação GEOAPI baseia-se em decisões arquiteturais documentadas em Architecture Decision Records incluindo ADR-001 escolha .NET 9 como framework backend principal, ADR-002 adoção PostgreSQL com extensão PostGIS para dados geoespaciais, ADR-003 integração Keycloak como provedor autenticação OAuth2 OIDC, ADR-005 implementação multi-tenancy via Row-Level Security PostgreSQL, ADR-008 aplicação Clean Architecture com Domain-Driven Design separando camadas responsabilidades, ADR-009 padrão CQRS separando comandos queries usando MediatR, ADR-010 arquitetura orientada eventos para comunicação desacoplada entre componentes garantindo consistência eventual escalabilidade horizontal permitindo evolução independente módulos sistema conforme requisitos negócio crescimento base usuários municípios atendidos.

## 🔗 Referências

Especificação completa REST API endpoints request response schemas encontra-se documentada em CENTRAL/API descrevendo contratos HTTP métodos status codes autenticação headers query parameters body payloads validation rules rate limiting CORS policies versionamento compatibilidade retroativa clientes frontend mobile web, modelo domínio entities aggregates value objects domain events business rules constraints invariantes documentados CENTRAL/DOMAIN-MODEL e CENTRAL/BUSINESS-RULES estabelecendo linguagem ubíqua bounded contexts compartilhados entre todas aplicações ecossistema CARF garantindo consistência semântica conceitual através projetos GEOWEB REURBCAD ADMIN GEOGIS mantendo alinhamento requirements originais especificados CENTRAL facilitando manutenção evolução coordenada sistema distribuído. Fundamentos teóricos Clean Architecture descritos por Robert C. Martin e Domain-Driven Design por Eric Evans fornecem base conceitual padrões práticas aplicadas implementação GEOAPI.
