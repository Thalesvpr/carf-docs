# Build Custom Docker Image

Build de imagem Docker customizada Keycloak CARF nível intermediário requer Docker e registry credentials. Build com tag version docker build -t carf/keycloak:1.0.0 ., tag latest docker tag carf/keycloak:1.0.0 carf/keycloak:latest, verificar size docker images grep carf/keycloak.

Testar localmente rodando docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin carf/keycloak:1.0.0 start-dev, verificar temas incluídos docker exec container ls /opt/keycloak/themes/carf.

Push para registry Docker Hub via docker login depois docker tag para username/carf-keycloak:1.0.0 e docker push. AWS ECR via aws ecr get-login-password --region us-east-1 pipe docker login --username AWS, tag para 123456789.dkr.ecr.us-east-1.amazonaws.com/carf-keycloak:1.0.0 e push. Azure ACR via az acr login --name carfregistry, tag para carfregistry.azurecr.io/carf-keycloak:1.0.0 e push.

Scan vulnerabilidades com Trivy docker run aquasec/trivy image carf/keycloak:1.0.0 ou Snyk via snyk container test carf/keycloak:1.0.0. Otimização de tamanho via multi-stage build já implementado no Dockerfile atual, reduzir layers combinando comandos RUN mkdir && cp ao invés de múltiplos RUNs separados.

Estratégia de tagging usando semantic versioning Major.Minor.Patch como 1.0.0, Git SHA via docker tag com git rev-parse --short HEAD, build number CI/CD via build-${BUILD_NUMBER}. Automação via Makefile com make build para build image, make deploy para build e push, make deploy VERSION=1.0.0 para versão específica.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Pronto
