---
type: leaf
status: approved
updated: 2026-01-22
---

# Clean Architecture

Padrao arquitetural adotado no backend GEOAPI que organiza o codigo em camadas concentricas com dependencias apontando para o centro. O nucleo contem regras de negocio puras sem dependencias externas, enquanto camadas externas implementam detalhes tecnicos como banco de dados e APIs.

A separacao em camadas facilita testabilidade ao permitir mocks de dependencias externas, e evolucao tecnologica ao isolar frameworks em camadas perifericas. Mudancas em banco de dados ou bibliotecas HTTP nao afetam regras de negocio.

## Camadas

A camada Domain contem entidades, value objects e interfaces de repositorio. Application implementa casos de uso orquestrando entidades. Infrastructure fornece implementacoes concretas de repositorios e servicos externos. Presentation expoe APIs REST e processa requisicoes HTTP.

## Regra de Dependencia

Dependencias sempre apontam para dentro. Domain nao conhece nenhuma outra camada. Application conhece apenas Domain. Infrastructure e Presentation conhecem Application e Domain. Inversao de dependencia via interfaces permite que camadas internas definam contratos implementados por externas.
