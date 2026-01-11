# OVERLAYS

Kustomize overlays customizando base por ambiente. Estrutura: cada ambiente (DEV, PROD) tem pasta com kustomization.yaml referenciando ../../base/ e aplicando patches. Patches: replicas (dev: 1, prod: 3), image tags (dev: latest, prod: v1.2.3 SHA), resources (dev: requests 100m/128Mi, prod: requests 500m/512Mi limits 1000m/1Gi), env vars (DATABASE_HOST diferentes), ingress hosts (dev: dev-api.carf, prod: api.carf). HPA em prod (minReplicas 3, maxReplicas 10, targetCPUUtilizationPercentage 70). PodDisruptionBudget prod garantindo availability durante rolling updates.

## Ambientes

- **[DEV/](./DEV/README.md)** - Overlay desenvolvimento (1 replica, recursos mínimos, image:latest)
- **[PROD/](./PROD/README.md)** - Overlay produção (3+ replicas, HPA, resources limits, versões fixas)

---

**Última atualização:** 2025-12-29
