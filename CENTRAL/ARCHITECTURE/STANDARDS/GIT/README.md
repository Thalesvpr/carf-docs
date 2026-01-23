---
type: readme
status: current
updated: 2026-01-22
---

# GIT

Workflow Git para desenvolvimento no CARF com praticas padronizadas de branching, commits e colaboracao.

O [guia de setup](./01-setup-guide.md) cobre clone dos repositorios, configuracao de SSH keys e estrutura de diretorios local. A [branching strategy](./02-branching-strategy.md) usa trunk-based development com feature branches curtas onde main esta sempre deployable.

Os [commit conventions](./03-commit-conventions.md) seguem Conventional Commits para changelog automatico e mensagens padronizadas. As [PR guidelines](./04-pr-guidelines.md) definem templates e checklist de code review com CI checks obrigatorios. Os [git hooks](./05-git-hooks.md) rodam linting no pre-commit, validam mensagens no commit-msg e executam testes no pre-push.

O [guia de worktree](./06-worktree-guide.md) permite trabalho paralelo em multiplas branches sem necessidade de stash ou multiplos clones.

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
