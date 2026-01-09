# COMPOSE

Docker Compose orchestration do CARF. docker-compose.dev.yml desenvolvimento (volumes mounting código para hot-reload, ports expostos localhost, logs verbose, sem resource limits, serviços: postgres, keycloak, redis, geoapi, geoweb). docker-compose.staging.yml (images pre-built tagged :staging, environment vars via .env.staging, healthchecks, depends_on com condition service_healthy, networks isoladas). docker-compose.prod.yml production (resource limits memory/cpu, restart: always, logging driver json-file com rotation, secrets via Docker secrets ao invés .env files, traefik reverse proxy com SSL). Override files: docker-compose.override.yml local customizations gitignored.

---

**Última atualização:** 2025-12-29
