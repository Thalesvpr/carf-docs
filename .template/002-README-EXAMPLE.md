---
type: readme
status: approved
updated: 2026-01-22
---

# Domain Model

Modelo de dominio do sistema CARF definindo entidades, agregados, value objects e eventos seguindo Domain-Driven Design. Serve como fonte unica de verdade para a estrutura conceitual do sistema, independente de implementacao tecnica.

A pasta organiza-se em [entidades](./ENTITIES/README.md) que representam objetos com identidade propria como Unit, Holder e Community, [value objects](./VALUE-OBJECTS/README.md) que encapsulam conceitos imutaveis como CPF e GeoPolygon, [agregados](./AGGREGATES/README.md) que definem fronteiras de consistencia, e [eventos](./EVENTS/README.md) que capturam mudancas de estado relevantes para o negocio.

Os diagramas em [DIAGRAMS](./DIAGRAMS/README.md) visualizam relacionamentos entre entidades e fluxos de eventos. Toda implementacao nos projetos GEOAPI e REURBCAD deve seguir as definicoes aqui documentadas.
