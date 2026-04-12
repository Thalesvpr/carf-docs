---
type: leaf
status: review
updated: 2026-02-08
---

# Data Flow

O fluxo de dados na GEOAPI segue a estrutura de Clean Architecture onde cada requisicao HTTP atravessa camadas concentricas com responsabilidades bem definidas.

## Request Flow

A requisicao HTTP chega ao controller que deserializa JSON para DTO. O ExceptionHandlingMiddleware envolve toda a pipeline para captura de erros. O middleware de autenticacao valida o JWT e extrai claims. O TenantMiddleware extrai tenant_id do JWT e executa SET LOCAL app.current_tenant no PostgreSQL. O ValidationFilter valida o DTO via ModelState. O controller despacha Command ou Query via MediatR.

## Command Flow

Para operacoes de escrita, o MediatR executa pipeline behaviors na ordem: ValidationBehavior (FluentValidation antes do handler), LoggingBehavior (loga entrada e saida), AuditLoggingBehavior (captura snapshots antes e depois). O handler recebe o command, injeta interfaces de repositorio e servicos, valida regras de negocio via Domain Entity, cria ou atualiza a entidade, persiste via Repository.Add e UnitOfWork.SaveChanges e dispara Domain Events via IDomainEventDispatcher. O resultado e mapeado para DTO e retornado ao controller.

## Query Flow

Para operacoes de leitura, o handler pode acessar DbContext diretamente para performance, projetando para DTO via Select sem materializar a entidade completa. Aplica filtros Where, ordenacao OrderBy e paginacao Skip/Take. O resultado e retornado sem passar pela camada Domain, otimizando leituras frequentes.

## Multi-Tenancy Flow

O JWT contem claim tenant_id. O TenantMiddleware extrai o claim e define a variavel de sessao app.current_tenant no PostgreSQL via ExecuteSqlRaw com parameter binding. Policies RLS filtram automaticamente todas as tabelas por tenant_id sem necessidade de filtro explicito no codigo.

## Error Handling Flow

Excecoes de dominio (ValidationException, NotFoundException, ConflictException) sao capturadas pelo ExceptionHandlingMiddleware e convertidas para ProblemDetails RFC 7807 com status HTTP apropriado. Erros 500 logam exception completa via Serilog, erros abaixo de 500 logam apenas mensagem. Mensagens internas nunca sao expostas em respostas 500.

## Caching Flow

Query handlers verificam IDistributedCache (Redis) antes de consultar o banco. Cache miss executa query e armazena resultado com TTL configuravel. Domain Events disparam invalidacao seletiva quando entidades sao modificadas. Cache keys seguem padrao tenant:entity:id.
