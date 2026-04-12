---
type: leaf
status: review
updated: 2026-02-08
---

# Overview

A GEOAPI e o backend REST API do ecossistema CARF, construido em .NET 9 seguindo Clean Architecture com CQRS via MediatR e Domain-Driven Design. Serve como unica fonte de dados para todos os clientes: REURBWEB (React SPA para analistas), REURBCAD (React Native para campo), REURBMASTER (React Vite para administracao), GEOGIS (plugin QGIS para analise espacial) e WEBDOCS (portal de documentacao).

## Quatro Camadas

A Presentation Layer e a camada mais externa, contendo controllers ASP.NET Core que recebem requisicoes HTTP e delegam para commands e queries via MediatR, middlewares de autenticacao e tratamento de excecoes, filtros de validacao, hubs SignalR para notificacoes real-time e configuracao de Dependency Injection. A Application Layer orquestra casos de uso via Commands de escrita (CreateUnitCommand, LinkHolderCommand, ApproveUnitCommand) e Queries de leitura (GetUnitByIdQuery, ListUnitsQuery), com DTOs, validators FluentValidation e mappers AutoMapper. A Domain Layer e a camada mais interna, sem dependencias externas, contendo entidades (Unit, Holder, Community, LegitimationRequest, Team), value objects imutaveis (CPF, Email, GeoPolygon, Address), contratos de repositorio e domain events. A Infrastructure Layer implementa contratos do Domain com EF Core para PostgreSQL, integracao Keycloak, cliente S3 para armazenamento, cache Redis e jobs Hangfire.

## Multi-Tenancy

O isolamento por municipio e implementado via Row-Level Security do PostgreSQL. Cada requisicao extrai tenant_id do JWT, o TenantMiddleware define a variavel de sessao app.current_tenant e policies RLS filtram automaticamente todas as queries sem filtro explicito no codigo.

## Stack Tecnologico

O backend utiliza .NET 9, ASP.NET Core, EF Core com Npgsql e NetTopologySuite para PostGIS, MediatR para CQRS, FluentValidation, AutoMapper, SignalR, Hangfire para processamento assincrono, StackExchange.Redis para cache e Swashbuckle para documentacao OpenAPI. O banco de dados e PostgreSQL 16 com PostGIS 3.4.
