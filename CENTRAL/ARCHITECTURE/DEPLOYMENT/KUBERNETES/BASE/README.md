# BASE

Diretório base contém manifests Kubernetes genéricos do sistema CARF compartilhados entre todos ambientes servindo como foundation para overlays específicos de dev staging e produção através de Kustomize permitindo DRY principle onde configurações comuns ficam centralizadas e overlays apenas sobrescrevem valores específicos de cada ambiente como replicas resource limits hostnames e secrets, backend GEOAPI definido via Deployment especificando container image geoapi com env vars extraídas ConfigMap Secret resources requests limits placeholders livenessProbe readinessProbe, Service type ClusterIP expondo port 80 interno mapeando targetPort 8080 container selector app geoapi, Ingress rules definindo host api.carf.example.com path direcionando backend TLS habilitado cert-manager annotations provisioning automático certificados Let's Encrypt, database PostgreSQL implementado StatefulSet garantindo pods identidade persistente ordenação startup volumeClaimTemplates persistent storage automático criando PVC por pod preservando dados restarts, demais serviços incluem Keycloak SSO OAuth2 Redis cache distribuído GEOWEB nginx servindo static assets frontend SPA RabbitMQ message broker ConfigMap Secret templates, arquivo kustomization.yaml lista todos resources manifests agregando base reutilizável overlays através kustomize build comando gerando manifests finais merged.

## Manifests Base

- **[geoapi-deployment.yaml](./geoapi-deployment.yaml)** - Deployment GEOAPI backend .NET container image env vars health probes
- **[geoapi-service.yaml](./geoapi-service.yaml)** - Service ClusterIP GEOAPI port 80 targetPort 8080
- **[geoapi-ingress.yaml](./geoapi-ingress.yaml)** - Ingress rules host TLS cert-manager annotations Let's Encrypt
- **[geoweb-deployment.yaml](./geoweb-deployment.yaml)** - Deployment GEOWEB frontend nginx static assets SPA
- **[geoweb-service.yaml](./geoweb-service.yaml)** - Service ClusterIP GEOWEB port 80
- **[postgres-statefulset.yaml](./postgres-statefulset.yaml)** - StatefulSet PostgreSQL volumeClaimTemplates persistent storage PVC
- **[keycloak-deployment.yaml](./keycloak-deployment.yaml)** - Deployment Keycloak SSO OAuth2 autenticação
- **[redis-deployment.yaml](./redis-deployment.yaml)** - Deployment Redis cache distribuído sessions
- **[rabbitmq-deployment.yaml](./rabbitmq-deployment.yaml)** - Deployment RabbitMQ message broker async processing
- **[configmap-template.yaml](./configmap-template.yaml)** - ConfigMap template variáveis não sensíveis environment
- **[secret-template.yaml](./secret-template.yaml)** - Secret template credenciais database Keycloak JWT
- **[kustomization.yaml](./kustomization.yaml)** - Kustomize base aggregating resources manifests

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: o ramo inteiro esta incompleto. Precisa de supervisão para corrigir.

