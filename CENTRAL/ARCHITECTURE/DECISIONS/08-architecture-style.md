---
type: adr
status: current
updated: 2026-01-22
---

# ADR-008: Clean Architecture com CQRS

## Contexto

Backend implementa regras de negocio complexas do dominio REURB que evoluem conforme legislacao. Testabilidade e essencial para garantir corretude. Separacao de leitura e escrita pode otimizar performance. Decisao impacta estrutura de codigo e facilidade de evolucao.

## Decisao

Adotamos Clean Architecture com CQRS no backend GEOAPI. Camadas Domain, Application, Infrastructure e Presentation com dependencias apontando para o centro. MediatR implementa commands e queries separados. Domain Events disparam side effects de forma desacoplada.

## Consequencias

Regras de negocio isoladas em Domain facilitam testes unitarios sem mocks de infraestrutura. CQRS permite otimizar queries de leitura independente de comandos. Codigo mais verboso com mais arquivos e indirections. Curva de aprendizado para desenvolvedores novos no padrao.

## Alternativas Rejeitadas

Arquitetura em camadas tradicional foi descartada por acoplar regras de negocio a infraestrutura. Microservices foi rejeitado por complexidade operacional desproporcional ao tamanho da equipe. Event sourcing foi descartado por overhead de implementacao sem beneficio claro para o dominio.
