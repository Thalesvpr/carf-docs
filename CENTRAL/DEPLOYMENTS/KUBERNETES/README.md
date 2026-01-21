---
status: rejected
description: "Conteudo operacional. Configs de deploy pertencem a PROJECTS ou infra repo separado."
updated: 2026-01-15
---

# KUBERNETES

Manifests Kubernetes CARF usando Kustomize BASE contém manifests genéricos Deployment Service Ingress ConfigMap Secret templates sem environment-specific values OVERLAYS contém customizações ambiente DEV uma replica resources requests baixos PROD três replicas HPA autoscaling resources limits liveness readiness probes agressivos kustomization arquivo cada overlay referencia base aplica patches replicas image tags env vars deploy kubectl apply k overlays prod namespaces separados carf-dev carf-staging carf-prod RBAC ServiceAccounts RoleBindings limitando permissions garantindo isolamento segurança configuração declarativa versionada Git facilitando rollback disaster recovery infrastructure as code.

## Subpastas

- **[BASE](CENTRAL/DEPLOYMENTS/KUBERNETES/BASE/README.md)** - Manifests genéricos compartilhados
- **[OVERLAYS](CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/README.md)** - Customizações por ambiente


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (4 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Base](CENTRAL/DEPLOYMENTS/KUBERNETES/BASE/README.md) | 2 |
|  | [Overlays](CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/README.md) | 2 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/DEPLOYMENTS/KUBERNETES/BASE/README|BASE]]
- [[CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/README|OVERLAYS]]

<!-- CARF-INDEX-END -->
