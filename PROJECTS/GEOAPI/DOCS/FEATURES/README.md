# FEATURES - Funcionalidades GEOAPI

Backend GEOAPI implementa funcionalidades via Clean Architecture organizada em camadas Domain Application Infrastructure Presentation documentadas em LAYERS ao invés de FEATURES tradicional frontend separando concerns responsabilidades boundaries conforme DDD Domain-Driven Design patterns aggregates repositories use cases commands queries CQRS handlers MediatR pipelines garantindo separação lógica negócio da infraestrutura persistence comunicação externa facilitando manutenibilidade testabilidade evolução independente cada camada sem acoplamento tight coupling entre componentes arquiteturais permitindo substituição implementações concretas interfaces abstrações dependency injection container ASP.NET Core.

Consulte LAYERS para documentação técnica detalhada de cada funcionalidade implementada mapeando requirements CENTRAL para implementation .NET específica camadas arquiteturais facilitando navegação descoberta features backend REST API endpoints controllers services domain logic business rules validações persistence PostgreSQL Entity Framework Core migrations contextos bounded contexts agregados value objects specifications patterns repository unit of work garantindo integridade transacional consistência dados domínio através de abstrações bem definidas separando infraestrutura de lógica negócio core aplicação mantendo testabilidade via mocks stubs in-memory repositories testes unitários integração end-to-end CI/CD pipelines automatizados.

---

**Última atualização:** 2026-01-11
