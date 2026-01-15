# REQUIREMENTS

Especificação completa de requisitos do sistema CARF organizada em hierarquia que estabelece rastreabilidade entre o que foi especificado e o que está implementado em cada projeto.

Os [casos de uso](./USE-CASES/README.md) documentam fluxos completos de interação entre usuário e sistema, incluindo caminhos alternativos e tratamento de exceções. Os [requisitos funcionais](./FUNCTIONAL-REQUIREMENTS/README.md) definem capacidades específicas que o sistema deve ter, mantendo independência tecnológica. As [user stories](./USER-STORIES/README.md) estabelecem a perspectiva do usuário e o valor de negócio de cada funcionalidade. E os [requisitos não-funcionais](./NON-FUNCTIONAL-REQUIREMENTS/README.md) definem critérios de qualidade como performance, segurança e usabilidade.

A hierarquia funciona assim: requisitos funcionais definem O QUE fazer, user stories especificam QUEM usa e POR QUE, e casos de uso documentam COMO fazer o fluxo completo. Cada caso de uso identifica os módulos implementadores via frontmatter, permitindo rastrear a implementação correspondente em cada projeto.

Os requisitos são organizados por épicas temáticas como Security, Performance e Usability, cruzando com os módulos implementadores para mostrar cobertura e identificar gaps no backlog.

## Estrutura

- **[USE-CASES/](./USE-CASES/README.md)** - Casos de uso e fluxos completos
- **[FUNCTIONAL-REQUIREMENTS/](./FUNCTIONAL-REQUIREMENTS/README.md)** - Requisitos funcionais atômicos
- **[USER-STORIES/](./USER-STORIES/README.md)** - User stories formato BDD
- **[NON-FUNCTIONAL-REQUIREMENTS/](./NON-FUNCTIONAL-REQUIREMENTS/README.md)** - Requisitos não-funcionais e qualidade

---

**Última atualização:** 2026-01-14
