---
status: review
updated: 2025-01-05
---

# UNIT

Testes unitários isolados sem dependências externas. domain-unit-tests.md testa entities (Unit.CalculateArea retorna área correta dado polygon, Unit constructor valida status inicial Rascunho, CPF value object valida formato rejeita inválido), value objects imutáveis equality by value, aggregates invariantes (UnitAggregate.AddHolder valida max 1 is_main). application-tests.md testa use cases (CreateUnitCommandHandler mock IUnitRepository, valida chamou Add com entity correto, publicou UnitCreatedEvent), validators (CreateUnitValidator valida required fields, CPF format, coordinates bounds). Fast rodando milissegundos, deterministicos sem flakiness, coverage alto business logic.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (1 arquivo)

| ID | Titulo |
|:---|:-------|
| [01-domain-tests](./01-domain-tests.md) | Domain Unit Tests |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/TESTING/TEST-CASES/UNIT/01-domain-tests.md|Domain Unit Tests]]

<!-- CARF-INDEX-END -->
