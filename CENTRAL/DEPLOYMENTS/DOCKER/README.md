---
type: readme
status: rejected
description: "Conteudo operacional. Configs de deploy pertencem a PROJECTS ou infra repo separado."
updated: 2026-01-15
---

# DOCKER

Containerização Docker do CARF. DOCKERFILES contém Dockerfile por projeto (Dockerfile.geoapi multi-stage build dotnet restore/build/publish, Dockerfile.geoweb node build React, Dockerfile.keycloak customizado). COMPOSE contém docker-compose files por ambiente (docker-compose.dev.yml services geoapi/postgres/keycloak/redis/geoweb volumes mounted code hot-reload, docker-compose.staging.yml imagens pre-built sem volumes, docker-compose.prod.yml com resource limits, health checks, restart policies). Networks isolando services (backend-network para GEOAPI-PostgreSQL, frontend-network para GEOWEB-GEOAPI). Secrets via env files .env.dev/.env.prod gitignored. Build: docker-compose build, run: docker-compose up -d, logs: docker-compose logs -f service-name.

## Subpastas

- **[DOCKERFILES](CENTRAL/DEPLOYMENTS/DOCKER/DOCKERFILES/README.md)** - Dockerfile por projeto
- **[COMPOSE](CENTRAL/DEPLOYMENTS/DOCKER/COMPOSE/README.md)** - Docker Compose por ambiente


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (4 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Compose](CENTRAL/DEPLOYMENTS/DOCKER/COMPOSE/README.md) | 2 |
|  | [Dockerfiles](CENTRAL/DEPLOYMENTS/DOCKER/DOCKERFILES/README.md) | 2 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/DEPLOYMENTS/DOCKER/COMPOSE/README|COMPOSE]]
- [[CENTRAL/DEPLOYMENTS/DOCKER/DOCKERFILES/README|DOCKERFILES]]

<!-- CARF-INDEX-END -->
