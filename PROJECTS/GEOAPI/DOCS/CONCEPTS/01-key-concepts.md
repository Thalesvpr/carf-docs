# Key Concepts

Conceitos-chave do GEOAPI incluem Clean Architecture onde dependências apontam para dentro (Gateway → Application → Domain ← Infrastructure) com Domain layer puro sem frameworks externos contendo apenas regras de negócio em C# puro. Domain-Driven Design implementa Ubiquitous Language compartilhado entre devs e stakeholders, Bounded Context de regularização fundiária REURB, Aggregates garantindo consistência transacional, Value Objects imutáveis com validação no construtor, e Domain Events para comunicação assíncrona entre aggregates.

CQRS separa Commands que modificam estado com validação complexa retornando DTOs de Queries que leem estado sem side effects usando projeções otimizadas e cache, ambos despachados via MediatR para handlers isolados e testáveis. Repository Pattern abstrai persistência onde Domain layer depende de interfaces IRepository implementadas por Infrastructure layer com EF Core. Row-Level Security RLS garante isolamento multi-tenant via policies PostgreSQL aplicadas em nível de database, queries automáticas sem precisar filtrar por tenant_id no código.

Aggregates principais incluem UnitAggregate com Unit como root agregando Holders Documents History com invariante que unidade deve ter pelo menos 1 holder e transaction boundary commitando todas mudanças juntas, CommunityAggregate com Community como root agregando referências a Units e Metadata com invariante que comunidade ativa deve ter coordenadas válidas, e LegitimationRequestAggregate com LegitimationRequest como root agregando ApprovalSteps Documents Comments com invariante que request aprovado não pode ser editado.

---

**Última atualização:** 2026-01-12

