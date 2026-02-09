---
type: leaf
status: review
updated: 2026-02-08
---

# Build Custom Docker Image

O build de imagem Docker customizada para o Keycloak CARF e um procedimento de nivel intermediario que requer Docker instalado e credenciais de acesso ao registry de destino.

## Build e Tagging Local

O build e feito com `docker build -t carf/keycloak:1.0.0 .` seguido do tag latest com `docker tag carf/keycloak:1.0.0 carf/keycloak:latest`. Para verificar o tamanho da imagem resultante, executar `docker images | grep carf/keycloak`.

## Teste Local

Para testar a imagem localmente, executar `docker run -p 8080:8080 -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin carf/keycloak:1.0.0 start-dev`. Verificar que os temas estao incluidos com `docker exec <container> ls /opt/keycloak/themes/carf`.

## Push para Registry

O procedimento de push varia conforme o registry de destino.

| Registry   | Autenticacao                                                                                      | Tag                                                                   | Push              |
|------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|--------------------|
| Docker Hub | `docker login`                                                                                   | `docker tag carf/keycloak:1.0.0 username/carf-keycloak:1.0.0`        | `docker push`     |
| AWS ECR    | `aws ecr get-login-password --region us-east-1 \| docker login --username AWS`                   | `docker tag carf/keycloak:1.0.0 123456789.dkr.ecr.us-east-1.amazonaws.com/carf-keycloak:1.0.0` | `docker push` |
| Azure ACR  | `az acr login --name carfregistry`                                                               | `docker tag carf/keycloak:1.0.0 carfregistry.azurecr.io/carf-keycloak:1.0.0` | `docker push` |

## Scan de Vulnerabilidades

A verificacao de seguranca da imagem pode ser feita com Trivy via `docker run aquasec/trivy image carf/keycloak:1.0.0` ou com Snyk via `snyk container test carf/keycloak:1.0.0`. Essas ferramentas identificam vulnerabilidades conhecidas nas camadas da imagem e dependencias.

## Otimizacao de Tamanho

O Dockerfile atual ja utiliza multi-stage build para reduzir o tamanho final da imagem. Para otimizacoes adicionais, reduzir o numero de layers combinando comandos RUN (por exemplo `RUN mkdir -p /dir && cp file /dir/` ao inves de multiplos RUNs separados).

## Estrategia de Tagging

O projeto adota semantic versioning no formato Major.Minor.Patch (exemplo: `1.0.0`). Alem da versao semantica, cada imagem pode receber tags adicionais com o Git SHA via `docker tag` usando `git rev-parse --short HEAD`, e com o build number do CI/CD no formato `build-${BUILD_NUMBER}`.

## Automacao via Makefile

O Makefile do projeto oferece comandos que simplificam o workflow de build e deploy.

| Comando                     | Descricao                          |
|-----------------------------|------------------------------------|
| `make build`                | Build da imagem Docker             |
| `make deploy`               | Build e push para o registry       |
| `make deploy VERSION=1.0.0` | Build e push com versao especifica |
