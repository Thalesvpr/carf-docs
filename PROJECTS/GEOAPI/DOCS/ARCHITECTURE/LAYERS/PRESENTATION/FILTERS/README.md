# FILTERS

Action filters do GEOAPI aplicando cross-cutting concerns específicos a controllers/actions individuais executando lógica antes/depois de action methods. ValidationFilter verifica ModelState retornando 400 Bad Request com validation errors detalhados quando DTOs inválidos evitando executar action desnecessariamente. AuthorizationFilter customizado verifica permissões granulares além de roles básicas como acesso específico a comunidade via ICommunityAccessChecker baseado em community_authorizations table. AuditFilter registra operações críticas (create/update/delete de entities principais) em audit_logs table com before/after snapshots JSON permitindo compliance e rollback parcial se necessário. CacheFilter implementa HTTP caching com ETags e Last-Modified headers para GET requests idempotentes reduzindo bandwidth e carga servidor quando client possui versão atual. TransactionFilter envolve action em transaction scope explícito quando múltiplas operações precisam atomicidade além do SaveChanges padrão. Filters configurados via attributes declarativos [ValidateModel], [Audit], [RequireCommunityAccess] ou globalmente em Program.cs para todas actions.

## Arquivos Principais (a criar)

- 01-validation-filter.md - ModelState validation automática
- 02-authorization-filter.md - Permissões granulares customizadas
- 03-audit-filter.md - Logging operações críticas
- 04-cache-filter.md - HTTP caching ETags
- 05-transaction-filter.md - Explicit transaction scope

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático.
