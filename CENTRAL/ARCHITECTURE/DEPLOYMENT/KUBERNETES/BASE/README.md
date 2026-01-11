# BASE

Diretório base contém manifests Kubernetes genéricos do sistema CARF compartilhados entre todos ambientes servindo como foundation para overlays específicos de dev staging e produção através de Kustomize permitindo DRY principle onde configurações comuns ficam centralizadas e overlays apenas sobrescrevem valores específicos de cada ambiente como replicas resource limits hostnames e secrets.

Backend GEOAPI definido via geoapi-deployment.yaml Deployment especificando container image geoapi com env vars extraídas de ConfigMap para configurações não sensíveis e Secret para credenciais database Keycloak JWT, resources requests e limits como placeholders a serem sobrescritos por overlay, livenessProbe HTTP GET /health periodSeconds 10 e readinessProbe HTTP GET /ready initialDelaySeconds 30, geoapi-service.yaml Service type ClusterIP expondo port 80 interno mapeando para targetPort 8080 do container com selector app igual geoapi, geoapi-ingress.yaml Ingress rules definindo host api.carf.example.com path / direcionando para backend geoapi-service com TLS habilitado usando cert-manager annotations para provisioning automático de certificados Let's Encrypt.

Database PostgreSQL implementado via postgres-statefulset.yaml StatefulSet garantindo pods com identidade persistente e ordenação de startup usando volumeClaimTemplates para persistent storage automático criando PVC por pod preservando dados entre restarts, postgres-config ConfigMap contendo initialization scripts SQL e postgres-secret Secret com POSTGRES_PASSWORD protegido. Demais serviços incluem keycloak-deployment.yaml para SSO OAuth2, redis-deployment.yaml para cache distribuído, geoweb-deployment.yaml com nginx servindo static assets do frontend SPA. Arquivo kustomization.yaml lista todos resources manifests agregando como base reutilizável por overlays dev staging prod através de kustomize build comando gerando manifests finais merged.

---

**Última atualização:** 2026-01-10
