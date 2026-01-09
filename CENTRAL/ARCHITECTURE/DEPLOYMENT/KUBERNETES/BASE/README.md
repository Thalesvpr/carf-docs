# BASE

Kubernetes base manifests genéricos do CARF. geoapi-deployment.yaml (Deployment com container geoapi, env vars from ConfigMap/Secret, resources requests/limits placeholders, liveness /health readiness /ready probes HTTP). geoapi-service.yaml (Service type ClusterIP port 80 targetPort 8080 selector app=geoapi). geoapi-ingress.yaml (Ingress rules host api.carf.example.com path / backend geoapi-service, TLS cert-manager annotations). postgres-statefulset.yaml (StatefulSet volumeClaimTemplates persistent storage, postgres-config ConfigMap, postgres-secret Secret). keycloak-deployment.yaml. redis-deployment.yaml. geoweb-deployment.yaml nginx serving static. kustomization.yaml listing all resources.

---

**Última atualização:** 2025-12-29
