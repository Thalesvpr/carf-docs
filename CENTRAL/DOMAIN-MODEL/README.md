# DOMAIN-MODEL

Modelo de domínio conceitual do sistema CARF definindo entidades value objects agregados e relacionamentos de forma agnóstica a tecnologia servindo como fonte da verdade para implementações em múltiplos projetos. Ver 00-INDEX.md para lista completa de 33 entities e 23 value objects.

## Estrutura

- **[00-INDEX.md](./00-INDEX.md)** - Índice completo de todas entities, value objects, aggregates, workflows e business rules
- **[ENTITIES/](./ENTITIES/README.md)** - 33 entidades do domínio (Unit, Holder, Community, LegitimationRequest, etc.)
- **[VALUE-OBJECTS/](./VALUE-OBJECTS/README.md)** - 25 value objects imutáveis (CPF, CNPJ, Email, GeoPolygon, Status, etc.)
- **[AGGREGATES/](./AGGREGATES/README.md)** - 3 aggregates principais (Unit, Community, LegitimationRequest)
- **[EVENTS/](./EVENTS/README.md)** - 19 domain events para comunicação entre aggregates
- **[RELATIONSHIPS/](./RELATIONSHIPS/README.md)** - Relacionamentos entre entidades (1:N, N:N, polimórficos)
- **[DIAGRAMS/](./DIAGRAMS/README.md)** - Diagramas de classe e relacionamentos
- **[BUSINESS-RULES/](./BUSINESS-RULES/README.md)** - Business rules aplicadas ao domínio (ver também [CENTRAL/BUSINESS-RULES](../BUSINESS-RULES/README.md))

---

**Última atualização:** 2025-01-05
