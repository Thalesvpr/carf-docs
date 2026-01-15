# VERSIONING

Estratégia de versionamento do CARF coordenando releases entre os projetos independentes.

A [decisão por Git](./01-git-decision.md) justifica a escolha como ferramenta de controle de versão pela performance, branching, workflows offline-first e ecossistema de ferramentas. A [decisão por GitHub](./02-github-decision.md) justifica a plataforma pela colaboração via pull requests, code review, Actions para CI/CD e segurança com Dependabot e CodeQL.

O [Semantic Versioning](./03-semantic-versioning.md) define o formato MAJOR.MINOR.PATCH para comunicar claramente o significado das mudanças. Releases são coordenadas entre projetos com compatibility matrix especificando versões compatíveis.

O [workflow Git](./GIT/README.md) define branching strategy com trunk-based development, conventional commits para changelog automático, PR guidelines com code review obrigatório, e git hooks para linting e testes.

## Estrutura

- **[01-git-decision.md](./01-git-decision.md)** - Decisão por Git
- **[02-github-decision.md](./02-github-decision.md)** - Decisão por GitHub
- **[03-semantic-versioning.md](./03-semantic-versioning.md)** - Formato MAJOR.MINOR.PATCH
- **[GIT/](./GIT/README.md)** - Workflow Git do projeto

---

**Última atualização:** 2026-01-14
