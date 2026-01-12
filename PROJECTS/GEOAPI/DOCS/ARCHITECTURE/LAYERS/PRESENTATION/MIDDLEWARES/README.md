# MIDDLEWARES

Middlewares globais do GEOAPI interceptando pipeline HTTP ASP.NET Core em ordem específica aplicando cross-cutting concerns para todos requests. AuthenticationMiddleware valida JWT bearer tokens extraindo claims e populando HttpContext.User antes de qualquer controller executar. ExceptionHandlingMiddleware captura exceções não tratadas convertendo em ProblemDetails JSON padronizado com status code apropriado (500 Internal Server Error, 400 Bad Request para ValidationException) evitando stack traces vazarem para cliente. RequestLoggingMiddleware via Serilog registra método HTTP, path, query string, response status, duração com correlation ID propagado via header X-Correlation-ID rastreando request através sistema distribuído. RateLimitingMiddleware verifica limites por tenant/endpoint baseado em Redis contador incrementado por minuto retornando 429 Too Many Requests quando excedido com header Retry-After. TenantResolutionMiddleware extrai tenant_id de JWT claim ou subdomain injetando em scoped service disponível para repositories aplicarem RLS queries. CorsMiddleware aplica policies permitindo origens autorizadas (frontends GEOWEB/REURBCAD/ADMIN) com credentials e headers específicos.

## Arquivos Principais (a criar)

- 01-authentication-middleware.md - JWT validation e claims extraction
- 02-exception-handling-middleware.md - Global error handling
- 03-request-logging-middleware.md - Serilog structured logging
- 04-rate-limiting-middleware.md - Redis-based throttling
- 05-tenant-resolution-middleware.md - Multi-tenancy context injection
- 06-cors-middleware.md - CORS policies configuration

---

**Última atualização:** 2026-01-12
