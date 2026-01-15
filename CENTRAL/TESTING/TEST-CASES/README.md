# TEST-CASES

Casos de teste organizados por tipo, facilitando encontrar e manter testes específicos.

Os [testes de API](./API/README.md) cobrem endpoints REST: authentication com cenários de login válido, inválido e token expirado; units com CRUD completo, validações, filtros e paginação; e endpoints similares para holders, communities, reports e legitimation.

Os [testes E2E](./E2E/README.md) validam jornadas completas do usuário: unit-creation-flow para cadastrar unidade, vincular titular e aprovar; offline-sync-flow para testar coleta offline no REURBCAD com sincronização e resolução de conflitos.

Os [testes unitários](./UNIT/README.md) cobrem código isolado: domain-tests para entities, value objects e aggregates sem dependências externas; application-tests para use cases com mock de repositories.

Fixtures, factories e test data builders facilitam o setup rápido dos testes.

## Estrutura

- **[API/](./API/README.md)** - Testes de API REST
- **[E2E/](./E2E/README.md)** - Testes end-to-end
- **[UNIT/](./UNIT/README.md)** - Testes unitários

---

**Última atualização:** 2026-01-14
