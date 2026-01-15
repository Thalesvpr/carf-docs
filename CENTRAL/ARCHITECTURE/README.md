# ARCHITECTURE

Documentação da arquitetura sistêmica do CARF definindo princípios, padrões e estratégias de deployment aplicados nos projetos.

Os [ADRs](./ADRs/README.md) documentam decisões arquiteturais críticas como escolha de tecnologias, padrões de autenticação e estratégias de multi-tenancy, registrando contexto, alternativas avaliadas e consequências de cada decisão.

Os [padrões arquiteturais](./PATTERNS/README.md) definem como aplicar Clean Architecture, CQRS, Repository, Domain Events e padrões específicos para frontend React e aplicações offline-first mobile.

As [estratégias de deployment](./DEPLOYMENT/README.md) cobrem containerização Docker, orquestração Kubernetes, pipelines CI/CD com GitHub Actions, deployment mobile para App Store e Google Play, e sites estáticos.

Para implementação técnica específica de cada projeto, consulte a documentação em **PROJECTS/\*/DOCS/**.

## Estrutura

- **[ADRs/](./ADRs/README.md)** - Architecture Decision Records
- **[DEPLOYMENT/](./DEPLOYMENT/README.md)** - Estratégias de deployment e infraestrutura
- **[PATTERNS/](./PATTERNS/README.md)** - Padrões arquiteturais aplicados

---

**Última atualização:** 2026-01-14
