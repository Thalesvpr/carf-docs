---
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING."
updated: 2026-01-20
---

# GIT

Workflow Git para desenvolvimento no CARF com práticas padronizadas de branching, commits e colaboração.

O [guia de setup](./01-setup-guide.md) cobre clone dos repositórios, configuração de SSH keys e estrutura de diretórios local. A [branching strategy](./02-branching-strategy.md) usa trunk-based development com feature branches curtas onde main está sempre deployable.

Os [commit conventions](./03-commit-conventions.md) seguem Conventional Commits para changelog automático e mensagens padronizadas. As [PR guidelines](./04-pr-guidelines.md) definem templates e checklist de code review com CI checks obrigatórios. Os [git hooks](./05-git-hooks.md) rodam linting no pre-commit, validam mensagens no commit-msg e executam testes no pre-push.

O [guia de worktree](./06-worktree-guide.md) permite trabalho paralelo em múltiplas branches sem necessidade de stash ou múltiplos clones.

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/VERSIONING/GIT/01-setup-guide.md|Guia de Setup - CARF Polyrepo]]
- ○ [[CENTRAL/VERSIONING/GIT/02-branching-strategy.md|Branching Strategy]]
- ○ [[CENTRAL/VERSIONING/GIT/03-commit-conventions.md|Commit Conventions]]
- ○ [[CENTRAL/VERSIONING/GIT/04-pr-guidelines.md|PR Guidelines]]
- ○ [[CENTRAL/VERSIONING/GIT/05-git-hooks.md|Git Hooks]]
- ○ [[CENTRAL/VERSIONING/GIT/06-worktree-guide.md|Git Worktree - Trabalho Paralelo em Múltiplas Branches]]

<!-- CARF-INDEX-END -->
