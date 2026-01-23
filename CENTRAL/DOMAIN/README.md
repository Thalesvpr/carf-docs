---
type: readme
status: review
updated: 2026-01-22
---

# DOMAIN

Linguagem ubiqua e conceitos de negocio do dominio REURB. Define O QUE sao as coisas, nao como sao implementadas.

## Estrutura

| Pasta | Conteudo |
|-------|----------|
| [CONCEPTS](./CONCEPTS/README.md) | Entidades conceituais (unit, holder, community...) |
| [AGGREGATES](./AGGREGATES/README.md) | Boundaries de consistencia transacional |
| [VALUE-OBJECTS](./VALUE-OBJECTS/README.md) | Tipos de valor imutaveis (CPF, Status, Polygon...) |
| [RELATIONSHIPS](./RELATIONSHIPS/README.md) | Como entidades se relacionam |
| [DIAGRAMS](./DIAGRAMS/README.md) | Visualizacoes ER, state machines |

## O que NAO pertence aqui

- Classes base tecnicas (BaseEntity, AggregateRoot) → ficam em codigo
- Eventos de dominio → ficam em GEOAPI/DOMAIN/EVENTS
- Regras de negocio → ficam em DOMAIN-RULES

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (5)

| Pasta | Descrição |
|-------|-----------|
| [AGGREGATES](./AGGREGATES/README.md) | ... |
| [CONCEPTS](./CONCEPTS/README.md) | ... |
| [DIAGRAMS](./DIAGRAMS/README.md) | ... |
| [RELATIONSHIPS](./RELATIONSHIPS/README.md) | ... |
| [VALUE-OBJECTS](./VALUE-OBJECTS/README.md) | ... |

<!-- CARF-INDEX-END -->
