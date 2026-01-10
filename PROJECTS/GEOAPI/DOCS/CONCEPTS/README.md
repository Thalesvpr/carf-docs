# Conceitos Fundamentais - GEOAPI

Documentação conceitual do backend REST API do projeto CARF. Esta seção explica os conceitos-chave, terminologia e princípios de design que fundamentam a arquitetura do GEOAPI.

## 📚 Documentos Disponíveis

| Documento | Descrição |
|-----------|-----------|
| [01-authentication.md](./01-authentication.md) | Conceitos de autenticação OAuth2/OIDC com Keycloak |
| [02-authorization.md](./02-authorization.md) | Conceitos de autorização RBAC e multi-tenancy |
| [01-key-concepts.md](./01-key-concepts.md) | Conceitos-chave (Domain Model, Aggregates, Value Objects, CQRS) |
| [02-terminology.md](./02-terminology.md) | Glossário completo de termos técnicos e de negócio |
| [03-design-principles.md](./03-design-principles.md) | Princípios de design (SOLID, DDD, Clean Architecture) |

## 🎯 Conceitos Principais

### Clean Architecture

Arquitetura em camadas com dependências apontando sempre para o núcleo (Domain):

```
┌─────────────────────────────────────────┐
│       Gateway (Controllers, DTOs)       │  ← External Interface
├─────────────────────────────────────────┤
│   Application (Use Cases, Handlers)     │  ← Business Logic
├─────────────────────────────────────────┤
│      Domain (Entities, Rules)           │  ← Core Business
├─────────────────────────────────────────┤
│  Infrastructure (DB, APIs, Services)    │  ← External Services
└─────────────────────────────────────────┘
```

**Benefícios:**
- Independência de frameworks
- Testabilidade
- Independência de UI
- Independência de banco de dados
- Manutenibilidade

### Domain-Driven Design (DDD)

Foco no modelo de domínio como centro da aplicação:

**Aggregates:**
- `Unit` - Unidade imobiliária (raiz do aggregate)
- `Community` - Comunidade/assentamento
- `LegitimationRequest` - Pedido de legitimação

**Value Objects:**
- `CPF`, `CNPJ` - Documentos
- `Address` - Endereço completo
- `Coordinates` - Coordenadas geográficas (lat/lng)
- `Area` - Área do imóvel

**Domain Events:**
- `UnitCreatedEvent`
- `HolderRegisteredEvent`
- `LegitimationApprovedEvent`

### CQRS (Command Query Responsibility Segregation)

Separação entre operações de escrita (Commands) e leitura (Queries):

**Commands (Modificam estado):**
- `CreateUnitCommand`
- `UpdateHolderCommand`
- `ApproveLegitimationCommand`

**Queries (Apenas leitura):**
- `GetUnitByIdQuery`
- `ListUnitsQuery`
- `SearchCommunitiesQuery`

**Benefícios:**
- Separação de responsabilidades
- Otimização independente
- Escalabilidade
- Modelos específicos para leitura e escrita

### Multi-Tenancy via Row-Level Security (RLS)

Isolamento de dados por município através de políticas RLS no PostgreSQL:

```sql
CREATE POLICY units_tenant_isolation ON units
FOR ALL
USING (municipality_id = current_setting('app.current_municipality_id')::uuid);
```

**Fluxo:**
1. JWT contém `municipality_id` claim
2. Middleware extrai claim e configura `SET LOCAL app.current_municipality_id`
3. RLS policies filtram automaticamente todos os queries

### Repository Pattern

Abstração de acesso a dados, isolando a lógica de persistência:

```csharp
public interface IUnitRepository
{
    Task<Unit?> GetByIdAsync(UnitId id);
    Task<PagedResult<Unit>> ListAsync(int page, int pageSize);
    Task AddAsync(Unit unit);
    Task UpdateAsync(Unit unit);
    Task DeleteAsync(UnitId id);
}
```

**Benefícios:**
- Separação de concerns
- Testabilidade (fácil de mockar)
- Flexibilidade (trocar ORM sem afetar domain)

## 🏛️ Princípios SOLID

### Single Responsibility Principle (SRP)
Cada classe tem uma única responsabilidade:
- `UnitRepository` - apenas persistência de Units
- `CreateUnitCommandHandler` - apenas lógica de criação

### Open/Closed Principle (OCP)
Aberto para extensão, fechado para modificação:
- Novos validators podem ser adicionados sem modificar `FluentValidation` pipeline
- Novos domain events podem ser criados sem modificar aggregate roots

### Liskov Substitution Principle (LSP)
Subclasses devem ser substituíveis por suas bases:
- Todas as implementações de `IRepository<T>` são intercambiáveis

### Interface Segregation Principle (ISP)
Interfaces específicas em vez de genéricas:
- `IUnitRepository` em vez de `IRepository<Unit>` genérico
- Métodos específicos de domain (ex: `FindUnitsWithinRadiusAsync`)

### Dependency Inversion Principle (DIP)
Depender de abstrações, não de implementações:
- Domain depende de `IUnitRepository` (interface)
- Infrastructure implementa `UnitRepository` (concreta)
- Injeção de dependência resolve em runtime

## 🌐 Conceitos de Negócio

### Regularização Fundiária

Processo de legalização de áreas urbanas ocupadas irregularmente:

**Etapas:**
1. Cadastro de unidades e possuidores
2. Levantamento topográfico
3. Análise jurídica
4. Emissão de título de propriedade

### Unidade Imobiliária (Unit)

Imóvel individual dentro de uma comunidade, com:
- Endereço
- Coordenadas GPS
- Área (m²)
- Possuidores (pessoas que ocupam)
- Status de legitimação

### Comunidade (Community)

Agrupamento de unidades imobiliárias (assentamento informal):
- Nome da comunidade
- Polígono delimitador
- Município
- População estimada

### Legitimação (Legitimation)

Processo de concessão de título de propriedade:
- Pedido de legitimação
- Documentação comprobatória
- Análise técnica
- Aprovação/rejeição

## 🔗 Referências

- [ARCHITECTURE/](../ARCHITECTURE/README.md) - Arquitetura técnica detalhada
- [HOW-TO/](../HOW-TO/README.md) - Guias práticos de desenvolvimento
- [CENTRAL/DOMAIN-MODEL/](../../../../CENTRAL/DOMAIN-MODEL/README.md) - Modelo de domínio completo
- [CENTRAL/BUSINESS-RULES/](../../../../CENTRAL/BUSINESS-RULES/README.md) - Regras de negócio
- [Clean Architecture (Robert C. Martin)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Domain-Driven Design (Eric Evans)](https://domainlanguage.com/ddd/)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
