# UNIT

Testes unitários isolados sem dependências externas. domain-unit-tests.md testa entities (Unit.CalculateArea retorna área correta dado polygon, Unit constructor valida status inicial Rascunho, CPF value object valida formato rejeita inválido), value objects imutáveis equality by value, aggregates invariantes (UnitAggregate.AddHolder valida max 1 is_main). application-tests.md testa use cases (CreateUnitCommandHandler mock IUnitRepository, valida chamou Add com entity correto, publicou UnitCreatedEvent), validators (CreateUnitValidator valida required fields, CPF format, coordinates bounds). Fast rodando milissegundos, deterministicos sem flakiness, coverage alto business logic.

---

**Última atualização:** 2025-01-05
**Status do arquivo**: Review
