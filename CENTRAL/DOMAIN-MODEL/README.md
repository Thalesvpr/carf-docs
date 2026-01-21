---
status: rejected
description: "Estrutura caotica. Numeracao nao agrupa por categoria. Precisa reorganizar por agregado/contexto."
updated: 2026-01-15
---

# DOMAIN-MODEL

Modelo de domínio conceitual do sistema CARF, definindo entidades, value objects, agregados e relacionamentos de forma agnóstica a tecnologia, servindo como **fonte única de verdade** para implementações nos projetos.

As [entidades](./ENTITIES/README.md) representam os elementos centrais do domínio com identidade única e ciclo de vida rastreável, como Unit, Holder, Community e LegitimationRequest. Os [value objects](./VALUE-OBJECTS/README.md) são objetos imutáveis definidos por seus atributos, como CPF, GeoPolygon e Status, que encapsulam validações e regras de negócio.

Os [aggregates](./AGGREGATES/README.md) agrupam entidades em clusters coesos com fronteiras transacionais bem definidas, seguindo padrões DDD. Os [domain events](./EVENTS/README.md) representam fatos de negócio significativos que permitem comunicação desacoplada entre aggregates.

Os [relacionamentos](./RELATIONSHIPS/README.md) mapeiam como as entidades se associam, definindo cardinalidades e constraints. E os [diagramas](./DIAGRAMS/README.md) visualizam a estrutura através de UML, ERD e state machines.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (87 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Aggregates](./AGGREGATES/README.md) | 3 |
|  | [Diagrams](./DIAGRAMS/README.md) | 2 |
|  | [Entities](./ENTITIES/README.md) | 35 |
|  | [Events](./EVENTS/README.md) | 20 |
|  | [Relationships](./RELATIONSHIPS/README.md) | 1 |
|  | [Value Objects](./VALUE-OBJECTS/README.md) | 26 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/DOMAIN-MODEL/AGGREGATES/README|AGGREGATES]]
- [[CENTRAL/DOMAIN-MODEL/DIAGRAMS/README|DIAGRAMS]]
- [[CENTRAL/DOMAIN-MODEL/ENTITIES/README|ENTITIES]]
- [[CENTRAL/DOMAIN-MODEL/EVENTS/README|EVENTS]]
- [[CENTRAL/DOMAIN-MODEL/RELATIONSHIPS/README|RELATIONSHIPS]]
- [[CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/README|VALUE-OBJECTS]]

<!-- CARF-INDEX-END -->
