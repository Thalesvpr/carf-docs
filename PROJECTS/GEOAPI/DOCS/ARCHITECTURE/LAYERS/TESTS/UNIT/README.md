# UNIT

Testes unitários do GEOAPI verificando comportamento isolado de componentes individuais sem dependências externas usando mocks e stubs para simular colaboradores. Domain entities testadas verificam invariants aplicados no constructor e métodos behavior (Unit.ChangeStatus deve validar transições permitidas, Holder.AddContact deve rejeitar duplicates), value objects testam validações e equality semantics (CPF rejeita formato inválido, Address.Equals compara por valor não referência) e domain services verificam business rules complexas sem side effects em database. Application layer validators usando FluentValidation testam todas rules declaradas (CreateUnitCommandValidator verifica required fields, format constraints, business rules) com test cases cobrindo valid inputs e cada validation rule isoladamente retornando error messages esperados. Mappers AutoMapper testam conversões bidirecionais Entity ↔ DTO preservando todos campos relevantes e aplicando transformações corretas (geometry WKB para GeoJSON, DateTimeOffset para ISO8601 string) verificados via assertions profundas comparando cada property.

## Arquivos Principais (a criar)

**Domain - Entities:**
- 01-unit-tests.md - Unit entity invariants e behavior methods
- 02-holder-tests.md - Holder entity vinculos e validações
- 03-community-tests.md - Community entity aggregates
- 04-team-tests.md - Team entity members e status

**Domain - Value Objects:**
- 05-cpf-tests.md - CPF validation rules e formatting
- 06-email-tests.md - Email format validation
- 07-geometry-tests.md - Geometry creation e spatial operations
- 08-address-tests.md - Address value object equality

**Domain - Services:**
- 09-legitimation-eligibility-service-tests.md - Regras REURB-S/E eligibility
- 10-unit-area-calculator-tests.md - Cálculo área via PostGIS

**Application - Validators:**
- 11-create-unit-validator-tests.md - CreateUnitCommand validation rules
- 12-update-holder-validator-tests.md - UpdateHolderCommand validations
- 13-assign-team-validator-tests.md - AssignTeamCommand business rules

**Application - Mappers:**
- 14-unit-mapper-tests.md - Unit ↔ UnitDto conversões
- 15-holder-mapper-tests.md - Holder ↔ HolderDto mapping

**Application - Handlers:**
- 16-create-unit-handler-tests.md - CreateUnitCommandHandler lógica orquestração
- 17-get-units-handler-tests.md - GetUnitsQueryHandler filtering

## Convenções

Testes unitários devem executar rapidamente (< 100ms cada) sem IO operations como database access ou HTTP calls usando mocks via Moq para substituir repositories e external services. Arrange-Act-Assert pattern estrutura cada test method claramente separando setup (criar entity, configurar mocks), execution (chamar method under test) e verification (assertions sobre resultado e interactions). Test data factories criam entities válidas com valores default realistas via Bogus permitindo testes focar apenas nos campos relevantes para cenário específico sem boilerplate repetitivo construindo objetos complexos manualmente. Cada test class herda de base class fornecendo utilities comuns como mock creation helpers e assertion extensions reduzindo duplicação cross tests mantendo consistency. Theory tests usando InlineData ou MemberData exercitam múltiplos inputs com mesmo assertion logic ideal para boundary testing de validations (CPF com 10 digits, 11 digits, 12 digits, formato inválido) cobrindo edge cases sistematicamente.

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático; Muitas listas com bullets (17) antes do rodapé - considerar converter para parágrafo denso.
