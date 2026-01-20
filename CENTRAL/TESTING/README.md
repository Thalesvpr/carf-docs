---
status: review
updated: 2026-01-15
---

# TESTING

Estratégia de testes do CARF garantindo qualidade e confiabilidade do código.

A [estratégia](./TEST-STRATEGY/README.md) segue a pirâmide de testes com proporção de 70% unitários, 20% integração e 10% E2E, priorizando feedback rápido. As metas de coverage são 80% para domain layer, 60% para application e 40% para infrastructure. O pipeline CI falha se o coverage ficar abaixo dos targets.

Os [casos de teste](./TEST-CASES/README.md) estão organizados por tipo: testes de API para endpoints REST, testes E2E para jornadas completas do usuário, e testes unitários para domain e application layers.

Inclui fixtures, factories e test data builders para setup rápido, evitando código duplicado nos testes.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (7 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Test Cases](./TEST-CASES/README.md) | 5 |
|  | [Test Strategy](./TEST-STRATEGY/README.md) | 2 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Subpastas

- [[CENTRAL/TESTING/TEST-CASES/README|TEST-CASES]]
- [[CENTRAL/TESTING/TEST-STRATEGY/README|TEST-STRATEGY]]

<!-- CARF-INDEX-END -->
