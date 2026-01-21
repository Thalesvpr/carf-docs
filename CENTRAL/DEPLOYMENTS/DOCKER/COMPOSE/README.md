---
status: review
updated: 2026-01-15
---

# COMPOSE

Sistema CARF utiliza Docker Compose para orquestração de serviços em diferentes ambientes sendo docker-compose.dev.yml para desenvolvimento local com volumes mounting código-fonte permitindo hot-reload durante desenvolvimento, ports expostos diretamente em localhost facilitando debug, logs verbose para troubleshooting, sem resource limits permitindo uso total de recursos da máquina, incluindo serviços postgres keycloak redis geoapi e geoweb configurados para startup rápido e iteração ágil de desenvolvimento.

Ambiente staging utiliza docker-compose.staging.yml com images pre-built e tagged com versão :staging garantindo imutabilidade e reprodutibilidade, environment variables gerenciadas via arquivo .env.staging separado do desenvolvimento, healthchecks configurados para todos serviços validando saúde antes de marcar ready, depends_on com condition service_healthy garantindo ordem correta de startup onde geoapi só inicia após postgres e keycloak estarem operacionais, networks isoladas separando comunicação interna de acesso externo melhorando segurança e simulando ambiente produção.

Ambiente produção usa docker-compose.prod.yml com resource limits definindo memory e cpu por container evitando consumo excessivo e garantindo estabilidade, restart: always configurado para recovery automático de crashes, logging driver json-file com rotation evitando disco cheio por logs acumulados, secrets gerenciados via Docker secrets ao invés de .env files em plaintext protegendo credenciais sensíveis, traefik como reverse proxy com SSL terminação automática via Let's Encrypt. Customizações locais utilizam docker-compose.override.yml gitignored permitindo desenvolvedores ajustarem configuração sem afetar repositório compartilhado.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (2 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-docker-compose-dev](01-docker-compose-dev.md) | Docker Compose Development |
| [02-docker-compose-prod](02-docker-compose-prod.md) | Docker Compose Production |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/DEPLOYMENTS/DOCKER/COMPOSE/01-docker-compose-dev.md|Docker Compose Development]]
- ○ [[CENTRAL/DEPLOYMENTS/DOCKER/COMPOSE/02-docker-compose-prod.md|Docker Compose Production]]

<!-- CARF-INDEX-END -->
