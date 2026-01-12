# CONFIGURATION

Configuração startup do GEOAPI em Program.cs registrando serviços no DI container, configurando middleware pipeline, aplicando settings de appsettings.json/environment variables e preparando aplicação para receber requests HTTP. Service registration inclui AddDbContext configurando connection string PostgreSQL e retry policy, AddMediatR registrando handlers commands/queries, AddFluentValidation descobrindo validators via assembly scanning, AddAuthentication/AddAuthorization configurando JWT bearer scheme e policies RBAC, AddStackExchangeRedis para cache distribuído, AddHangfire para background jobs, AddSignalR para real-time hubs e AddControllers configurando JSON serialization camelCase e referenceHandling. Middleware pipeline ordena middlewares em sequência crítica (ExceptionHandling → Logging → Cors → Authentication → Authorization → RateLimiting → Routing → Endpoints) garantindo exceptions capturadas primeiro e autenticação validada antes de rate limiting. Health checks registram verificações para PostgreSQL connectivity, Redis availability, S3 storage access e Keycloak reachability expostas em /health endpoint para Kubernetes readiness/liveness probes.

## Arquivos Principais (a criar)

- 01-program-cs-overview.md - Entry point e pipeline completo
- 02-service-registration.md - DI container configuration
- 03-middleware-pipeline.md - Ordem e configuração middlewares
- 04-appsettings-structure.md - Configuration schema por ambiente
- 05-health-checks.md - Readiness e liveness probes
- 06-cors-policies.md - Configuração origens permitidas
- 07-jwt-authentication.md - Bearer token validation setup

---

**Última atualização:** 2026-01-12
