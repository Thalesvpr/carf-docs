---
type: leaf
status: review
updated: 2026-02-08
---

# Command Handler Tests

Este documento detalha os padroes de teste para command handlers CQRS implementados com MediatR. Cada handler e testado em isolamento total, com mocks de repositorios e services, verificando resultados, efeitos colaterais e domain events emitidos.

## Padrao Arrange-Act-Assert

Todos os testes de handlers seguem rigorosamente o padrao AAA:

**Arrange** - Configura mocks, cria o command com dados de teste via builders, instancia o handler com as dependencias mockadas.

**Act** - Chama `handler.Handle(command, CancellationToken.None)` e captura o resultado.

**Assert** - Verifica o resultado (sucesso/falha), verifica chamadas aos mocks (AddAsync, CommitAsync), verifica domain events emitidos na entidade.

## Setup de Mocks Comuns

### IRepository (generico)

Cada repositorio concreto (IUnitRepository, IHolderRepository, ICommunityRepository) e mockado individualmente. O padrao de setup:

- `mockRepo.Setup(r => r.GetByIdAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>())).ReturnsAsync(entity)` - retorna entidade pre-construida
- `mockRepo.Setup(r => r.AddAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>())).Returns(Task.CompletedTask)` - aceita adicao
- `mockRepo.Setup(r => r.UpdateAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>())).Returns(Task.CompletedTask)` - aceita atualizacao
- `mockRepo.Setup(r => r.DeleteAsync(It.IsAny<Guid>(), It.IsAny<CancellationToken>())).Returns(Task.CompletedTask)` - aceita exclusao

### IUnitOfWork

Mock do unit of work para verificar que CommitAsync foi chamado apos operacoes de escrita:

- `mockUow.Setup(u => u.CommitAsync(It.IsAny<CancellationToken>())).ReturnsAsync(1)` - retorna 1 (uma entidade afetada)
- Verificacao: `mockUow.Verify(u => u.CommitAsync(It.IsAny<CancellationToken>()), Times.Once)` - confirma que commit foi chamado exatamente uma vez

### ITenantProvider

Mock do provider de tenant para isolar o contexto multi-tenant:

- `mockTenant.Setup(t => t.GetTenantId()).Returns(Guid.Parse("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"))` - retorna GUID fixo de teste
- Usado em handlers que precisam filtrar por tenant ou associar entidades ao tenant corrente

### ICurrentUser

Mock do usuario corrente para testes de autorizacao:

- `mockUser.Setup(u => u.Id).Returns(Guid.NewGuid())` - ID do usuario
- `mockUser.Setup(u => u.Email).Returns("agente@carf.gov.br")` - email
- `mockUser.Setup(u => u.Roles).Returns(new[] { "COORDINATOR" })` - roles

### IDateTimeProvider

Mock do provider de data/hora para testes deterministicos:

- `mockDateTime.Setup(d => d.UtcNow).Returns(new DateTime(2026, 1, 15, 10, 30, 0, DateTimeKind.Utc))` - data fixa

### IDomainEventDispatcher

Mock do dispatcher de domain events. Em testes unitarios, os events sao coletados na entidade e verificados diretamente, sem dispatch real:

- `mockDispatcher.Setup(d => d.DispatchAsync(It.IsAny<IReadOnlyList<IDomainEvent>>(), It.IsAny<CancellationToken>())).Returns(Task.CompletedTask)`

## Verificacao de Domain Events

Apos a execucao do handler, os domain events emitidos pela entidade sao verificados diretamente na colecao `DomainEvents` do aggregate root.

Padroes de verificacao:

- **Event emitido**: `entity.DomainEvents.Should().ContainSingle<UnitCreatedEvent>()`
- **Propriedades do event**: `entity.DomainEvents.OfType<UnitCreatedEvent>().Single().UnitId.Should().Be(entity.Id)`
- **Nenhum event**: `entity.DomainEvents.Should().BeEmpty()`
- **Multiplos events**: `entity.DomainEvents.Should().HaveCount(2).And.ContainItemsAssignableTo<IDomainEvent>()`
- **Ordem dos events**: `entity.DomainEvents[0].Should().BeOfType<UnitCreatedEvent>(); entity.DomainEvents[1].Should().BeOfType<HolderLinkedEvent>()`

## Teste de ValidationBehavior (Pipeline)

O `ValidationBehavior<TRequest, TResponse>` e um behavior do pipeline MediatR que executa os validators FluentValidation antes do handler. Testado separadamente.

### Setup

Instanciar o behavior com uma lista de validators mockados ou reais:

- Criar instancia do validator concreto (ex: `CreateUnitCommandValidator`)
- Criar instancia do `ValidationBehavior` passando o array de validators
- Chamar `behavior.Handle(command, next, CancellationToken.None)` onde `next` e um delegate mockado

### Cenarios

| Cenario | Setup | Assertion |
|---------|-------|-----------|
| Comando valido | Validator nao retorna erros | Delegate `next` e invocado, resultado e o retorno do handler |
| Comando invalido (1 erro) | Validator retorna 1 erro | Lanca ValidationException com 1 erro, delegate `next` nao e invocado |
| Comando invalido (multiplos erros) | Validator retorna 3 erros | Lanca ValidationException com 3 erros na colecao Errors |
| Sem validators registrados | Lista vazia de validators | Delegate `next` e invocado normalmente |

## Test Data Builders com Bogus

### UnitBuilder

Gera instancias validas da entidade Unit para uso em testes:

- `new UnitBuilder().Build()` - Unit com dados aleatorios validos (Draft)
- `new UnitBuilder().WithStatus(UnitStatus.Pending).Build()` - Unit com status especifico
- `new UnitBuilder().WithHolder(holder).Build()` - Unit com titular pre-vinculado
- `new UnitBuilder().WithGeometry(polygon).Build()` - Unit com geometria especifica
- `new UnitBuilder().WithTenantId(tenantId).Build()` - Unit com tenant especifico
- `new UnitBuilder().WithCode("UNI-2026-00001").Build()` - Unit com codigo especifico

Internamente usa Bogus: `faker.Random.Guid()` para IDs, `faker.Address.FullAddress()` para enderecos, `GeoPolygonBuilder` para geometria.

### HolderBuilder

Gera instancias validas da entidade Holder:

- `new HolderBuilder().Build()` - Holder pessoa fisica com CPF valido
- `new HolderBuilder().AsJuridica().Build()` - Holder pessoa juridica com CNPJ
- `new HolderBuilder().WithCpf("52998224725").Build()` - Holder com CPF especifico
- `new HolderBuilder().WithOwnershipPercentage(50m).Build()` - Holder com percentual especifico

### CommunityBuilder

Gera instancias validas da entidade Community:

- `new CommunityBuilder().Build()` - Community com boundary aleatorio
- `new CommunityBuilder().WithBoundary(polygon).Build()` - Community com boundary especifico
- `new CommunityBuilder().WithType(CommunityType.Quilombola).Build()` - Community com tipo especifico

### CommandBuilder

Gera instancias validas de commands para MediatR:

- `new CreateUnitCommandBuilder().Build()` - comando de criacao com dados aleatorios validos
- `new LinkHolderCommandBuilder().WithUnitId(unitId).Build()` - comando com UnitId especifico
- `new SubmitUnitCommandBuilder().WithUnitId(unitId).Build()` - comando de submit

## Handlers e Cenarios de Teste

### CreateUnitHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Comando valido sem sobreposicao | IUnitRepository.HasOverlapAsync retorna falso, IGeometryValidator.IsValid retorna verdadeiro | Result.IsSuccess, repo.AddAsync chamado 1x, UnitCreatedEvent emitido |
| Geometria invalida | IGeometryValidator.IsValid retorna falso | Result.IsFailure, codigo INVALID_GEOMETRY, repo.AddAsync nunca chamado |
| Sobreposicao detectada | IUnitRepository.HasOverlapAsync retorna verdadeiro | Result.IsFailure, codigo GEOMETRY_OVERLAP |
| Tenant nao encontrado | ITenantProvider.GetTenantId retorna Guid.Empty | Result.IsFailure, codigo TENANT_NOT_FOUND |
| Codigo gerado no formato correto | Nenhum mock especial | entity.Code comeca com "UNI-" seguido do ano e sequencial |

### UpdateUnitHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Atualizar unidade Draft | IUnitRepository.GetByIdAsync retorna Unit(Draft) | Result.IsSuccess, propriedades atualizadas, UnitOfWork.CommitAsync chamado |
| Atualizar unidade Approved | IUnitRepository.GetByIdAsync retorna Unit(Approved) | Result.IsFailure, codigo CANNOT_EDIT_APPROVED_UNIT |
| Unidade nao encontrada | IUnitRepository.GetByIdAsync retorna null | Result.IsFailure, codigo UNIT_NOT_FOUND |
| Novo poligono com sobreposicao | HasOverlapAsync retorna verdadeiro (excluindo a propria unidade) | Result.IsFailure, codigo GEOMETRY_OVERLAP |

### LinkHolderHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Vincular titular valido | IUnitRepository.GetByIdAsync retorna Unit, IHolderRepository.GetByIdAsync retorna Holder | Result.IsSuccess, HolderLinkedEvent emitido |
| Unidade nao encontrada | IUnitRepository.GetByIdAsync retorna null | Result.IsFailure, codigo UNIT_NOT_FOUND |
| Titular nao encontrado | IHolderRepository.GetByIdAsync retorna null | Result.IsFailure, codigo HOLDER_NOT_FOUND |
| Titular ja vinculado | Unit ja contem o holder | Result.IsFailure, codigo HOLDER_ALREADY_LINKED |
| Percentual excede 100% | Holders existentes somam 80%, novo holder com 30% | Result.IsFailure, codigo OWNERSHIP_EXCEEDS_100 |

### UnlinkHolderHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Desvincular titular existente | Unit com 2 holders | Result.IsSuccess, HolderUnlinkedEvent emitido |
| Desvincular unico titular | Unit com 1 holder (status Draft) | Result.IsSuccess (permitido em Draft) |
| Desvincular quando Pending | Unit com 1 holder (status Pending) | Result.IsFailure, codigo CANNOT_REMOVE_LAST_HOLDER |
| Titular nao vinculado | Unit nao contem o holderId | Result.IsFailure, codigo HOLDER_NOT_LINKED |

### SubmitUnitHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Submit valido | Unit(Draft) com holders, percentuais somam 100% | Result.IsSuccess, status muda para Pending, UnitStatusChangedEvent emitido |
| Sem titulares | Unit(Draft) sem holders | Result.IsFailure, codigo NO_HOLDERS_LINKED |
| Percentuais nao somam 100% | Unit com holders somando 80% | Result.IsFailure, codigo OWNERSHIP_NOT_100 |
| Status invalido (ja Pending) | Unit(Pending) | Result.IsFailure, codigo INVALID_STATUS_TRANSITION |
| Geometria ausente | Unit(Draft) sem geometria | Result.IsFailure, codigo GEOMETRY_REQUIRED |

### ApproveUnitHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Aprovacao valida | Unit(Pending), ICurrentUser com role COORDINATOR | Result.IsSuccess, status muda para Approved |
| Status invalido (Draft) | Unit(Draft) | Result.IsFailure, codigo INVALID_STATUS_TRANSITION |
| Sem permissao | ICurrentUser com role CADASTRATOR | Result.IsFailure, codigo ACCESS_DENIED |
| Unidade nao encontrada | GetByIdAsync retorna null | Result.IsFailure, codigo UNIT_NOT_FOUND |

### RejectUnitHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Rejeicao valida com motivo | Unit(Pending), motivo preenchido | Result.IsSuccess, status muda para Rejected, UnitStatusChangedEvent emitido |
| Sem motivo de rejeicao | Unit(Pending), motivo vazio | Result.IsFailure, codigo REJECTION_REASON_REQUIRED |
| Status invalido | Unit(Draft) | Result.IsFailure, codigo INVALID_STATUS_TRANSITION |

### UploadDocumentHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Upload valido | IFileStorage.UploadAsync retorna URL, tipo valido | Result.IsSuccess, DocumentUploadedEvent emitido |
| Tipo de documento invalido | Tipo nao listado no enum DocumentType | Result.IsFailure, codigo INVALID_DOCUMENT_TYPE |
| Arquivo excede tamanho maximo | Stream com mais de 10MB | Result.IsFailure, codigo FILE_TOO_LARGE |
| Entidade pai nao encontrada | GetByIdAsync retorna null | Result.IsFailure, codigo ENTITY_NOT_FOUND |

### CreateCommunityHandler

| Cenario | Mocks Necessarios | Assertion |
|---------|-------------------|-----------|
| Criacao valida | Boundary valido, nome unico | Result.IsSuccess, CommunityCreatedEvent emitido |
| Nome duplicado no tenant | ICommunityRepository.ExistsByNameAsync retorna verdadeiro | Result.IsFailure, codigo COMMUNITY_NAME_DUPLICATE |
| Boundary invalido | IGeometryValidator.IsValid retorna falso | Result.IsFailure, codigo INVALID_GEOMETRY |

## Padroes de FluentAssertions para Handlers

Assertions comuns utilizadas nos testes de handlers:

- **Sucesso**: `result.IsSuccess.Should().BeTrue(); result.Value.Should().NotBeNull();`
- **Falha com codigo**: `result.IsFailure.Should().BeTrue(); result.Error.Code.Should().Be("INVALID_GEOMETRY");`
- **Mock chamado**: `mockRepo.Verify(r => r.AddAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>()), Times.Once);`
- **Mock nao chamado**: `mockRepo.Verify(r => r.AddAsync(It.IsAny<Unit>(), It.IsAny<CancellationToken>()), Times.Never);`
- **UoW commitado**: `mockUow.Verify(u => u.CommitAsync(It.IsAny<CancellationToken>()), Times.Once);`
- **Status da entidade**: `entity.Status.Should().Be(UnitStatus.Pending);`
- **Domain event emitido**: `entity.DomainEvents.Should().ContainSingle<UnitCreatedEvent>();`
- **Propriedade do event**: `entity.DomainEvents.OfType<HolderLinkedEvent>().Single().HolderId.Should().Be(holderId);`

## Tabela Resumo

| Handler | Total de Cenarios | Sucesso | Falha | Edge Cases |
|---------|-------------------|---------|-------|------------|
| CreateUnitHandler | 5 | 1 | 3 | 1 |
| UpdateUnitHandler | 4 | 1 | 3 | 0 |
| LinkHolderHandler | 5 | 1 | 4 | 0 |
| UnlinkHolderHandler | 4 | 1 | 2 | 1 |
| SubmitUnitHandler | 5 | 1 | 4 | 0 |
| ApproveUnitHandler | 4 | 1 | 3 | 0 |
| RejectUnitHandler | 3 | 1 | 2 | 0 |
| UploadDocumentHandler | 4 | 1 | 3 | 0 |
| CreateCommunityHandler | 3 | 1 | 2 | 0 |
| **Total** | **37** | **9** | **26** | **2** |

## Referencias Cruzadas

- Definicao dos handlers: `APPLICATION/COMMANDS/`
- Validators dos commands: `APPLICATION/VALIDATORS/`
- Entidades testadas: `DOMAIN/ENTITIES/`
- Domain events: `DOMAIN/EVENTS/`
- Estrategia geral de testes: `TESTS/00-testing-strategy.md`
