---
type: leaf
status: approved
updated: 2026-01-22
---

# Clean Architecture

Padrao arquitetural adotado no backend GEOAPI que organiza o codigo em camadas concentricas com dependencias apontando para o centro. O nucleo contem regras de negocio puras sem dependencias externas, enquanto camadas externas implementam detalhes tecnicos como banco de dados e APIs.

A separacao em camadas facilita testabilidade ao permitir mocks de dependencias externas, e evolucao tecnologica ao isolar frameworks em camadas perifericas. Mudancas em banco de dados ou bibliotecas HTTP nao afetam regras de negocio.

## Estrutura

Domain contem entidades e value objects. Application implementa casos de uso. Infrastructure fornece repositorios concretos. Presentation expoe APIs REST. Dependencias sempre apontam para dentro, com inversao via interfaces.
