---
type: readme
status: review
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
updated: 2026-01-22
---

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

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (5)

| Documento | Status |
|-----------|--------|
| [Configure Keycloak](./01-configure-keycloak.md) | ⚠ |
| [Setup Dev Environment - GEOAPI](./01-setup-dev-environment.md) | ⚠ |
| [Build and Run](./02-build-and-run.md) | ⚠ |
| [Validate Tokens](./02-validate-tokens.md) | ⚠ |
| [Test Authentication](./03-test-authentication.md) | ⚠ |

<!-- CARF-INDEX-END -->
