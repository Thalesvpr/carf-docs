# CACHE

Implementação caching distribuído do GEOAPI usando Redis para cache de queries frequentes, sessões usuário e dados quasi-static compartilhados entre instâncias API reduzindo carga banco dados e melhorando performance reads. RedisCacheService encapsula StackExchange.Redis com serialização JSON via System.Text.Json, namespacing por tenant evitando colisões keys entre múltiplos clientes e expiration policies TTL baseadas em tipo dado (user sessions 30min, query results 5min, reference data 1h). Cache-aside pattern aplicado em queries onde handler verifica cache primeiro retornando imediatamente se hit ou consultando DB e populando cache se miss, cache invalidation coordenada via pub/sub Redis quando domain events indicam dados alterados (UnitUpdatedEvent invalida cache GetUnitById) e distributed locking Redlock garantindo apenas uma instância executa operação cara evitando thundering herd. Health checks monitoram conectividade Redis e fallback graceful para no-cache quando Redis indisponível mantendo aplicação funcional com performance degradada.

## Arquivos Principais (a criar)

**Core:**
- 01-redis-cache-service.md - Wrapper StackExchange.Redis
- 02-cache-keys-strategy.md - Namespacing e key patterns

**Patterns:**
- 03-cache-aside-pattern.md - Read-through caching
- 04-cache-invalidation.md - Pub/sub based invalidation

**Advanced:**
- 05-distributed-locking.md - Redlock para operações exclusivas
- 06-health-checks.md - Monitoring e fallback graceful

**Configuration:**
- 07-ttl-policies.md - Expiration por tipo de dado
- 08-eviction-policies.md - LRU e memory management

---

**Última atualização:** 2026-01-12
**Status do arquivo**: Incompleto
Descrição: Falta seção GENERATED com índice automático; Muitas listas com bullets (8) antes do rodapé - considerar converter para parágrafo denso.
