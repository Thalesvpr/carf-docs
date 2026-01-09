# GIT

Documentação de estratégia Git e workflow polyrepo do CARF. Documenta branching strategy (trunk-based development com feature branches curtas, main sempre deployable, releases via tags), workflow polyrepo (6 repositórios independentes: carf-docs/carf-geoapi/carf-geoweb/carf-reurbcad/carf-geogis/carf-webdocs), sincronização entre repos (compatibility matrix versionando dependências, coordenação releases via release notes), commit conventions (Conventional Commits para changelog automático), PR guidelines (templates, code review checklist, CI checks obrigatórios), e git hooks (pre-commit linting/formatting, commit-msg validando conventional commits, pre-push running tests). Define responsável por cada repo, permissões branches protegidas, e processo de hotfixes emergenciais.

## Documentos

| Arquivo | Descrição |
|---------|-----------|
| [00-setup-guide.md](00-setup-guide.md) | **Guia de setup completo** - Instruções passo a passo para clonar repositórios |
| [01-polyrepo-strategy.md](01-polyrepo-strategy.md) | Estratégia polyrepo e comandos de clone |
| [02-branching-strategy.md](02-branching-strategy.md) | Trunk-based development e workflow de branches |
| [03-commit-conventions.md](03-commit-conventions.md) | Conventional Commits e mensagens padronizadas |
| [04-pr-guidelines.md](04-pr-guidelines.md) | Guidelines para Pull Requests e code review |
| [05-git-hooks.md](05-git-hooks.md) | Hooks automáticos para qualidade de código |
| [06-release-coordination.md](06-release-coordination.md) | Coordenação de releases entre repositórios |
| [07-worktree-guide.md](07-worktree-guide.md) | Git worktree para trabalho paralelo em múltiplas branches |

## Quick Start

Novo no projeto? Comece aqui:

1. **Primeiro acesso:** Leia o [Guia de Setup](00-setup-guide.md)
2. **Clone os repositórios:** Siga os comandos em [Polyrepo Strategy](01-polyrepo-strategy.md)
3. **Aprenda o workflow:** Consulte [Branching Strategy](02-branching-strategy.md)
4. **Faça commits corretos:** Use [Commit Conventions](03-commit-conventions.md)
5. **Abra Pull Requests:** Siga [PR Guidelines](04-pr-guidelines.md)

---

**Última atualização:** 2026-01-08
