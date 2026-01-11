# DEPLOYMENT

Estratégia de deployment do CARF documentando ambientes (dev local com docker-compose, staging em cloud homologando releases, prod em Kubernetes multi-node), infraestrutura cloud (AWS EKS ou Azure AKS com managed PostgreSQL RDS/Azure Database, load balancer ALB/Application Gateway, CDN CloudFront/Azure CDN para assets estáticos) e on-premises (Kubernetes on bare-metal, PostgreSQL self-hosted com replicação, HAProxy load balancer), pipeline CI/CD (GitHub Actions: push→build→test→docker build→push registry→deploy staging→smoke tests→deploy prod com approval manual), estratégia blue-green deployment para zero-downtime (manter versão antiga rodando até nova passar health checks), canary releases (liberar 10% tráfego para nova versão, monitorar error rate, gradualmente aumentar), e rollback procedures (reverter deployment via kubectl rollout undo, restaurar database de snapshot se necessário).

## Estrutura de Configurações

Configurações de deployment organizadas em DOCKER (subpasta DOCKERFILES/ com Dockerfile para cada projeto, COMPOSE/ com docker-compose.yml para dev/staging/prod orquestrando containers de GEOAPI, PostgreSQL, Keycloak, Redis, e GEOWEB servido via nginx), KUBERNETES (subpasta BASE/ com manifests genéricos de Deployment, Service, Ingress, ConfigMap, Secret; OVERLAYS/ com customizações por ambiente usando Kustomize), e CONFIGS (nginx.conf para reverse proxy e SSL termination, env-vars.md documentando variáveis de ambiente obrigatórias/opcionais por projeto, health checks endpoints).

## Documentação Detalhada

### Pipeline CI/CD
- **[04-cicd-pipeline.md](./04-cicd-pipeline.md)** - Pipeline completo GitHub Actions: build → test → deploy

### Containerização Docker
- **[02-containerization.md](./02-containerization.md)** - Estratégia de containerização e Docker best practices
- **[DOCKER/](./DOCKER/README.md)** - Dockerfiles por projeto, docker-compose para orquestração local/staging
  - [DOCKERFILES/](./DOCKER/DOCKERFILES/README.md) - Dockerfiles multi-stage otimizados por projeto
  - [COMPOSE/](./DOCKER/COMPOSE/README.md) - Docker Compose files para dev/staging/prod

### Orquestração Kubernetes
- **[KUBERNETES/](./KUBERNETES/README.md)** - Manifests Kubernetes com Kustomize para customização por ambiente
  - [BASE/](./KUBERNETES/BASE/README.md) - Manifests base genéricos (Deployment, Service, Ingress)
  - [OVERLAYS/](./KUBERNETES/OVERLAYS/README.md) - Customizações por ambiente
    - [DEV/](./KUBERNETES/OVERLAYS/DEV/README.md) - Configurações desenvolvimento
    - [PROD/](./KUBERNETES/OVERLAYS/PROD/README.md) - Configurações produção

### Configurações e Variáveis
- **[CONFIGS/](./CONFIGS/README.md)** - Arquivos de configuração nginx, variáveis de ambiente, health checks
  - [env-vars.md](./CONFIGS/env-vars.md) - Variáveis de ambiente por projeto
  - [health-checks.md](./CONFIGS/health-checks.md) - Endpoints e estratégias de health checking

### Deployments Específicos
- [06-static-site-deployment.md](./06-static-site-deployment.md) - Deploy de sites estáticos (WEBDOCS) em GitHub Pages/Netlify

---

**Última atualização:** 2025-12-29
