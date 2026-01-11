# @carf/ui - Componentes React Compartilhados

@carf/ui é a biblioteca de componentes React compartilhados do ecossistema CARF, fornecendo componentes reutilizáveis baseados em shadcn/ui + Tailwind CSS para os frontends GEOWEB e ADMIN. A biblioteca implementa o design system CARF, garantindo consistência visual, acessibilidade WCAG 2.1 AA e responsividade em todas as aplicações. Inclui componentes shadcn/ui customizados (Button, Input, Dialog, Table) e componentes específicos do domínio CARF (UnitCard, HolderCard, MapView, CommunityList) que encapsulam lógica de apresentação de entidades do sistema. Documentação completa em Storybook, testes com Testing Library, e publicação como NPM package via GitHub Packages.

## Estrutura da Documentação

### [ARCHITECTURE/README.md](./ARCHITECTURE/README.md)
- [01-overview.md](./ARCHITECTURE/01-overview.md) - Arquitetura de componentes React
- [03-data-flow.md](./ARCHITECTURE/03-data-flow.md) - Fluxo de props e state
- [04-integration.md](./ARCHITECTURE/04-integration.md) - Integração com GEOWEB/ADMIN
- [05-deployment.md](./ARCHITECTURE/05-deployment.md) - Publicação NPM

### [CONCEPTS/README.md](./CONCEPTS/README.md)
- [01-key-concepts.md](./CONCEPTS/01-key-concepts.md) - Design tokens, composição
- [02-accessibility.md](./CONCEPTS/02-accessibility.md) - Padrões de acessibilidade
- [02-terminology.md](./CONCEPTS/02-terminology.md) - Glossário de componentes
- [03-design-principles.md](./CONCEPTS/03-design-principles.md) - Princípios de design

### [HOW-TO/README.md](./HOW-TO/README.md)
- [01-setup-dev-environment.md](./HOW-TO/01-setup-dev-environment.md) - Setup Storybook
- [02-build-and-run.md](./HOW-TO/02-build-and-run.md) - Build da biblioteca
- [02-customization.md](./HOW-TO/02-customization.md) - Customizar tema
- [03-testing.md](./HOW-TO/03-testing.md) - Testes de componentes
- [04-troubleshooting.md](./HOW-TO/04-troubleshooting.md) - Problemas comuns

## Relação com CENTRAL/

- **Design System:** (não existe em CENTRAL - específico da lib)
- **Component Patterns:** Segue [CENTRAL/ARCHITECTURE/PATTERNS/05-frontend-patterns.md](../../../../../CENTRAL/ARCHITECTURE/PATTERNS/05-frontend-patterns.md)

## Relação com outros projetos

### Dependências
- [@carf/tscore](../../TSCORE/DOCS/README.md) - Types, validações

### Consumidores
- **GEOWEB** - Frontend web principal
- **ADMIN** - Console administrativo

## Tecnologias

- React 18
- TypeScript 5.3
- Tailwind CSS 3.4
- shadcn/ui
- Radix UI (primitives)
- Storybook 8.0
- Testing Library
- Vite 5

## Quick Start

```bash
cd PROJECTS/LIB/TS/UI-COMPONENTS/SRC-CODE
bun install
bun run storybook  # Abre Storybook em http://localhost:6006
```

## Links Úteis

- [Source Code README](../SRC-CODE/carf-ui/README.md) - Repositório e setup local
- [CENTRAL/LIBRARIES/](../../../../../CENTRAL/LIBRARIES/README.md) - Índice de bibliotecas
- [Storybook Oficial](https://storybook.js.org/)
- [shadcn/ui](https://ui.shadcn.com/)
