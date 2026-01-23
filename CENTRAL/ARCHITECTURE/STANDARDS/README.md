---
type: readme
status: current
updated: 2026-01-22
---

# STANDARDS

Padroes e convencoes obrigatorios para todos os projetos do ecossistema CARF garantindo consistencia, interoperabilidade e facilidade de manutencao entre equipes.

Os padroes definem regras prescritivas de como fazer as coisas. Diferem de decisoes arquiteturais (ADRs) que explicam por que uma escolha foi feita, e de documentacao de integracao que explica como sistemas se comunicam. Standards sao imperativos e devem ser seguidos por todos os projetos.

O padrao de [documentacao](./01-documentation.md) define estrutura de arquivos markdown, templates obrigatorios e formato de frontmatter. O padrao de [codigo](./02-code-style.md) estabelece convencoes de nomenclatura, organizacao de arquivos e formatacao. O padrao de [commits](./03-commits.md) define formato de mensagens e processo de revisao. O padrao de [api](./04-api-design.md) especifica convencoes REST, versionamento e tratamento de erros. O padrao de [versionamento](./05-versioning.md) define semantic versioning e politicas de releases.

A subpasta [GIT](./GIT/README.md) documenta workflows de branching, commit conventions, PR guidelines e git hooks. A subpasta [RELEASES](./RELEASES/README.md) cobre estrategia polyrepo, coordenacao de releases e matriz de compatibilidade entre projetos. Templates de cada tipo de documento estao disponiveis em .template/ na raiz do repositorio.

<!-- CARF-INDEX-START -->

<!-- CARF-INDEX-END -->
