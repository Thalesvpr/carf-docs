---
type: readme
status: rejected
description: "Conteudo operacional. Configs de deploy pertencem a PROJECTS ou infra repo separado."
updated: 2026-01-15
---

# OVERLAYS

Kustomize overlays customizando base por ambiente. Estrutura: cada ambiente (DEV, PROD) tem pasta com kustomization.yaml referenciando ../../base/ e aplicando patches. Patches: replicas (dev: 1, prod: 3), image tags (dev: latest, prod: v1.2.3 SHA), resources (dev: requests 100m/128Mi, prod: requests 500m/512Mi limits 1000m/1Gi), env vars (DATABASE_HOST diferentes), ingress hosts (dev: dev-api.carf, prod: api.carf). HPA em prod (minReplicas 3, maxReplicas 10, targetCPUUtilizationPercentage 70). PodDisruptionBudget prod garantindo availability durante rolling updates.

## Ambientes

- **[DEV](CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/DEV/README.md)** - Configuração desenvolvimento
- **[PROD](CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/PROD/README.md)** - Configuração produção


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (2 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Dev](CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/DEV/README.md) | 1 |
|  | [Prod](CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/PROD/README.md) | 1 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/DEV/README|DEV]]
- [[CENTRAL/DEPLOYMENTS/KUBERNETES/OVERLAYS/PROD/README|PROD]]

<!-- CARF-INDEX-END -->
