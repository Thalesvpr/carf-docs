# DOCKER

Containerização Docker do CARF. DOCKERFILES contém Dockerfile por projeto (Dockerfile.geoapi multi-stage build dotnet restore/build/publish, Dockerfile.geoweb node build React, Dockerfile.keycloak customizado). COMPOSE contém docker-compose files por ambiente (docker-compose.dev.yml services geoapi/postgres/keycloak/redis/geoweb volumes mounted code hot-reload, docker-compose.staging.yml imagens pre-built sem volumes, docker-compose.prod.yml com resource limits, health checks, restart policies). Networks isolando services (backend-network para GEOAPI-PostgreSQL, frontend-network para GEOWEB-GEOAPI). Secrets via env files .env.dev/.env.prod gitignored. Build: docker-compose build, run: docker-compose up -d, logs: docker-compose logs -f service-name.

## Subpastas

- **[DOCKERFILES](./DOCKERFILES/README.md)** - Dockerfile por projeto
- **[COMPOSE](./COMPOSE/README.md)** - Docker Compose por ambiente

---

**Última atualização:** 2025-12-29

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (0 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Compose](./COMPOSE/README.md) | 0 |
|  | [Dockerfiles](./DOCKERFILES/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
