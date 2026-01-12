# Design Principles

Princípios SOLID aplicados no GEOAPI incluem Single Responsibility Principle (SRP) onde cada classe tem uma única razão para mudar com Controllers recebendo requests e retornando responses, Handlers processando lógica de negócio e Repositories acessando dados. Open/Closed Principle (OCP) permite extensão via novos handlers e events sem modificar código existente. Liskov Substitution Principle (LSP) garante que interfaces IRepository são substituíveis por qualquer implementação seja EF Core, Dapper ou mock. Interface Segregation Principle (ISP) define interfaces pequenas e específicas como IUnitReader e IUnitWriter ao invés de uma grande interface genérica. Dependency Inversion Principle (DIP) faz Domain depender de abstrações IRepository enquanto Infrastructure implementa concreções UnitRepository.

DRY (Don't Repeat Yourself) evita duplicação via base classes Entity<TId> com propriedades Id CreatedAt UpdatedAt compartilhadas entre todas entities, métodos compartilhados via extensions methods e helpers. KISS (Keep It Simple) aplica CQRS completo apenas para use cases complexos enquanto queries simples podem ser feitas diretamente no controller sem handler separado evitando over-engineering. YAGNI (You Aren't Gonna Need It) implementa features quando necessário evitando abstrações prematuras como factories e validators quando só há uma implementação.

Separation of Concerns isola cada layer com responsabilidade única onde Domain contém regras de negócio puras sem EF Core nem ASP.NET, Application orquestra use cases, Infrastructure implementa detalhes técnicos, e Gateway cuida de HTTP serialização e autenticação. Fail Fast valida no construtor de Value Objects lançando exception imediata para dados inválidos e FluentValidation valida Commands/DTOs antes de chegar Domain. Explicit Over Implicit prefere mapeamento explícito de DTOs via extension methods ToDto() ao invés de AutoMapper mágico facilitando debug e performance. Database-Agnostic Domain não conhece database dependendo apenas de interfaces sem referências a EF Core. Test-Driven Design injeta dependências via construtor tornando código testável com mocks. Performance Awareness usa AsNoTracking() em queries read-only e projeções Select() ao invés de carregar entidades completas com Includes.

---

**Última atualização:** 2026-01-12

