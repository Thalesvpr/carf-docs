# DEPLOYMENT

Estratégias de deployment do CARF cobrindo os diferentes ambientes e plataformas onde o sistema é executado.

Os [ambientes](./01-environments.md) incluem desenvolvimento local com Docker Compose, staging em cloud para homologação de releases, e produção em Kubernetes multi-node. A [containerização](./02-containerization.md) usa Docker com multi-stage builds. A [orquestração](./03-orchestration.md) é feita com Kubernetes e Kustomize para customizações por ambiente.

O [pipeline CI/CD](./04-cicd-pipeline.md) usa GitHub Actions para build, test e deploy automatizado com blue-green deployment e rollback. O [deployment mobile](./05-mobile-deployment.md) cobre publicação na App Store e Google Play. E os [sites estáticos](./06-static-site-deployment.md) usam GitHub Pages e Netlify.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Aguardando (nova geração) index gerado por script.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (2 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Configs](./CONFIGS/README.md) | 2 |
|  | [Docker](./DOCKER/README.md) | 0 |
|  | [Kubernetes](./KUBERNETES/README.md) | 0 |

*Gerado automaticamente em 2026-01-15 17:41*

## Arquivos (6 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-environments](./01-environments.md) | Environments |
| [02-containerization](./02-containerization.md) | Containerization |
| [03-orchestration](./03-orchestration.md) | Orchestration |
| [04-cicd-pipeline](./04-cicd-pipeline.md) | CI/CD Pipeline |
| [05-mobile-deployment](./05-mobile-deployment.md) | Mobile Deployment |
| [06-static-site-deployment](./06-static-site-deployment.md) | Static Site Deployment |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
