# TESTING

Estratégia de testes do CARF garantindo qualidade e confiabilidade do código.

A [estratégia](./TEST-STRATEGY/README.md) segue a pirâmide de testes com proporção de 70% unitários, 20% integração e 10% E2E, priorizando feedback rápido. As metas de coverage são 80% para domain layer, 60% para application e 40% para infrastructure. O pipeline CI falha se o coverage ficar abaixo dos targets.

Os [casos de teste](./TEST-CASES/README.md) estão organizados por tipo: testes de API para endpoints REST, testes E2E para jornadas completas do usuário, e testes unitários para domain e application layers.

Inclui fixtures, factories e test data builders para setup rápido, evitando código duplicado nos testes.

## Estrutura

- **[TEST-STRATEGY/](./TEST-STRATEGY/README.md)** - Pirâmide de testes e coverage targets
- **[TEST-CASES/](./TEST-CASES/README.md)** - Casos de teste organizados por tipo

---

**Última atualização:** 2026-01-14
