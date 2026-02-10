---
type: leaf
status: review
updated: 2026-02-08
---

# Estrategia de Testes - GEOAPI

Este documento define a estrategia de testes do projeto Carf.GeoApi, incluindo a piramide de testes, ferramentas utilizadas, convencoes de nomenclatura, organizacao dos projetos e integracao com CI/CD.

## Piramide de Testes

A distribuicao dos testes segue a piramide classica, priorizando testes unitarios por velocidade e custo de manutencao.

| Nivel | Proporcao | Foco | Tempo Medio por Teste |
|-------|-----------|------|-----------------------|
| Unitarios | 70% | Regras de dominio, value objects, handlers CQRS, validators | < 10ms |
| Integracao | 20% | Repositorios, DbContext, queries PostGIS, RLS, migrations | 100-500ms |
| E2E | 10% | Fluxo HTTP completo, autenticacao JWT, workflows multi-etapa | 500ms-2s |

## Ferramentas

| Ferramenta | Versao | Funcao | Camada de Uso |
|------------|--------|--------|---------------|
| xUnit | 2.x | Framework de testes (test runner, fixtures, theories) | Todas |
| Moq | 4.x | Mocking de interfaces (repositorios, services, providers) | Unit |
| Bogus | 35.x | Geracao de dados de teste (fakers, builders) | Todas |
| FluentAssertions | 6.x | Assertions expressivas e mensagens de erro claras | Todas |
| Testcontainers | 3.x | Containers Docker efemeros para PostgreSQL+PostGIS e Redis | Integration, E2E |
| WebApplicationFactory | .NET 9 | Host de teste in-process para a API ASP.NET Core | E2E |
| Coverlet | 6.x | Coleta de cobertura de codigo no formato Cobertura XML | CI |
| ReportGenerator | 5.x | Geracao de relatorios HTML a partir de Cobertura XML | CI |

## Cobertura Minima por Camada

Cada camada da arquitetura possui um threshold de cobertura distinto, refletindo a criticidade e testabilidade do codigo.

| Camada | Projeto de Teste | Ferramentas Principais | Cobertura Minima |
|--------|-----------------|----------------------|------------------|
| Domain | Carf.GeoApi.Tests.Unit | xUnit, Moq, Bogus, FluentAssertions | 90% |
| Application | Carf.GeoApi.Tests.Unit | xUnit, Moq, Bogus, FluentAssertions | 80% |
| Infrastructure | Carf.GeoApi.Tests.Integration | xUnit, Testcontainers, Bogus, FluentAssertions | 60% |
| Presentation | Carf.GeoApi.Tests.E2E | xUnit, WebApplicationFactory, Testcontainers | 50% |

## Organizacao dos Projetos de Teste

O solution contem tres projetos de teste, cada um com responsabilidade delimitada.

### Carf.GeoApi.Tests.Unit

Testa a camada Domain e Application em isolamento total. Nenhuma dependencia de banco, rede ou filesystem. Todos os mocks sao injetados via construtor. Execucao rapida (suite completa em menos de 30 segundos).

Estrutura interna:

- `Domain/Entities/` - testes de entidades e aggregate roots
- `Domain/ValueObjects/` - testes de value objects (CPF, Email, GeoPolygon)
- `Domain/Events/` - testes de domain events
- `Application/Commands/` - testes de command handlers
- `Application/Queries/` - testes de query handlers
- `Application/Validators/` - testes de FluentValidation rules
- `Builders/` - test data builders com Bogus
- `Fakes/` - implementacoes fake de interfaces

### Carf.GeoApi.Tests.Integration

Testa repositorios, DbContext, queries espaciais e RLS contra um PostgreSQL real provisionado por Testcontainers. Cada classe de teste usa uma fixture compartilhada (IClassFixture) para reutilizar o container.

Estrutura interna:

- `Repositories/` - testes de repositorios concretos
- `Database/` - testes de constraints, triggers, migrations
- `Fixtures/` - DatabaseFixture, container lifecycle
- `Seeders/` - classes de seed para dados de teste

### Carf.GeoApi.Tests.E2E

Testa o fluxo HTTP completo usando WebApplicationFactory. Substitui Keycloak por um emissor JWT fake e usa Testcontainers para PostgreSQL e Redis.

Estrutura interna:

- `Endpoints/` - testes por controller/endpoint
- `Workflows/` - testes de fluxos multi-etapa
- `Sync/` - testes do protocolo de sincronizacao
- `Fixtures/` - ApiFixture, JWT helper
- `Helpers/` - metodos auxiliares (CreateUnitAsync, AuthenticateAsAsync)

## Convencao de Nomenclatura

Todos os metodos de teste seguem o padrao `MethodName_Scenario_ExpectedResult`.

Exemplos:

| Metodo | Descricao |
|--------|-----------|
| `CreateUnit_WithValidGeometry_ReturnsSuccess` | Criacao de unidade com geometria valida retorna sucesso |
| `Submit_WithoutHolders_ThrowsDomainException` | Submit sem titulares lanca excecao de dominio |
| `GetById_WrongTenant_ReturnsNull` | Busca por ID com tenant incorreto retorna nulo |
| `Push_DuplicateLocalId_IgnoresDuplicate` | Push com localId duplicado ignora a duplicata |
| `Validate_CpfWithRepeatedDigits_ReturnsFailure` | Validacao de CPF com digitos repetidos retorna falha |

Regras adicionais:

- Classes de teste: sufixo `Tests` (ex: `UnitTests`, `CpfTests`, `CreateUnitHandlerTests`)
- Fixture classes: sufixo `Fixture` (ex: `DatabaseFixture`, `ApiFixture`)
- Builder classes: sufixo `Builder` (ex: `UnitBuilder`, `HolderBuilder`)
- Faker classes: sufixo `Faker` (ex: `UnitFaker`, `CommunityFaker`)

## Integracao com CI (GitHub Actions)

O pipeline de CI executa os testes em tres etapas sequenciais, respeitando a piramide.

### Etapa 1 - Testes Unitarios

Executa primeiro por serem os mais rapidos. Se falharem, o pipeline aborta imediatamente.

Comando: `dotnet test Carf.GeoApi.Tests.Unit --collect:"XPlat Code Coverage" --results-directory ./coverage/unit`

### Etapa 2 - Testes de Integracao

Requer Docker (Testcontainers). Executa somente se os unitarios passarem.

Comando: `dotnet test Carf.GeoApi.Tests.Integration --collect:"XPlat Code Coverage" --results-directory ./coverage/integration`

### Etapa 3 - Testes E2E

Requer Docker. Executa somente se os de integracao passarem.

Comando: `dotnet test Carf.GeoApi.Tests.E2E --collect:"XPlat Code Coverage" --results-directory ./coverage/e2e`

### Geracao de Relatorio

Apos todas as etapas, o ReportGenerator combina os relatorios Cobertura XML.

Comando: `reportgenerator -reports:"./coverage/**/coverage.cobertura.xml" -targetdir:"./coverage/report" -reporttypes:"Html;Cobertura" -assemblyfilters:"+Carf.GeoApi.*"`

### Thresholds no GitHub Actions

Os thresholds sao validados como quality gate. Se qualquer camada ficar abaixo do minimo, o pipeline falha.

| Camada | Threshold | Acao ao Falhar |
|--------|-----------|----------------|
| Domain | 90% | Pipeline falha, PR bloqueado |
| Application | 80% | Pipeline falha, PR bloqueado |
| Infrastructure | 60% | Pipeline falha, PR bloqueado |
| Presentation | 50% | Warning no PR, nao bloqueia |

## Principios Gerais

1. **Testes sao cidadaos de primeira classe** - recebem o mesmo rigor de code review que o codigo de producao
2. **Cada teste testa uma unica coisa** - um cenario, uma assertion principal (assertions auxiliares permitidas para setup verification)
3. **Testes sao independentes** - nenhum teste depende da ordem de execucao ou do resultado de outro teste
4. **Dados de teste sao gerados** - Bogus gera dados aleatorios mas deterministicos (seed fixa por classe)
5. **Cleanup automatico** - testes de integracao usam transaction rollback, E2E usam database recreate por fixture
6. **Nao mockar o que nao precisa** - value objects e entidades sao usados diretamente, mocks apenas para interfaces de infraestrutura

## Referencias Cruzadas

- Testes unitarios de dominio: `TESTS/UNIT/01-domain-unit-tests.md`
- Testes de value objects: `TESTS/UNIT/02-value-object-tests.md`
- Testes de command handlers: `TESTS/UNIT/03-command-handler-tests.md`
- Testes de repositorios: `TESTS/INTEGRATION/01-repository-tests.md`
- Testes de banco de dados: `TESTS/INTEGRATION/02-database-tests.md`
- Testes E2E da API: `TESTS/E2E/01-api-e2e-tests.md`
- Testes E2E de sincronizacao: `TESTS/E2E/02-sync-e2e-tests.md`
