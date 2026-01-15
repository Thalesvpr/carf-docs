# TESTS

Estratégia testes GEOAPI implementando pirâmide três níveis: unitários validando entities value objects validators isolados com xUnit Moq, integração verificando interação camadas com Testcontainers PostgreSQL real queries EF Core migrations RLS policies, e E2E exercitando API completa via WebApplicationFactory HTTP requests validando contratos REST autenticação JWT autorização RBAC. Stack inclui xUnit runner, Moq mocking, Testcontainers Docker, FluentAssertions syntax, Bogus dados fake, Coverlet coverage. Convenções nomeiam projetos espelhando source (GeoApi.Domain.Tests), métodos seguem MethodName_Scenario_ExpectedBehavior, fixtures compartilham setup custoso via IClassFixture.

## Subpastas

- **[UNIT/](./UNIT/README.md)** - Testes unitários domain logic isolada
- **[INTEGRATION/](./INTEGRATION/README.md)** - Testes integração com database real
- **[E2E/](./E2E/README.md)** - Testes end-to-end API completa

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [E2e](./E2E/README.md) | 0 |
|  | [Integration](./INTEGRATION/README.md) | 0 |
|  | [Unit](./UNIT/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Pronto
