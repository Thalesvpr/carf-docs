# Arquitetura - @carf/ui

## Documentos Disponíveis

- [01-overview.md](./01-overview.md) - Visão geral da arquitetura de componentes React
- [03-data-flow.md](./03-data-flow.md) - Fluxo de dados (props, state, context)
- [04-integration.md](./04-integration.md) - Integração com GEOWEB e ADMIN
- [05-deployment.md](./05-deployment.md) - Build, publicação NPM, versionamento

## Conceitos Arquiteturais

A biblioteca segue arquitetura de **Atomic Design** (atoms → molecules → organisms) e padrões de composição React via compound components, render props e custom hooks. Todos os componentes são **server-side compatible** (RSC-ready) e seguem princípios de **acessibilidade** via Radix UI primitives.

## Referências

- [CENTRAL/ARCHITECTURE/PATTERNS/05-frontend-patterns.md](../../../../../../CENTRAL/ARCHITECTURE/PATTERNS/05-frontend-patterns.md)
- [React Server Components](https://react.dev/blog/2023/03/22/react-labs-what-we-have-been-working-on-march-2023#react-server-components)
- [Atomic Design](https://bradfrost.com/blog/post/atomic-web-design/)
