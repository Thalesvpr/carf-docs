# PRESENTATION

Camada de apresentação do GEOAPI expondo API REST HTTP via controllers ASP.NET Core recebendo requests externos, validando autenticação/autorização, delegando para Application layer via MediatR e retornando responses padronizadas. CONTROLLERS organizam endpoints por feature (UnitsController, HoldersController, CommunitiesController) recebendo DTOs validados por ModelState, executando commands/queries via IMediator retornando ActionResult<T> com status codes apropriados (200, 201, 400, 401, 403, 404, 409, 500) e headers HATEOAS quando aplicável. MIDDLEWARES interceptam pipeline HTTP global para authentication JWT bearer token validation, exception handling convertendo exceptions em ProblemDetails JSON padronizado, request logging estruturado Serilog com correlation ID rastreando request através sistema e rate limiting por tenant/endpoint prevenindo abuse. FILTERS aplicam cross-cutting concerns específicos como validation filter retornando 400 Bad Request quando ModelState inválido, authorization filter verificando permissões RBAC antes de executar action e audit filter registrando operações críticas para compliance. HUBS SignalR fornecem comunicação real-time bidirecional para notificações push clientes conectados quando domain events ocorrem. CONFIGURATION em Program.cs registra serviços DI, configura middleware pipeline, aplica CORS policies e health checks.

## Subpastas

- **[CONTROLLERS/](./CONTROLLERS/README.md)** - Controllers REST por feature
- **[MIDDLEWARES/](./MIDDLEWARES/README.md)** - Pipeline HTTP global (auth, logging, errors)
- **[FILTERS/](./FILTERS/README.md)** - Cross-cutting concerns específicos
- **[HUBS/](./HUBS/README.md)** - SignalR real-time communication
- **[CONFIGURATION/](./CONFIGURATION/README.md)** - DI registration e startup

---

**Última atualização:** 2026-01-12
