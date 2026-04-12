---
type: leaf
status: review
updated: 2026-02-08
---

# Domain Unit Tests

Os testes unitarios da camada de dominio validam regras de negocio, value objects e command handlers sem dependencia de banco de dados ou infraestrutura externa. Utilizam xUnit com FluentAssertions e Moq para mocks de repositorios.

## Convencao de Nomenclatura

Todos os metodos de teste seguem o padrao `MethodName_Scenario_ExpectedResult`:

| Exemplo | Descricao |
|---------|-----------|
| `CreateUnit_WithValidGeometry_ReturnsSuccess` | Criacao valida retorna sucesso |
| `Submit_WithoutHolders_ThrowsDomainException` | Submit sem titulares lanca excecao |
| `Approve_WhenPending_ChangesStatusToApproved` | Aprovacao quando Pending muda status |
| `Approve_WhenDraft_ThrowsDomainException` | Aprovacao quando Draft lanca excecao |
| `LinkHolder_OwnershipExceeds100_ThrowsDomainException` | Vincular titular que excede 100% lanca excecao |
| `Create_WithRepeatedCpf_ThrowsDomainException` | CPF com digitos repetidos lanca excecao |

## Patterns de Mock

### IRepository (generico)

Cada repositorio e mockado via Moq com setup de retorno assincrono:

- `mockUnitRepo.Setup(r => r.GetByIdAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>())).ReturnsAsync(unitEntity)` - retorna entidade pre-construida pelo builder
- `mockUnitRepo.Setup(r => r.AddAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>())).Returns(Task.CompletedTask)` - aceita adicao sem efeito
- `mockUnitRepo.Setup(r => r.HasOverlapAsync(It.IsAny<Geometry>(), It.IsAny<Guid>(), It.IsAny<CancellationToken>())).ReturnsAsync(false)` - sem sobreposicao por default

Verificacao apos act:

- `mockUnitRepo.Verify(r => r.AddAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>()), Times.Once)` - confirma que AddAsync foi chamado exatamente uma vez
- `mockUnitRepo.Verify(r => r.AddAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>()), Times.Never)` - confirma que AddAsync nunca foi chamado (cenario de falha)

### IUnitOfWork

Mock do unit of work para verificar commits:

- `mockUow.Setup(u => u.CommitAsync(It.IsAny<CancellationToken>())).ReturnsAsync(1)` - retorna 1 (registros afetados)
- Verificacao: `mockUow.Verify(u => u.CommitAsync(It.IsAny<CancellationToken>()), Times.Once)` - confirma commit chamado

### ITenantProvider

Mock do provider multi-tenant:

- `mockTenant.Setup(t => t.GetTenantId()).Returns(Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"))` - retorna GUID fixo de teste
- Para testes de tenant nao encontrado: `mockTenant.Setup(t => t.GetTenantId()).Returns(Guid.Empty)`

### ICurrentUser

Mock do usuario corrente:

- `mockUser.Setup(u => u.Id).Returns(Guid.NewGuid())`
- `mockUser.Setup(u => u.Roles).Returns(new[] { "COORDINATOR" })` - role de coordenador
- `mockUser.Setup(u => u.Roles).Returns(new[] { "CADASTRATOR" })` - role de cadastrador

### IDateTimeProvider

Mock para testes deterministicos de timestamp:

- `mockDateTime.Setup(d => d.UtcNow).Returns(new DateTime(2026, 1, 15, 10, 30, 0, DateTimeKind.Utc))` - data fixa

## Test Data Builders com Bogus

### UnitBuilder

Gera instancias validas da entidade Unit usando Bogus para dados aleatorios mas deterministicos:

- `new UnitBuilder().Build()` - Unit com status Draft, geometria valida (quadrado 100m na regiao de Brasilia), area calculada, codigo UNI-2026-NNNNN
- `new UnitBuilder().WithStatus(UnitStatus.Pending).Build()` - Unit com status especifico (inclui holder automaticamente se Pending)
- `new UnitBuilder().WithGeometry(polygon).Build()` - Unit com geometria customizada
- `new UnitBuilder().WithHolder(holder).Build()` - Unit com titular pre-vinculado
- `new UnitBuilder().WithTenantId(tenantId).Build()` - Unit para tenant especifico
- `new UnitBuilder().WithCode("UNI-2026-00042").Build()` - Unit com codigo especifico

Internamente: `faker.Random.Guid()` para IDs, `faker.Address.FullAddress()` para enderecos, `GeoPolygonBuilder` para geometria com coordenadas base em Brasilia (lat -15.7, lng -47.9).

### HolderBuilder

Gera instancias validas da entidade Holder:

- `new HolderBuilder().Build()` - Holder pessoa fisica com CPF valido (gerado via Mod-11), nome via `faker.Person.FullName`, email via `faker.Internet.Email()`
- `new HolderBuilder().AsJuridica().Build()` - Holder pessoa juridica com CNPJ, razao social via `faker.Company.CompanyName()`
- `new HolderBuilder().WithCpf("52998224725").Build()` - CPF especifico
- `new HolderBuilder().WithOwnershipPercentage(50m).Build()` - percentual de titularidade
- `new HolderBuilder().WithIsPrimary(true).Build()` - titular primario

### CommunityBuilder

Gera instancias validas da entidade Community:

- `new CommunityBuilder().Build()` - Community com boundary aleatorio (poligono grande ~1km2), nome via `faker.Address.City()`, tipo REURB_S
- `new CommunityBuilder().WithBoundary(polygon).Build()` - boundary customizado
- `new CommunityBuilder().WithType(CommunityType.Quilombola).Build()` - tipo especifico
- `new CommunityBuilder().ContainingPoint(lat, lng).Build()` - boundary que garante conter o ponto

## Testes da Entidade Unit

A classe `UnitTests` exercita o ciclo de vida completo e as invariantes da entidade Unit.

### Ciclo de Vida (State Machine)

| Cenario | Estado Inicial | Acao | Estado Final | Assertion |
|---------|---------------|------|-------------|-----------|
| Criar com dados validos | (novo) | Unit.Create(...) | Draft | Status Draft, area > 0, codigo UNI-YYYY-NNNNN, DomainEvents contem UnitCreatedEvent |
| Submit com titulares validos | Draft (holders somam 100%) | unit.Submit() | Pending | Status Pending, UnitStatusChangedEvent emitido |
| Submit sem titulares | Draft (sem holders) | unit.Submit() | Draft (inalterado) | Lanca DomainException "At least one holder required" |
| Submit com percentual incompleto | Draft (holders somam 80%) | unit.Submit() | Draft (inalterado) | Lanca DomainException "Ownership must sum to 100%" |
| Approve quando Pending | Pending | unit.Approve(userId) | Approved | Status Approved, ApprovedBy = userId, ApprovedAt preenchido |
| Approve quando Draft | Draft | unit.Approve(userId) | Draft (inalterado) | Lanca DomainException "Cannot approve unit in Draft status" |
| Reject quando Pending | Pending | unit.Reject(reason) | Rejected | Status Rejected, RejectionReason preenchido |
| Reject sem motivo | Pending | unit.Reject("") | Pending (inalterado) | Lanca DomainException "Rejection reason is required" |
| Return para revisao | Rejected | unit.ReturnToReview() | Draft | Status Draft, permite re-edicao |
| Archive quando Approved | Approved | unit.Archive() | Archived | Status Archived |

### Vinculacao de Titulares

| Cenario | Setup | Acao | Assertion |
|---------|-------|------|-----------|
| Vincular titular valido | Unit Draft, holder valido | unit.LinkHolder(holder, 50m) | Holders contem holder, HolderLinkedEvent emitido |
| Vincular titular duplicado | Unit ja contem holder | unit.LinkHolder(sameHolder, 20m) | Lanca DomainException "Holder already linked" |
| Percentual excede 100% | Unit com holder 80% | unit.LinkHolder(newHolder, 30m) | Lanca DomainException "Ownership exceeds 100%" |
| Desvincular titular | Unit com 2 holders | unit.UnlinkHolder(holderId) | Holders nao contem holder, HolderUnlinkedEvent emitido |
| Desvincular unico holder (Draft) | Unit Draft com 1 holder | unit.UnlinkHolder(holderId) | Permitido em Draft (unit volta a nao ter holders) |
| Desvincular unico holder (Pending) | Unit Pending com 1 holder | unit.UnlinkHolder(holderId) | Lanca DomainException "Cannot remove last holder from Pending unit" |
| Definir titular primario | Unit com 2 holders | unit.SetPrimaryHolder(holderId) | Holder marcado como primario, apenas 1 primario |

### Geometria

| Cenario | Setup | Acao | Assertion |
|---------|-------|------|-----------|
| Atribuir geometria valida | Unit Draft | unit.SetGeometry(polygon) | Geometry atualizada, area recalculada |
| Geometria com auto-intersecao | Unit Draft | unit.SetGeometry(invalidPolygon) | Lanca DomainException "Self-intersecting geometry" |
| Area recalculada | Unit Draft | unit.SetGeometry(newPolygon) | Area atualizada para valor correto |
| SRID incorreto | Unit Draft | unit.SetGeometry(polygon3857) | Lanca DomainException "SRID must be 4326" |

## Testes da Entidade Holder

A classe `HolderTests` exercita a criacao e validacao de titulares.

| Cenario | Acao | Assertion |
|---------|------|-----------|
| Criar pessoa fisica valida | Holder.CreatePessoaFisica(cpf, nome, ...) | Instancia criada, Type = PessoaFisica |
| Criar pessoa juridica valida | Holder.CreatePessoaJuridica(cnpj, razao, ...) | Instancia criada, Type = PessoaJuridica |
| CPF invalido | Holder.CreatePessoaFisica(invalidCpf, ...) | Lanca DomainException INVALID_CPF |
| Email invalido | Holder.CreatePessoaFisica(cpf, nome, invalidEmail) | Lanca DomainException INVALID_EMAIL |
| Atualizar dados | holder.UpdateInfo(novoNome, novoEmail) | Propriedades atualizadas |
| Atualizar CPF (imutavel) | holder.UpdateCpf(novoCpf) | Lanca DomainException "CPF cannot be changed" |

## Testes da Entidade Community

A classe `CommunityTests` exercita o ciclo de vida da comunidade.

| Cenario | Acao | Assertion |
|---------|------|-----------|
| Criar community valida | Community.Create(nome, boundary, tipo) | Instancia criada, CommunityCreatedEvent emitido |
| Alterar boundary | community.ChangeBoundary(newPolygon) | Boundary atualizado, CommunityBoundaryChangedEvent emitido |
| Boundary invalido | community.ChangeBoundary(invalidPolygon) | Lanca DomainException INVALID_GEOMETRY |
| Adicionar bloco | community.AddBlock(blockName) | Block adicionado, BlockAddedEvent emitido |
| Nome duplicado de bloco | community.AddBlock(existingName) | Lanca DomainException "Block name already exists" |
| Arquivar community | community.Archive() | Status Archived, CommunityArchivedEvent emitido |
| Arquivar com unidades ativas | community com units nao-arquivadas | Lanca DomainException "Cannot archive community with active units" |

## Testes de Value Objects

A classe `CPFTests` valida a criacao e formatacao do value object CPF. Aceita tanto formato numerico puro quanto com mascara, normalizando para 11 digitos. Rejeita CPFs com digito verificador invalido, sequencias repetidas e valores nao numericos, lancando DomainException. O metodo Masked retorna o CPF ofuscado no formato asterisco-asterisco-asterisco-digitos.

A classe `AddressTests` confirma que a propriedade FullAddress formata corretamente o endereco completo concatenando logradouro, numero, complemento, bairro, cidade e UF.

Para detalhes completos dos testes de value objects, consulte `TESTS/UNIT/02-value-object-tests.md`.

## Testes de Command Handlers

A classe `CreateUnitHandlerTests` utiliza mocks de IUnitRepository e IGeometryValidator para testar o handler de criacao de unidades em isolamento.

| Cenario | Setup dos Mocks | Resultado |
|---------|----------------|-----------|
| Comando valido | Geometria valida, sem sobreposicao | Result.IsSuccess verdadeiro, repositorio recebe chamada AddAsync uma vez, UnitCreatedEvent emitido |
| Geometria invalida | Validador retorna falso | Result.IsFailure verdadeiro, codigo de erro INVALID_GEOMETRY, repositorio nunca chamado |
| Sobreposicao detectada | HasOverlapAsync retorna verdadeiro | Result.IsFailure verdadeiro, codigo GEOMETRY_OVERLAP |
| Tenant nao encontrado | GetTenantId retorna Guid.Empty | Result.IsFailure verdadeiro, codigo TENANT_NOT_FOUND |

Para detalhes completos dos testes de handlers, consulte `TESTS/UNIT/03-command-handler-tests.md`.

## Padroes de FluentAssertions

Assertions padronizadas utilizadas em todos os testes de dominio:

| Padrao | Exemplo | Uso |
|--------|---------|-----|
| Sucesso de resultado | `result.IsSuccess.Should().BeTrue()` | Validar operacao bem-sucedida |
| Falha de resultado | `result.IsFailure.Should().BeTrue()` | Validar operacao rejeitada |
| Codigo de erro | `result.Error.Code.Should().Be("INVALID_GEOMETRY")` | Validar codigo de erro especifico |
| Status de entidade | `entity.Status.Should().Be(UnitStatus.Draft)` | Validar estado da entidade |
| Excecao lancada | `act.Should().Throw<DomainException>()` | Validar excecao de dominio |
| Excecao com mensagem | `act.Should().Throw<DomainException>().WithMessage("*required*")` | Validar mensagem da excecao |
| Colecao contem | `entity.Holders.Should().Contain(holder)` | Validar presenca em colecao |
| Colecao vazia | `entity.Holders.Should().BeEmpty()` | Validar colecao vazia |
| Domain event emitido | `entity.DomainEvents.Should().ContainSingle<UnitCreatedEvent>()` | Validar evento emitido |
| Propriedade do event | `entity.DomainEvents.OfType<UnitCreatedEvent>().Single().UnitId.Should().Be(entity.Id)` | Validar dados do evento |
| Valor nao nulo | `entity.ApprovedAt.Should().NotBeNull()` | Validar preenchimento |
| Valor aproximado | `entity.Area.Should().BeApproximately(10000, 100)` | Validar valor com tolerancia |

## Organizacao dos Testes

```
Carf.GeoApi.Tests.Unit/
  Domain/
    Entities/
      UnitTests.cs
      HolderTests.cs
      CommunityTests.cs
      BlockTests.cs
      DocumentTests.cs
    ValueObjects/
      CpfTests.cs
      EmailTests.cs
      GeoPolygonTests.cs
      GeoPointTests.cs
      AddressTests.cs
      PhoneNumberTests.cs
      CreaTests.cs
      UnitStatusTests.cs
    Events/
      DomainEventTests.cs
  Application/
    Commands/
      CreateUnitHandlerTests.cs
      UpdateUnitHandlerTests.cs
      LinkHolderHandlerTests.cs
      SubmitUnitHandlerTests.cs
      ApproveUnitHandlerTests.cs
      RejectUnitHandlerTests.cs
      UploadDocumentHandlerTests.cs
      CreateCommunityHandlerTests.cs
    Validators/
      CreateUnitCommandValidatorTests.cs
      LinkHolderCommandValidatorTests.cs
    Behaviors/
      ValidationBehaviorTests.cs
  Builders/
    UnitBuilder.cs
    HolderBuilder.cs
    CommunityBuilder.cs
    GeoPolygonBuilder.cs
    CommandBuilders.cs
  Fakes/
    FakeTenantProvider.cs
    FakeCurrentUser.cs
    FakeDateTimeProvider.cs
```

## Referencias Cruzadas

- Testes de value objects: `TESTS/UNIT/02-value-object-tests.md`
- Testes de command handlers: `TESTS/UNIT/03-command-handler-tests.md`
- Estrategia de testes: `TESTS/00-testing-strategy.md`
- Entidades do dominio: `DOMAIN/ENTITIES/`
- Value objects: `DOMAIN/VALUE-OBJECTS/`
- Domain events: `DOMAIN/EVENTS/`
