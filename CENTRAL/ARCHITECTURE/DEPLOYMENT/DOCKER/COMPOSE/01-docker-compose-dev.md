# Docker Compose Development

Configuração Docker Compose para ambiente de desenvolvimento local.

## docker-compose.dev.yml

```yaml
version: '3.8'

services:
  geoapi:
    build:
      context: ./GEOAPI
      dockerfile: Dockerfile.geoapi
      target: build  # Para hot reload
    ports:
      - "5000:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
      - ConnectionStrings__DefaultConnection=Host=postgres;Database=carf;Username=carf;Password=carf123
      - Keycloak__Authority=http://keycloak:8080/realms/carf
      - Redis__ConnectionString=redis:6379
    volumes:
      - ./GEOAPI/src:/src  # Hot reload
    depends_on:
      postgres:
        condition: service_healthy
      keycloak:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - backend-network
      - frontend-network

  geoweb:
    build:
      context: ./GEOWEB
      dockerfile: Dockerfile.geoweb
      target: deps
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:5000
      - NEXT_PUBLIC_KEYCLOAK_URL=http://localhost:8080
    volumes:
      - ./GEOWEB:/app
      - /app/node_modules  # Exclude node_modules
    command: npm run dev
    networks:
      - frontend-network

  postgres:
    image: postgis/postgis:16-3.4
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=carf
      - POSTGRES_USER=carf
      - POSTGRES_PASSWORD=carf123
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U carf -d carf"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend-network

  keycloak:
    image: quay.io/keycloak/keycloak:23.0
    ports:
      - "8080:8080"
    environment:
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=admin
      - KC_DB=postgres
      - KC_DB_URL=jdbc:postgresql://postgres:5432/keycloak
      - KC_DB_USERNAME=carf
      - KC_DB_PASSWORD=carf123
    command: start-dev --import-realm
    volumes:
      - ./keycloak/realm-export.json:/opt/keycloak/data/import/realm.json
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - backend-network
      - frontend-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - backend-network

volumes:
  postgres_data:
  redis_data:

networks:
  backend-network:
    driver: bridge
  frontend-network:
    driver: bridge
```

## Comandos

```bash
# Iniciar todos os serviços
docker-compose -f docker-compose.dev.yml up -d

# Ver logs
docker-compose -f docker-compose.dev.yml logs -f geoapi

# Rebuild após mudança no Dockerfile
docker-compose -f docker-compose.dev.yml up -d --build geoapi

# Parar tudo
docker-compose -f docker-compose.dev.yml down

# Limpar volumes (reset DB)
docker-compose -f docker-compose.dev.yml down -v
```

## Hot Reload

- **GEOAPI**: Volume mount + `dotnet watch` no container
- **GEOWEB**: Volume mount + `npm run dev`
- Mudanças refletem sem rebuild

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
