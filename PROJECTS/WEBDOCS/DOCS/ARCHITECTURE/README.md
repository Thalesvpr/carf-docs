# Arquitetura - WEBDOCS

## Documentos Disponíveis

- [01-overview.md](./01-overview.md) - Visão geral da arquitetura Astro/Starlight
- [02-layers.md](./02-layers.md) - Camadas (Content, Components, Layout)
- [03-data-flow.md](./03-data-flow.md) - Fluxo de dados (Markdown → HTML)
- [04-integration.md](./04-integration.md) - Integração com CENTRAL e search
- [05-deployment.md](./05-deployment.md) - Deploy para Vercel/GitHub Pages

## Conceitos Arquiteturais

WEBDOCS é site estático gerado com **Astro 4 + Starlight** consumindo documentação de `CENTRAL/` via sync automatizado, compilando Markdown em HTML com syntax highlighting, search via **Pagefind**, e deploy para **Vercel** com preview deployments em PRs.

## Stack

- Astro 4 - SSG framework
- Starlight - Documentation theme
- MDX - Markdown + JSX
- Shiki - Syntax highlighting
- Pagefind - Search indexing
- Vercel - Hosting + CI/CD

## Referências

- [Astro](https://astro.build/)
- [Starlight](https://starlight.astro.build/)
- [Pagefind](https://pagefind.app/)

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (5 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-overview](./01-overview.md) | Overview da Arquitetura - WEBDOCS |
| [02-layers](./02-layers.md) | Layers - WEBDOCS |
| [03-data-flow](./03-data-flow.md) | Data Flow - WEBDOCS |
| [04-integration](./04-integration.md) | Integration - WEBDOCS |
| [05-deployment](./05-deployment.md) | Deployment - WEBDOCS |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Muitas listas com bullets (14) antes do rodapé - considerar converter para parágrafo denso.
