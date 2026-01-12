# HOW-TO - GEOAPI

Guias práticos para desenvolvimento e configuração do GEOAPI backend .NET.

## Setup Inicial

- **[01-setup-dev-environment.md](./01-setup-dev-environment.md)** - Setup completo ambiente desenvolvimento: instalar .NET 9 SDK Docker, clonar repositório, subir PostgreSQL PostGIS, configurar Keycloak, aplicar migrations, rodar API

## Autenticação e Keycloak

- **[01-configure-keycloak.md](./01-configure-keycloak.md)** - Configurar Keycloak authentication em appsettings.json, adicionar middleware AddJwtBearer, configurar TokenValidationParameters e RoleClaimType
- **[02-validate-tokens.md](./02-validate-tokens.md)** - Validar tokens JWT manualmente em testes de integração, obter token via password grant, usar tokens mockados
- **[03-test-authentication.md](./03-test-authentication.md)** - Testar autenticação end-to-end, iniciar Keycloak local, criar usuário de teste, verificar RLS por tenant

## Build e Execução

- **[02-build-and-run.md](./02-build-and-run.md)** - Build, run e deploy do GEOAPI em diferentes ambientes

## Conceitos Relacionados

Ver também:
- [ARCHITECTURE/](../ARCHITECTURE/README.md) - Decisões arquiteturais específicas do GEOAPI
- [CONCEPTS/](../CONCEPTS/README.md) - Conceitos fundamentais (Clean Architecture, CQRS, DDD)

---

**Última atualização:** 2026-01-10
