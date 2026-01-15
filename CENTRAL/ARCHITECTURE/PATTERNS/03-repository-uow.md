# Repository & Unit of Work

Repository Pattern abstrai persistência com interfaces domain (IUnitRepository, IHolderRepository, ICommunityRepository) implementadas no Infrastructure via EF Core mas testáveis via mocks. Repositories encapsulam queries complexas (GetActiveUnitsInCommunity, GetPendingApprovalsByFiscal) usando Specification Pattern componível, retornam entities/aggregates nunca DTOs, suportam async/await para I/O não-bloqueante, e nunca expõem IQueryable evitando queries lazy executadas fora de contexto. Unit of Work coordena transações multi-repository garantindo atomicidade (criar Unit + vincular Holder + disparar evento = tudo ou nada), DbContext EF Core age como UoW natural com ChangeTracker rastreando mudanças, SaveChangesAsync persiste atomicamente disparando domain events via MediatR após commit bem-sucedido, e rollback automático se exception ocorrer. Specifications encapsulam regras reutilizáveis (ActiveUnitsSpec, WithinBoundingBoxSpec, CreatedAfterSpec) combináveis via And/Or, evitam duplicação de queries, facilitam testes validando logic sem database, e permitem trocar ORM sem quebrar domain. Generic repository evitado (cada aggregate tem repository específico com métodos relevantes), queries ad-hoc complexas usam CQRS query handlers direto no DbContext, e read-only queries desabilitam tracking (.AsNoTracking()) otimizando performance.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Pronto
