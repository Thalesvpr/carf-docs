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

Ver também em GEOAPI/DOCS:
- ARCHITECTURE - Decisões arquiteturais específicas do GEOAPI
- CONCEPTS - Conceitos fundamentais (Clean Architecture, CQRS, DDD)

---

**Última atualização:** 2026-01-12

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (5 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-configure-keycloak](./01-configure-keycloak.md) | Configure Keycloak |
| [01-setup-dev-environment](./01-setup-dev-environment.md) | Setup Dev Environment - GEOAPI |
| [02-build-and-run](./02-build-and-run.md) | Build and Run |
| [02-validate-tokens](./02-validate-tokens.md) | Validate Tokens |
| [03-test-authentication](./03-test-authentication.md) | Test Authentication |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Falta parágrafo denso introdutório; Muitas listas com bullets (7) antes do rodapé - considerar converter para parágrafo denso.
