# KUBERNETES

Manifests Kubernetes do CARF usando Kustomize. BASE contém manifests genéricos (Deployment, Service, Ingress, ConfigMap, Secret templates) sem environment-specific values. OVERLAYS contém customizações por ambiente (DEV com 1 replica, resources requests baixos; PROD com 3 replicas, HPA autoscaling, resources limits, liveness/readiness probes agressivos). Kustomization.yaml em cada overlay referencia base/ e aplica patches (replicas, image tags, env vars). Deploy: kubectl apply -k overlays/prod/. Namespaces separados: carf-dev, carf-staging, carf-prod. RBAC com ServiceAccounts e RoleBindings limitando permissions.

## Estrutura

- **[BASE/](./BASE/README.md)** - Manifests Kubernetes base genéricos (Deployment, Service, Ingress, ConfigMap, Secret)
- **[OVERLAYS/](./OVERLAYS/README.md)** - Customizações por ambiente usando Kustomize
  - [DEV/](./OVERLAYS/DEV/README.md) - Configurações desenvolvimento (1 replica, recursos baixos)
  - [PROD/](./OVERLAYS/PROD/README.md) - Configurações produção (3+ replicas, HPA, recursos altos)

---

**Última atualização:** 2025-12-29
