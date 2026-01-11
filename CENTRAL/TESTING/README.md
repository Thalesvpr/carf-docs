# TESTING

Estratégia de testes do CARF organizada em TEST-STRATEGY (test-pyramid.md defendendo proporção 70% unit / 20% integration / 10% e2e, coverage-targets.md definindo mínimo 80% coverage para domain layer, 60% para application, ferramentas de testes unitários para backend, framework de testes para frontend, framework de testes E2E para mobile) e TEST-CASES organizados por tipo ao invés de módulo: API (authentication-api-tests.md com cenários de login válido/inválido, token expiration, refresh; units-api-tests.md com CRUD completo, validações, filtros, paginação; holders, communities, reports, legitimation seguem padrão similar), E2E (unit-creation-flow.md testando jornada completa de cadastrar unidade→vincular titular→aprovar; offline-sync-flow.md para REURBCAD testar coleta offline→sincronização→resolução de conflitos), e UNIT (domain-unit-tests.md testando entidades, value objects, aggregates isoladamente; application-tests.md testando use cases com mocks de repositories). Inclui fixtures, factories, e test data builders para setup rápido.

## Estrutura de Testes

### Estratégia de Testes
Ver [TEST-STRATEGY/](./TEST-STRATEGY/README.md):
- [test-pyramid.md](./TEST-STRATEGY/test-pyramid.md) - Pirâmide de testes (70% unit / 20% integration / 10% e2e)
- [coverage-targets.md](./TEST-STRATEGY/coverage-targets.md) - Metas de cobertura por camada

### Casos de Teste
Ver [TEST-CASES/](./TEST-CASES/README.md):
- [API/](./TEST-CASES/API/README.md) - Testes de API REST endpoints
- [E2E/](./TEST-CASES/E2E/README.md) - Testes end-to-end de fluxos completos
- [UNIT/](./TEST-CASES/UNIT/README.md) - Testes unitários de domain e application

---

**Última atualização:** 2025-01-05
