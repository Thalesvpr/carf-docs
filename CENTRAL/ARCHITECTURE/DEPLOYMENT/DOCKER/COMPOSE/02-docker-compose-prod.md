# Docker Compose Production

Configuração Docker Compose para ambiente de produção.

## docker-compose.prod.yml

```yaml
version: '3.8'

services:
  geoapi:
    image: carf/geoapi:${GEOAPI_VERSION:-latest}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ConnectionStrings__DefaultConnection=${DATABASE_URL}
      - Keycloak__Authority=${KEYCLOAK_URL}/realms/carf
      - Redis__ConnectionString=${REDIS_URL}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      start_period: 60s
      retries: 3
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - backend-network
      - frontend-network

  geoweb:
    image: carf/geoweb:${GEOWEB_VERSION:-latest}
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '1'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 128M
      restart_policy:
        condition: on-failure
    ports:
      - "3000:3000"
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    networks:
      - frontend-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - geoapi
      - geoweb
    networks:
      - frontend-network

networks:
  backend-network:
    driver: bridge
    internal: true  # Não expõe externamente
  frontend-network:
    driver: bridge
```

## Environment File (.env.prod)

```bash
# .env.prod (gitignored)
GEOAPI_VERSION=1.2.3
GEOWEB_VERSION=1.2.3
DATABASE_URL=Host=db.carf.com.br;Database=carf;Username=carf_prod;Password=***
KEYCLOAK_URL=https://keycloak.carf.com.br
REDIS_URL=redis.carf.com.br:6379,password=***
```

## Deploy

```bash
# Deploy com env específico
docker-compose -f docker-compose.prod.yml --env-file .env.prod up -d

# Rolling update
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d --no-deps geoapi

# Verificar saúde
docker-compose -f docker-compose.prod.yml ps
docker-compose -f docker-compose.prod.yml exec geoapi curl localhost:8080/health
```

## Diferenças de Produção

| Aspecto | Dev | Prod |
|---------|-----|------|
| Imagem | build local | registry |
| Volumes | code mount | nenhum |
| Replicas | 1 | 3+ |
| Resources | ilimitado | limits |
| Restart | no | on-failure |
| Logging | stdout | json-file |
| Network | exposed | internal |

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
