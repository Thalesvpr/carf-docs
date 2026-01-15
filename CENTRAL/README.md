# CENTRAL

Documentação central do CARF servindo como **fonte única de verdade** para requisitos, decisões arquiteturais e modelo de domínio compartilhados por todos os projetos do sistema.

A base da especificação está nos [requisitos do projeto](./REQUIREMENTS/README.md), que contém os casos de uso, user stories, requisitos funcionais e não-funcionais, estabelecendo rastreabilidade entre o que foi especificado e o que está implementado. As decisões técnicas estão registradas como [ADRs](./ARCHITECTURE/README.md), documentando escolhas sobre autenticação, multi-tenancy e padrões de design.

O [modelo de domínio](./DOMAIN-MODEL/README.md) define as entidades, agregados e value objects seguindo DDD. As [regras de negócio](./BUSINESS-RULES/README.md) especificam validações e workflows de aprovação conforme a Lei 13.465/2017. Os [fluxos do sistema](./WORKFLOWS/README.md) descrevem processos completos como coleta em campo e validação por analistas.

As [integrações](./INTEGRATION/README.md) documentam conexões com Keycloak e PostgreSQL. Os [contratos da API](./API/README.md) definem endpoints e schemas. As [políticas de segurança](./SECURITY/README.md) cobrem conformidade LGPD. A [estratégia de testes](./TESTING/README.md) define a pirâmide de testes. O [monitoramento](./OPERATIONS/README.md) cobre logging e manutenção. O [versionamento](./VERSIONING/README.md) define o workflow Git. E as [bibliotecas compartilhadas](./LIBRARIES/README.md) documentam código reutilizado entre projetos.

## Estrutura

- **[REQUIREMENTS/](./REQUIREMENTS/README.md)** - Casos de uso, requisitos funcionais e user stories
- **[ARCHITECTURE/](./ARCHITECTURE/README.md)** - ADRs e padrões arquiteturais
- **[DOMAIN-MODEL/](./DOMAIN-MODEL/README.md)** - Entidades, agregados e value objects
- **[BUSINESS-RULES/](./BUSINESS-RULES/README.md)** - Regras de validação e workflows
- **[API/](./API/README.md)** - Contratos REST e schemas
- **[INTEGRATION/](./INTEGRATION/README.md)** - Integrações Keycloak e PostgreSQL
- **[SECURITY/](./SECURITY/README.md)** - Políticas de segurança e LGPD
- **[TESTING/](./TESTING/README.md)** - Estratégia de testes
- **[OPERATIONS/](./OPERATIONS/README.md)** - Monitoramento e manutenção
- **[VERSIONING/](./VERSIONING/README.md)** - Git workflow e versionamento
- **[WORKFLOWS/](./WORKFLOWS/README.md)** - Fluxos end-to-end do sistema
- **[LIBRARIES/](./LIBRARIES/README.md)** - Bibliotecas compartilhadas

---

**Última atualização:** 2026-01-14
