# DEPLOYMENT

Estratégias de deployment do CARF cobrindo os diferentes ambientes e plataformas onde o sistema é executado.

Os [ambientes](./01-environments.md) incluem desenvolvimento local com Docker Compose, staging em cloud para homologação de releases, e produção em Kubernetes multi-node. A [containerização](./02-containerization.md) usa Docker com multi-stage builds. A [orquestração](./03-orchestration.md) é feita com Kubernetes e Kustomize para customizações por ambiente.

O [pipeline CI/CD](./04-cicd-pipeline.md) usa GitHub Actions para build, test e deploy automatizado com blue-green deployment e rollback. O [deployment mobile](./05-mobile-deployment.md) cobre publicação na App Store e Google Play. E os [sites estáticos](./06-static-site-deployment.md) usam GitHub Pages e Netlify.

## Documentos

- **[01-environments.md](./01-environments.md)** - Ambientes dev, staging e prod
- **[02-containerization.md](./02-containerization.md)** - Docker multi-stage builds
- **[03-orchestration.md](./03-orchestration.md)** - Kubernetes e Kustomize
- **[04-cicd-pipeline.md](./04-cicd-pipeline.md)** - GitHub Actions workflow
- **[05-mobile-deployment.md](./05-mobile-deployment.md)** - App Store e Google Play
- **[06-static-site-deployment.md](./06-static-site-deployment.md)** - GitHub Pages e Netlify

## Configurações

- **[CONFIGS/](./CONFIGS/README.md)** - Variáveis de ambiente e health checks
- **[DOCKER/](./DOCKER/README.md)** - Dockerfiles e Compose
- **[KUBERNETES/](./KUBERNETES/README.md)** - Manifests base e overlays

---

**Última atualização:** 2026-01-14
