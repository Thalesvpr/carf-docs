# DOMAIN-MODEL

Modelo de domínio conceitual do sistema CARF, definindo entidades, value objects, agregados e relacionamentos de forma agnóstica a tecnologia, servindo como **fonte única de verdade** para implementações nos projetos.

As [entidades](./ENTITIES/README.md) representam os elementos centrais do domínio com identidade única e ciclo de vida rastreável, como Unit, Holder, Community e LegitimationRequest. Os [value objects](./VALUE-OBJECTS/README.md) são objetos imutáveis definidos por seus atributos, como CPF, GeoPolygon e Status, que encapsulam validações e regras de negócio.

Os [aggregates](./AGGREGATES/README.md) agrupam entidades em clusters coesos com fronteiras transacionais bem definidas, seguindo padrões DDD. Os [domain events](./EVENTS/README.md) representam fatos de negócio significativos que permitem comunicação desacoplada entre aggregates.

Os [relacionamentos](./RELATIONSHIPS/README.md) mapeiam como as entidades se associam, definindo cardinalidades e constraints. E os [diagramas](./DIAGRAMS/README.md) visualizam a estrutura através de UML, ERD e state machines.

## Estrutura

- **[ENTITIES/](./ENTITIES/README.md)** - Entidades do domínio
- **[VALUE-OBJECTS/](./VALUE-OBJECTS/README.md)** - Value objects imutáveis
- **[AGGREGATES/](./AGGREGATES/README.md)** - Aggregates e boundaries transacionais
- **[EVENTS/](./EVENTS/README.md)** - Domain events
- **[RELATIONSHIPS/](./RELATIONSHIPS/README.md)** - Relacionamentos entre entidades
- **[DIAGRAMS/](./DIAGRAMS/README.md)** - Diagramas UML e ERD

---

**Última atualização:** 2026-01-14
