# DEPLOYMENT

Estratégia deployment CARF documentando ambientes dev local docker-compose staging cloud homologando releases prod Kubernetes multi-node infraestrutura cloud AWS EKS Azure AKS managed PostgreSQL RDS Azure Database load balancer ALB Application Gateway CDN CloudFront Azure CDN assets estáticos on-premises Kubernetes bare-metal PostgreSQL self-hosted replicação HAProxy load balancer pipeline CI/CD GitHub Actions push build test docker build push registry deploy staging smoke tests deploy prod approval manual blue-green deployment zero-downtime canary releases liberar dez por cento tráfego nova versão monitorar error rate gradualmente aumentar rollback procedures reverter deployment kubectl rollout undo restaurar database snapshot necessário configurações organizadas DOCKER subpasta DOCKERFILES Dockerfile cada projeto COMPOSE docker-compose orquestrando containers KUBERNETES BASE manifests genéricos Deployment Service Ingress ConfigMap Secret OVERLAYS customizações ambiente Kustomize CONFIGS nginx reverse proxy SSL termination env-vars variáveis ambiente health checks endpoints.

## Documentos

- **[01-environments.md](./01-environments.md)** - Ambientes dev staging prod
- **[02-containerization.md](./02-containerization.md)** - Docker multi-stage builds security
- **[03-orchestration.md](./03-orchestration.md)** - Kubernetes Kustomize overlays
- **[04-cicd-pipeline.md](./04-cicd-pipeline.md)** - GitHub Actions workflow completo
- **[05-mobile-deployment.md](./05-mobile-deployment.md)** - React Native App Store Google Play
- **[06-static-site-deployment.md](./06-static-site-deployment.md)** - VitePress GitHub Pages Netlify

## Configurações

- **[DOCKER/](./DOCKER/README.md)** - Dockerfiles multi-stage docker-compose orquestração containers
- **[KUBERNETES/](./KUBERNETES/README.md)** - Manifests Kustomize BASE OVERLAYS patches ambiente
- **[CONFIGS/](./CONFIGS/README.md)** - Nginx reverse proxy SSL env-vars health checks

---

**Última atualização:** 2026-01-11
