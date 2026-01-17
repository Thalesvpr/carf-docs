# CONCEPTS

Documentação conceitual do backend REST API GEOAPI explicando conceitos fundamentais arquitetura patterns e terminologia do domínio de regularização fundiária. Clean Architecture organiza código em 4 camadas onde Gateway recebe HTTP requests Controllers DTOs, Application orquestra use cases Commands Queries Handlers, Domain contém regras negócio puras Entities Aggregates Value Objects sem dependências externas, e Infrastructure implementa detalhes técnicos EF Core PostgreSQL Keycloak. Domain-Driven Design modela domínio com Aggregates garantindo consistência transacional UnitAggregate CommunityAggregate LegitimationRequestAggregate, Value Objects imutáveis CPF Address Coordinates validados no construtor, e Domain Events comunicação assíncrona UnitCreatedEvent LegitimationApprovedEvent.

CQRS separa Commands que modificam estado com validação complexa de Queries que leem estado sem side effects usando projeções otimizadas, ambos despachados via MediatR para handlers isolados testáveis. Multi-tenancy via Row-Level Security PostgreSQL garante isolamento automático onde JWT contém tenant_id claim, middleware seta app.tenant_id, e policies RLS filtram queries automaticamente sem precisar filtrar no código. Repository Pattern abstrai persistência onde Domain depende de interfaces IUnitRepository implementadas por Infrastructure com EF Core garantindo testabilidade e flexibilidade trocar ORM sem afetar domain.

## Arquivos

- **[01-authentication.md](./01-authentication.md)** - Autenticação OAuth2/OIDC com Keycloak JWT
- **[02-authorization.md](./02-authorization.md)** - Autorização RBAC e multi-tenancy RLS
- **[01-key-concepts.md](./01-key-concepts.md)** - Clean Architecture DDD CQRS Repository
- **[02-terminology.md](./02-terminology.md)** - Glossário termos técnicos e negócio REURB
- **[03-design-principles.md](./03-design-principles.md)** - Princípios SOLID DRY KISS YAGNI
- **[04-audit-logging.md](./04-audit-logging.md)** - Sistema auditoria LGPD compliance

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (6 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-authentication](./01-authentication.md) | 01-authentication |
| [01-key-concepts](./01-key-concepts.md) | Key Concepts |
| [02-authorization](./02-authorization.md) | 02-authorization |
| [02-terminology](./02-terminology.md) | Terminology - GEOAPI |
| [03-design-principles](./03-design-principles.md) | Design Principles |
| [04-audit-logging](./04-audit-logging.md) | Audit Logging |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (6) antes do rodapé - considerar converter para parágrafo denso.
