# DOMAIN-MODEL

Modelo de domínio conceitual do sistema CARF, definindo entidades, value objects, agregados e relacionamentos de forma agnóstica a tecnologia, servindo como **fonte única de verdade** para implementações nos projetos.

As [entidades](./ENTITIES/README.md) representam os elementos centrais do domínio com identidade única e ciclo de vida rastreável, como Unit, Holder, Community e LegitimationRequest. Os [value objects](./VALUE-OBJECTS/README.md) são objetos imutáveis definidos por seus atributos, como CPF, GeoPolygon e Status, que encapsulam validações e regras de negócio.

Os [aggregates](./AGGREGATES/README.md) agrupam entidades em clusters coesos com fronteiras transacionais bem definidas, seguindo padrões DDD. Os [domain events](./EVENTS/README.md) representam fatos de negócio significativos que permitem comunicação desacoplada entre aggregates.

Os [relacionamentos](./RELATIONSHIPS/README.md) mapeiam como as entidades se associam, definindo cardinalidades e constraints. E os [diagramas](./DIAGRAMS/README.md) visualizam a estrutura através de UML, ERD e state machines.

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Incompleto
Descrição: Aguardando index gerado por script.

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (85 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Aggregates](./AGGREGATES/README.md) | 3 |
|  | [Diagrams](./DIAGRAMS/README.md) | 0 |
|  | [Entities](./ENTITIES/README.md) | 35 |
|  | [Events](./EVENTS/README.md) | 20 |
|  | [Relationships](./RELATIONSHIPS/README.md) | 1 |
|  | [Value Objects](./VALUE-OBJECTS/README.md) | 26 |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
