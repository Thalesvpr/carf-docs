# GIT

Workflow Git para o polyrepo CARF com seis repositórios independentes.

O [setup](./00-setup-guide.md) cobre clone dos repos e configuração de SSH keys. A [estratégia polyrepo](./01-polyrepo-strategy.md) justifica repositórios separados para deployment independente e ownership claro.

A [branching strategy](./02-branching-strategy.md) usa trunk-based development com feature branches curtas onde main está sempre deployable. Os [commit conventions](./03-commit-conventions.md) seguem Conventional Commits para changelog automático.

As [PR guidelines](./04-pr-guidelines.md) definem templates e checklist de code review com CI checks obrigatórios. Os [git hooks](./05-git-hooks.md) rodam linting no pre-commit, validam mensagens no commit-msg e executam testes no pre-push.

A [coordenação de releases](./06-release-coordination.md) mantém compatibility matrix entre projetos. O [guia de worktree](./07-worktree-guide.md) permite trabalho paralelo em múltiplas branches.

## Documentos

- **[00-setup-guide.md](./00-setup-guide.md)** - Clone e configuração inicial
- **[01-polyrepo-strategy.md](./01-polyrepo-strategy.md)** - Estratégia de repositórios separados
- **[02-branching-strategy.md](./02-branching-strategy.md)** - Trunk-based development
- **[03-commit-conventions.md](./03-commit-conventions.md)** - Conventional Commits
- **[04-pr-guidelines.md](./04-pr-guidelines.md)** - Pull request e code review
- **[05-git-hooks.md](./05-git-hooks.md)** - Hooks de linting e testes
- **[06-release-coordination.md](./06-release-coordination.md)** - Coordenação entre projetos
- **[07-worktree-guide.md](./07-worktree-guide.md)** - Trabalho paralelo com worktrees

---

**Última atualização:** 2026-01-14
