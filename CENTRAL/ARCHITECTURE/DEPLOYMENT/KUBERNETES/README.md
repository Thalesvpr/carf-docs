# KUBERNETES

Manifests Kubernetes CARF usando Kustomize BASE contém manifests genéricos Deployment Service Ingress ConfigMap Secret templates sem environment-specific values OVERLAYS contém customizações ambiente DEV uma replica resources requests baixos PROD três replicas HPA autoscaling resources limits liveness readiness probes agressivos kustomization arquivo cada overlay referencia base aplica patches replicas image tags env vars deploy kubectl apply k overlays prod namespaces separados carf-dev carf-staging carf-prod RBAC ServiceAccounts RoleBindings limitando permissions garantindo isolamento segurança configuração declarativa versionada Git facilitando rollback disaster recovery infrastructure as code.

## Estrutura

- **[BASE/](./BASE/README.md)** - Manifests genéricos Deployment Service Ingress ConfigMap Secret templates
- **[OVERLAYS/](./OVERLAYS/README.md)** - Customizações ambiente DEV PROD patches replicas resources HPA PDB

---

**Última atualização:** 2026-01-11
