---
type: leaf
status: review
updated: 2026-02-08
---

# Design Principles

Principios de design aplicados na arquitetura e implementacao da GEOAPI.

## SOLID

Single Responsibility garante que Controllers recebem requests e retornam responses, Handlers processam logica de negocio e Repositories acessam dados, cada classe com uma unica razao para mudar. Open/Closed permite extensao via novos handlers e domain events sem modificar codigo existente. Liskov Substitution garante que interfaces IRepository sao substituiveis por qualquer implementacao (EF Core, Dapper, mock). Interface Segregation define interfaces pequenas e especificas como IUnitReader e IUnitWriter. Dependency Inversion faz Domain depender de abstracoes IRepository enquanto Infrastructure implementa concrecoes.

## DDD Tactical Patterns

Aggregates delimitam fronteiras de consistencia transacional com Unit, Community e LegitimationRequest como aggregate roots. Value Objects imutaveis (CPF, Email, Address, GeoPolygon) encapsulam validacao no construtor seguindo Fail Fast. Domain Events permitem comunicacao assincrona entre aggregates sem acoplamento direto. Factory methods em entidades encapsulam logica de criacao validando invariantes.

## Separacao de Concerns

Cada camada tem responsabilidade unica: Domain contem regras de negocio puras sem EF Core nem ASP.NET, Application orquestra use cases, Infrastructure implementa detalhes tecnicos, Presentation cuida de HTTP e serializacao. Essa separacao permite testar logica de negocio sem banco de dados, sem HTTP e sem servicos externos usando mocks.

## Performance e Pragmatismo

Queries de leitura usam AsNoTracking e projecoes Select direto para DTOs evitando materializacao de entidades completas. CQRS completo e aplicado apenas para use cases que justificam, queries simples podem ser feitas diretamente sem handler separado. Cache Redis com invalidacao seletiva via domain events otimiza leituras frequentes. Fail Fast valida dados no construtor de Value Objects e via FluentValidation em Commands antes de chegar ao Domain.
