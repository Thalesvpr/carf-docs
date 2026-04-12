---
type: readme
status: review
updated: 2026-01-12
---

# LAYERS

Camadas da Clean Architecture do GEOAPI seguindo Dependency Inversion Principle separando responsabilidades domain application infrastructure presentation com testes automatizados em cada nível.

## Camadas

- **[DOMAIN/](./DOMAIN/README.md)** - Núcleo de negócio (entities, value objects, contracts, events)
- **[APPLICATION/](./APPLICATION/README.md)** - Use cases (commands, queries, DTOs, validators)
- **[INFRA/](./INFRA/README.md)** - Implementações técnicas (EF Core, Keycloak, S3)
- **[PRESENTATION/](./PRESENTATION/README.md)** - API REST controllers middlewares filters hubs SignalR
- **[TESTS/](./TESTS/README.md)** - Testes unitários integração E2E por camada

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (5)

| Pasta | Descrição |
|-------|-----------|
| [APPLICATION](./APPLICATION/README.md) | ... |
| [DOMAIN](./DOMAIN/README.md) | ... |
| [INFRA](./INFRA/README.md) | ... |
| [PRESENTATION](./PRESENTATION/README.md) | ... |
| [TESTS](./TESTS/README.md) | ... |

<!-- CARF-INDEX-END -->
