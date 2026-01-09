# DEPLOYMENT

Estratégia de deployment do CARF documentando ambientes (dev local com docker-compose, staging em cloud homologando releases, prod em Kubernetes multi-node), infraestrutura cloud (AWS EKS ou Azure AKS com managed PostgreSQL RDS/Azure Database, load balancer ALB/Application Gateway, CDN CloudFront/Azure CDN para assets estáticos) e on-premises (Kubernetes on bare-metal, PostgreSQL self-hosted com replicação, HAProxy load balancer), pipeline CI/CD (GitHub Actions: push→build→test→docker build→push registry→deploy staging→smoke tests→deploy prod com approval manual), estratégia blue-green deployment para zero-downtime (manter versão antiga rodando até nova passar health checks), canary releases (liberar 10% tráfego para nova versão, monitorar error rate, gradualmente aumentar), e rollback procedures (reverter deployment via kubectl rollout undo, restaurar database de snapshot se necessário).

## Estrutura de Configurações

Configurações de deployment organizadas em DOCKER (subpasta DOCKERFILES/ com Dockerfile para cada projeto, COMPOSE/ com docker-compose.yml para dev/staging/prod orquestrando containers de GEOAPI, PostgreSQL, Keycloak, Redis, e GEOWEB servido via nginx), KUBERNETES (subpasta BASE/ com manifests genéricos de Deployment, Service, Ingress, ConfigMap, Secret; OVERLAYS/ com customizações por ambiente usando Kustomize), e CONFIGS (nginx.conf para reverse proxy e SSL termination, env-vars.md documentando variáveis de ambiente obrigatórias/opcionais por projeto, health checks endpoints).

---

**Última atualização:** 2025-12-29
