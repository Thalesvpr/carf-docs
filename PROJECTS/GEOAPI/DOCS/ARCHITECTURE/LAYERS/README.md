# LAYERS

Camadas da Clean Architecture do GEOAPI seguindo Dependency Inversion Principle separando responsabilidades domain application infrastructure presentation com testes automatizados em cada nível.

## Camadas

- **[DOMAIN/](./DOMAIN/README.md)** - Núcleo de negócio (entities, value objects, contracts, events)
- **[APPLICATION/](./APPLICATION/README.md)** - Use cases (commands, queries, DTOs, validators)
- **[INFRA/](./INFRA/README.md)** - Implementações técnicas (EF Core, Keycloak, S3)
- **[PRESENTATION/](./PRESENTATION/README.md)** - API REST controllers middlewares filters hubs SignalR
- **[TESTS/](./TESTS/README.md)** - Testes unitários integração E2E por camada

---

**Última atualização:** 2026-01-12
