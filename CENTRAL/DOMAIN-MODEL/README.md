# DOMAIN-MODEL

Modelo de domínio conceitual do sistema CARF definindo entidades value objects agregados e relacionamentos de forma agnóstica a tecnologia servindo como fonte da verdade para implementações em múltiplos projetos. Ver 00-INDEX.md para lista completa de 33 entities e 23 value objects.

## Estrutura

Documentação core do domínio organizada em [00-INDEX.md](./00-INDEX.md) indexando todas entities value objects aggregates workflows e business rules do sistema. Conceitos fundamentais incluem [ENTITIES/](./ENTITIES/README.md) definindo 33 entidades do domínio como Unit Holder Community LegitimationRequest, [VALUE-OBJECTS/](./VALUE-OBJECTS/README.md) contendo 25 value objects imutáveis CPF CNPJ Email GeoPolygon Status, e [AGGREGATES/](./AGGREGATES/README.md) agrupando três aggregates principais Unit Community LegitimationRequest seguindo padrões DDD tactical design.

Comunicação e relacionamentos documentados em [EVENTS/](./EVENTS/README.md) especificando 19 domain events para integração entre aggregates, [RELATIONSHIPS/](./RELATIONSHIPS/README.md) mapeando relacionamentos entre entidades um-para-muitos muitos-para-muitos e polimórficos, [DIAGRAMS/](./DIAGRAMS/README.md) visualizando estrutura através de diagramas de classe e relacionamentos, e [BUSINESS-RULES/](./BUSINESS-RULES/README.md) detalhando regras de negócio aplicadas ao domínio complementando [CENTRAL/BUSINESS-RULES](../BUSINESS-RULES/README.md) com validações específicas de entidades.

---

**Última atualização:** 2025-01-05
