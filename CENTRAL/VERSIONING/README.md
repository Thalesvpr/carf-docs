---
status: rejected
description: "Conteudo operacional. Git workflows pertencem a .github ou CONTRIBUTING."
updated: 2026-01-20
---

# VERSIONING

Estratégia de versionamento do CARF coordenando releases entre os repositórios independentes do ecossistema polyrepo.

A [decisão por Git](./01-git-decision.md) justifica a escolha como ferramenta de controle de versão pela performance, branching, workflows offline-first e ecossistema de ferramentas. A [decisão por GitHub](./02-github-decision.md) justifica a plataforma pela colaboração via pull requests, code review, Actions para CI/CD e segurança com Dependabot e CodeQL. O [Semantic Versioning](./03-semantic-versioning.md) define o formato MAJOR.MINOR.PATCH para comunicar claramente o significado das mudanças.

O [catálogo de repositórios](./04-repository-catalog.md) é a fonte única de verdade listando todos os repositórios do projeto com URLs, stacks e responsáveis. O [workflow Git](./GIT/README.md) define branching strategy com trunk-based development, conventional commits para changelog automático, PR guidelines com code review obrigatório e git hooks para automação local.

A documentação do [GitHub](./GITHUB/README.md) cobre configuração de organização, proteção de branches, Actions workflows e features de segurança. A seção de [releases](./RELEASES/README.md) documenta estratégia polyrepo, coordenação de releases e matriz de compatibilidade entre versões.

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/VERSIONING/GIT/README|GIT]]
- [[CENTRAL/VERSIONING/GITHUB/README|GITHUB]]
- [[CENTRAL/VERSIONING/RELEASES/README|RELEASES]]

## Documentos

### Em Revisão

- ○ [[CENTRAL/VERSIONING/01-git-decision.md|Decisão Git - Sistema Controle Versão]]
- ○ [[CENTRAL/VERSIONING/02-github-decision.md|Decisão GitHub - Plataforma Hospedagem Código]]
- ○ [[CENTRAL/VERSIONING/03-semantic-versioning.md|Versionamento Numérico - Semantic Versioning]]
- ○ [[CENTRAL/VERSIONING/04-repository-catalog.md|Catálogo de Repositórios]]

<!-- CARF-INDEX-END -->
