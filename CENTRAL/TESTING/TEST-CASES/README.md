# TEST-CASES

Casos de teste organizados por tipo, facilitando encontrar e manter testes específicos.

Os [testes de API](./API/README.md) cobrem endpoints REST: authentication com cenários de login válido, inválido e token expirado; units com CRUD completo, validações, filtros e paginação; e endpoints similares para holders, communities, reports e legitimation.

Os [testes E2E](./E2E/README.md) validam jornadas completas do usuário: unit-creation-flow para cadastrar unidade, vincular titular e aprovar; offline-sync-flow para testar coleta offline no REURBCAD com sincronização e resolução de conflitos.

Os [testes unitários](./UNIT/README.md) cobrem código isolado: domain-tests para entities, value objects e aggregates sem dependências externas; application-tests para use cases com mock de repositories.

Fixtures, factories e test data builders facilitam o setup rápido dos testes.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Api](./API/README.md) | 0 |
|  | [E2e](./E2E/README.md) | 0 |
|  | [Unit](./UNIT/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
