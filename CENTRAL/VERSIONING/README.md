# VERSIONING - Estratégia Versionamento CARF

Estratégia versionamento completa CARF abrangendo ferramenta controle versão Git plataforma hospedagem GitHub e esquema numeração Semantic Versioning coordenando releases polyrepo cinco projetos independentes GEOAPI GEOWEB REURBCAD GEOGIS WEBDOCS garantindo compatibilidade rastreabilidade gestão dependências comunicação clara significado mudanças stakeholders desenvolvedores operações usuários finais. Estrutura organiza 01-git-decision.md justificando escolha Git ferramenta distribuída performance branching merging workflows offline-first ecossistema ferramentas comunidade documentação treinamento configurações recomendadas integração CI/CD. 02-github-decision.md justificando escolha GitHub plataforma colaboração pull requests code review issues actions marketplace segurança Dependabot CodeQL configurações organização teams permissions branch protection workflows secrets. 03-semantic-versioning.md especificando formato MAJOR.MINOR.PATCH estratégia releases changelog API versioning database migrations coordenação polyrepo dependencies compatibilidade. GIT/ subdiretório contém workflow polyrepo branching strategy trunk-based commit conventions conventional commits PR guidelines review approval hooks pre-commit post-commit release coordination tags triggers CI/CD pipelines automated deployments.

## Estrutura Diretório

### 01-git-decision.md
Decisão escolha Git ferramenta controle versão justificativa alternativas consideradas Mercurial SVN Perforce CVS configurações recomendadas user.name user.email autocrlf pull.rebase aliases úteis Git LFS Large File Storage binários integração CI/CD GitHub Actions webhooks notificações treinamento time onboarding fundamentals advanced topics resources Pro Git book tutorials.

### 02-github-decision.md
Decisão escolha GitHub plataforma hospedagem justificativa alternativas consideradas GitLab Bitbucket Azure Repos self-hosted Gitea configurações organização teams permissions branch protection code owners workflows secrets self-hosted runners Dependabot CodeQL segurança colaboração issues pull requests community transparency accountability.

### 03-semantic-versioning.md
Formato versionamento MAJOR.MINOR.PATCH estratégia releases coordenadas polyrepo changelog manutenção CHANGELOG.md conventional commits API versioning header api-version database migrations additive deprecate before remove coordenação sprint planning dependencies compatibility integration testing QA regression prevention.

### GIT/
Subdiretório contendo workflow Git específico projeto incluindo 00-setup-guide.md instalação configuração inicial 01-polyrepo-strategy.md justificativa múltiplos repositórios versus monorepo 02-branching-strategy.md trunk-based development feature branches short-lived max 2 dias 03-commit-conventions.md conventional commits feat fix docs style refactor test chore 04-pr-guidelines.md pull request process review approval checklist 05-git-hooks.md pre-commit lint staged post-commit notifications 06-release-coordination.md coordenação releases tags versões compatíveis dependencies.

## Fluxo Versionamento Típico

Desenvolvimento feature inicia branch feature/RF-123-nova-funcionalidade commits convencionais feat(units): add polygon validation commits atômicos focados single responsibility pull request criado reviewers solicitados dois approvals mínimo CI checks passing lint tests coverage gates merge squash main branch preservando histórico limpo. Release preparação tag v1.5.0 criada trigger CI/CD build test deploy staging smoke tests validação funcional QA exploratory testing aprovação stakeholders deploy production blue-green zero downtime monitoring error rates latency health checks alerting incidents rollback automático se necessário. Changelog atualizado CHANGELOG.md documentando mudanças Added Changed Fixed Security comunicando usuários release notes GitHub publicadas compatibilidade especificada GEOAPI v1.5.0 requires GEOWEB v2.3.x REURBCAD v0.8.5+ dependencies claras evitando combinações incompatíveis.

## Relacionado

Ver também ARCHITECTURE/DEPLOYMENT/ estratégias deployment CI/CD pipelines containerização Kubernetes OPERATIONS/MAINTENANCE/ procedimentos manutenção updates patches OPERATIONS/MONITORING/ observability métricas logs traces alerting REQUIREMENTS/ rastreabilidade requisitos features código releases validação cobertura completeness.

---

**Última atualização:** 2025-01-08
