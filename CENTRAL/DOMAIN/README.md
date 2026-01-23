---
type: readme
status: current
updated: 2026-01-22
---

# DOMAIN

Linguagem ubiqua e conceitos de negocio do dominio REURB. Define O QUE sao as coisas, nao como sao implementadas ou quais regras governam seu comportamento.

A documentacao de dominio organiza-se em cinco areas complementares. Os [conceitos](./CONCEPTS/README.md) definem as entidades fundamentais do dominio como unidade habitacional, titular, comunidade e nucleo, estabelecendo vocabulario comum entre equipe tecnica e especialistas de dominio. Os [agregados](./AGGREGATES/README.md) delimitam fronteiras de consistencia transacional, identificando quais entidades devem ser persistidas juntas para manter invariantes de negocio. Os [objetos de valor](./VALUE-OBJECTS/README.md) documentam tipos imutaveis como CPF, Status, Polygon e Coordinate que encapsulam validacao e comportamento sem identidade propria.

Os [relacionamentos](./RELATIONSHIPS/README.md) mapeiam como entidades se conectam, incluindo cardinalidades, direcionalidade e restricoes de navegacao entre agregados. Os [diagramas](./DIAGRAMS/README.md) fornecem visualizacoes complementares como diagramas ER, maquinas de estado e fluxos de transicao que facilitam compreensao rapida do modelo.

Esta pasta foca exclusivamente em modelagem conceitual. Classes base tecnicas como BaseEntity e AggregateRoot pertencem ao codigo-fonte em PROJECTS/GEOAPI/. Eventos de dominio que disparam comportamentos reativos ficam em PROJECTS/GEOAPI/DOMAIN/EVENTS/. Regras de negocio que governam validacoes, transicoes de estado e restricoes legais sao documentadas separadamente em [DOMAIN-RULES](../DOMAIN-RULES/README.md).

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
