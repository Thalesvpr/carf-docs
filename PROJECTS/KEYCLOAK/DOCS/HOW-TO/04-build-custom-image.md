# Build Custom Docker Image

**Nível**: Intermediário | **Tempo**: 10-15 minutos

## Build

```bash
# Build com tag version
docker build -t carf/keycloak:1.0.0 .

# Tag latest
docker tag carf/keycloak:1.0.0 carf/keycloak:latest

# Verificar size
docker images | grep carf/keycloak
```

## Test Local

```bash
docker run -p 8080:8080 \
  -e KEYCLOAK_ADMIN=admin \
  -e KEYCLOAK_ADMIN_PASSWORD=admin \
  carf/keycloak:1.0.0 start-dev

# Verificar temas incluídos
docker exec <container> ls /opt/keycloak/themes/carf
```

## Push para Registry

### Docker Hub
```bash
docker login
docker tag carf/keycloak:1.0.0 username/carf-keycloak:1.0.0
docker push username/carf-keycloak:1.0.0
```

### AWS ECR
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin 123456789.dkr.ecr.us-east-1.amazonaws.com

docker tag carf/keycloak:1.0.0 123456789.dkr.ecr.us-east-1.amazonaws.com/carf-keycloak:1.0.0
docker push 123456789.dkr.ecr.us-east-1.amazonaws.com/carf-keycloak:1.0.0
```

### Azure ACR
```bash
az acr login --name carfregistry
docker tag carf/keycloak:1.0.0 carfregistry.azurecr.io/carf-keycloak:1.0.0
docker push carfregistry.azurecr.io/carf-keycloak:1.0.0
```

## Scan Vulnerabilities

```bash
# Trivy
docker run aquasec/trivy image carf/keycloak:1.0.0

# Snyk
snyk container test carf/keycloak:1.0.0
```

## Optimize Image Size

### Multi-stage Build
Já implementado no Dockerfile atual.

### Reduce Layers
```dockerfile
# Bad (multiple layers)
RUN mkdir /opt/themes
RUN cp themes /opt/themes

# Good (single layer)
RUN mkdir /opt/themes && cp themes /opt/themes
```

## Tagging Strategy

```bash
# Semantic versioning
1.0.0 - Major.Minor.Patch

# Git SHA
docker tag carf/keycloak:1.0.0 carf/keycloak:$(git rev-parse --short HEAD)

# Build number (CI/CD)
docker tag carf/keycloak:1.0.0 carf/keycloak:build-${BUILD_NUMBER}
```

## Automation via Makefile

```bash
make build          # Build image
make deploy         # Build + push
make deploy VERSION=1.0.0
```
