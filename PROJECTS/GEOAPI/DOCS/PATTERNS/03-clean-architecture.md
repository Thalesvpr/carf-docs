---
type: leaf
status: approved
updated: 2026-02-07
---

# Clean Architecture

A GEOAPI e estruturada em quatro camadas concentricas com dependencia unidirecional apontando sempre para dentro. Cada camada compila em um assembly .NET separado (projeto .csproj proprio), e o enforcement da regra de dependencia acontece em tempo de build: project references unidirecionais impedem que uma camada interna referencie uma externa. Nenhuma violacao dessa regra compila.

## Domain

Camada mais interna. Contem entidades (Unit, Holder, Community, Team e todas as demais documentadas em ENTITIES/), value objects imutaveis (CPF, Email, GeoPolygon, Address), contratos de repositorio e servicos (IUnitRepository, IHolderRepository, IFileStorage, IEmailService), domain events (UnitCreatedEvent, HolderLinkedEvent, UnitStatusChangedEvent) e excecoes de negocio (ValidationException, ConflictException, AccessDeniedException).

Zero dependencias externas. Nenhum pacote NuGet de framework, ORM, HTTP ou infraestrutura. A unica referencia permitida e a biblioteca padrao do .NET. Todas as regras de negocio residem aqui. Entidades validam suas proprias invariantes: Unit verifica que area e positiva e que boundary e um poligono valido, Holder valida CPF via Mod11 e verifica obrigatoriedade condicional de dados do conjuge.

Os contratos definem interfaces que serao implementadas pela camada de Infrastructure. O Domain declara o que precisa sem saber como sera implementado. IUnitRepository declara metodos como GetByIdAsync, GetByCommunityAsync e SaveAsync sem mencionar EF Core ou PostgreSQL.

## Application

Camada que orquestra os casos de uso do sistema. Contem commands representando intencoes de escrita (CreateUnitCommand, LinkHolderCommand, ApproveUnitCommand), queries representando leituras (GetUnitByIdQuery, ListUnitsByCommunityQuery), DTOs de request e response (UnitDto, HolderDetailDto, PaginatedResult), validators FluentValidation que validam commands antes da execucao dos handlers e mappers que convertem entre entidades de dominio e DTOs.

Depende exclusivamente da camada Domain. Usa as interfaces de contratos definidas la sem conhecer as implementacoes concretas. Os handlers de commands e queries sao processados via MediatR, que tambem gerencia o pipeline de cross-cutting concerns: validation behavior executa o FluentValidation antes do handler, logging behavior registra entrada e saida de cada operacao e transaction behavior envolve commands em transacao.

## Infrastructure

Camada que implementa os contratos definidos pelo Domain e fornece adaptadores para tecnologias externas. Contem o DbContext do EF Core (GeoApiDbContext) com mapeamento de todas as entidades para tabelas PostgreSQL, implementacoes concretas dos repositorios (UnitRepository usando DbSet e IQueryable), integracao com Keycloak para validacao de tokens e sincronizacao de usuarios, cliente S3 para armazenamento de arquivos, servico de cache Redis, jobs Hangfire para processamento assincrono de ortofotos e cliente SMTP para notificacoes por email.

Depende do Domain (implementa seus contratos) e do Application (implementa interfaces de servicos de aplicacao quando existem). Nao depende da camada Presentation. As migrations do EF Core residem aqui, versionando o schema do banco de dados de forma incremental.

## Presentation

Camada mais externa, ponto de entrada HTTP. Contem controllers ASP.NET Core que recebem requisicoes HTTP e delegam para commands e queries via MediatR, middlewares de tratamento de excecoes (converte excecoes de dominio em respostas RFC 7807), filtros de validacao, hubs SignalR para notificacoes real-time e a configuracao de Dependency Injection que registra todos os servicos no container.

Depende de todas as camadas, mas e uma camada fina: controllers nao contem logica de negocio, apenas traduzem HTTP para commands/queries e formatam as respostas. Qualquer logica que apareca em um controller e candidata a ser movida para Application ou Domain.

## Regra de Dependencia

Domain nao conhece ninguem. Application depende so de Domain. Infrastructure depende de Application e Domain. Presentation depende de tudo mas e camada fina substituivel. Essa regra garante que a logica de negocio pode ser testada sem banco de dados, sem HTTP e sem servicos externos, usando apenas mocks das interfaces do Domain.
