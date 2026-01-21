---
status: rejected
description: "Conteudo operacional. Configs de deploy pertencem a PROJECTS ou infra repo separado."
updated: 2026-01-15
---

# DEPLOYMENT

Estratégias de deployment do CARF cobrindo os diferentes ambientes e plataformas onde o sistema é executado.

Os [ambientes](01-environments.md) incluem desenvolvimento local com Docker Compose, staging em cloud para homologação de releases, e produção em Kubernetes multi-node. A [containerização](02-containerization.md) usa Docker com multi-stage builds. A [orquestração](03-orchestration.md) é feita com Kubernetes e Kustomize para customizações por ambiente.

O [pipeline CI/CD](04-cicd-pipeline.md) usa GitHub Actions para build, test e deploy automatizado com blue-green deployment e rollback. O [deployment mobile](05-mobile-deployment.md) cobre publicação na App Store e Google Play. E os [sites estáticos](06-static-site-deployment.md) usam GitHub Pages e Netlify.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (10 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Configs](CENTRAL/DEPLOYMENTS/CONFIGS/README.md) | 2 |
|  | [Docker](CENTRAL/DEPLOYMENTS/DOCKER/README.md) | 4 |
|  | [Kubernetes](CENTRAL/DEPLOYMENTS/KUBERNETES/README.md) | 4 |

*Gerado automaticamente em 2026-01-17 11:57*

## Arquivos (6 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-environments](01-environments.md) | Environments |
| [02-containerization](02-containerization.md) | Containerization |
| [03-orchestration](03-orchestration.md) | Orchestration |
| [04-cicd-pipeline](04-cicd-pipeline.md) | CI/CD Pipeline |
| [05-mobile-deployment](05-mobile-deployment.md) | Mobile Deployment |
| [06-static-site-deployment](06-static-site-deployment.md) | Static Site Deployment |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/DEPLOYMENTS/CONFIGS/README|CONFIGS]]
- [[CENTRAL/DEPLOYMENTS/DOCKER/README|DOCKER]]
- [[CENTRAL/DEPLOYMENTS/KUBERNETES/README|KUBERNETES]]

## Documentos

### Em Revisão

- ○ [[CENTRAL/DEPLOYMENTS/01-environments.md|Environments]]
- ○ [[CENTRAL/DEPLOYMENTS/02-containerization.md|Containerization]]
- ○ [[CENTRAL/DEPLOYMENTS/03-orchestration.md|Orchestration]]
- ○ [[CENTRAL/DEPLOYMENTS/04-cicd-pipeline.md|CI/CD Pipeline]]
- ○ [[CENTRAL/DEPLOYMENTS/05-mobile-deployment.md|Mobile Deployment]]
- ○ [[CENTRAL/DEPLOYMENTS/06-static-site-deployment.md|Static Site Deployment]]

<!-- CARF-INDEX-END -->
