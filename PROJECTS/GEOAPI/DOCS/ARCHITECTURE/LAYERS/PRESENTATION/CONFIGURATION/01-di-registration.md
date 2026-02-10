---
type: leaf
status: active
updated: 2026-02-07
---

# DI Registration

O arquivo Program.cs configura todo o container de injecao de dependencia da GEOAPI. Os registros estao organizados por categoria funcional.

## Configuracao de Options

Tres secoes do appsettings sao mapeadas para options tipados: KeycloakOptions, StorageOptions e RedisOptions, cada um vinculado a sua respectiva secao de configuracao.

## Banco de Dados

O CARFDbContext e registrado com Npgsql e a extensao NetTopologySuite para suporte a tipos geograficos PostGIS.

## Autenticacao e Autorizacao

A autenticacao utiliza JWT Bearer via Keycloak. Duas policies de autorizacao sao definidas: RequireAdmin (exige role admin) e RequireAprovador (exige role aprovador).

## MediatR e Validacao

O MediatR registra handlers do assembly de commands e adiciona dois pipeline behaviors: ValidationBehavior (executa FluentValidation antes do handler) e LoggingBehavior (loga requisicoes). Os validators do FluentValidation sao registrados automaticamente por assembly scanning.

## Mapeamento e Repositorios

AutoMapper carrega profiles do assembly de mapeamento. Os repositorios sao registrados como Scoped: IUnitRepository, IHolderRepository e ICommunityRepository.

## Servicos de Infraestrutura

| Servico | Implementacao | Lifetime |
|---------|---------------|----------|
| ITenantContext | TenantContext | Scoped |
| IKeycloakService | KeycloakService | Scoped |
| IFileStorage | S3FileStorage | Scoped |
| ICacheService | RedisCacheService | Scoped |
| INotificationService | SignalRNotificationService | Scoped |
| IConnectionMultiplexer | ConnectionMultiplexer | Singleton |

## Pipeline de Middleware

O Hangfire utiliza PostgreSQL como storage e registra o servidor de jobs. O SignalR e adicionado para comunicacao real-time. Controllers recebem o ValidationFilter como filtro global. CORS permite origens configuradas em Cors:AllowedOrigins com credenciais. O pipeline de middleware segue a ordem: ExceptionHandlingMiddleware, Swagger, CORS, Authentication, Authorization, Controllers, Hub de notificacoes em /hubs/notifications, dashboard Hangfire em /hangfire e health checks em /health.
