# GIT

Workflow Git para o polyrepo CARF com seis repositórios independentes.

O [setup](./00-setup-guide.md) cobre clone dos repos e configuração de SSH keys. A [estratégia polyrepo](./01-polyrepo-strategy.md) justifica repositórios separados para deployment independente e ownership claro.

A [branching strategy](./02-branching-strategy.md) usa trunk-based development com feature branches curtas onde main está sempre deployable. Os [commit conventions](./03-commit-conventions.md) seguem Conventional Commits para changelog automático.

As [PR guidelines](./04-pr-guidelines.md) definem templates e checklist de code review com CI checks obrigatórios. Os [git hooks](./05-git-hooks.md) rodam linting no pre-commit, validam mensagens no commit-msg e executam testes no pre-push.

A [coordenação de releases](./06-release-coordination.md) mantém compatibility matrix entre projetos. O [guia de worktree](./07-worktree-guide.md) permite trabalho paralelo em múltiplas branches.

---

**Última atualização:** 2026-01-14

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Pronto

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (8 arquivos)

| ID | Titulo |
|:---|:-------|
| [00-setup-guide](./00-setup-guide.md) | Guia de Setup - CARF Polyrepo |
| [01-polyrepo-strategy](./01-polyrepo-strategy.md) | Polyrepo Strategy |
| [02-branching-strategy](./02-branching-strategy.md) | Branching Strategy |
| [03-commit-conventions](./03-commit-conventions.md) | Commit Conventions |
| [04-pr-guidelines](./04-pr-guidelines.md) | PR Guidelines |
| [05-git-hooks](./05-git-hooks.md) | Git Hooks |
| [06-release-coordination](./06-release-coordination.md) | Release Coordination |
| [07-worktree-guide](./07-worktree-guide.md) | Git Worktree - Trabalho Paralelo em Múltiplas Branches |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
