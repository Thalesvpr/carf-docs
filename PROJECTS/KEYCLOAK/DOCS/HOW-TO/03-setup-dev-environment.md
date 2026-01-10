# Setup Ambiente de Desenvolvimento

**Nível**: Iniciante | **Tempo**: 15-20 minutos

## Pré-requisitos
- Docker Desktop instalado
- Git
- Editor: VS Code ou IntelliJ IDEA

## 1. Clone e Setup

```bash
git clone <repo>
cd PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak

# Gerar secrets
chmod +x scripts/generate-secrets.sh
./scripts/generate-secrets.sh

# Iniciar ambiente
make dev
# ou: docker-compose -f docker-compose.dev.yml up -d
```

## 2. Verificar Stack

```bash
# Check containers
docker ps | grep keycloak

# Check health
curl http://localhost:8080/health

# Check logs
docker logs -f carf-keycloak-dev
```

## 3. Acessar Admin Console

```
URL: http://localhost:8080
User: admin
Pass: admin
```

## 4. Hot Reload (Temas)

Temas montados via volume:
```yaml
# docker-compose.dev.yml
volumes:
  - ./themes:/opt/keycloak/themes:ro
```

Edite tema e recarregue browser (Ctrl+Shift+R).

## 5. IDE Setup

### VS Code

**.vscode/extensions.json**:
```json
{
  "recommendations": [
    "vscode-freemarker",
    "esbenp.prettier-vscode"
  ]
}
```

### IntelliJ IDEA (para SPIs Java)

1. Open `extensions/pom.xml`
2. Maven → Reload
3. Run → Edit Configurations → Remote JVM Debug
4. Host: localhost, Port: 8787

## 6. Debug Remoto (SPIs)

```bash
# Start com debug port
docker run -p 8080:8080 -p 8787:8787 \
  -e JAVA_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8787" \
  carf/keycloak:latest start-dev
```

Attach debugger no IntelliJ e set breakpoints.

## 7. Quick Iteration Loop

```bash
# 1. Edit tema
vim themes/carf/login/login.ftl

# 2. Reload browser
# Ctrl+Shift+R

# 3. Edit SPI
vim extensions/cpf-validator/src/main/java/...

# 4. Rebuild e redeploy
mvn clean package
docker cp target/*.jar container:/opt/keycloak/providers/
docker restart container
```

## Troubleshooting

**Tema não recarrega**: Limpar cache browser + Keycloak cache
**Port 8080 em uso**: `docker ps -a` e parar containers conflitantes
**PostgreSQL não inicia**: `docker volume rm carf-keycloak-postgres-data` e recriar

## Atalhos Úteis

```bash
make dev      # Start environment
make logs     # Tail logs
make health   # Health check
make clean    # Stop e remove tudo
make psql     # Connect PostgreSQL
```
