---
type: leaf
status: active
updated: 2026-02-07
---

# Redis Cache

A GEOAPI utiliza Redis como cache distribuido para reduzir carga no banco de dados. Todas as chaves sao prefixadas com o tenantId para garantir isolamento multi-tenant.

## Interface ICacheService

| Metodo | Parametros | Retorno | Descricao |
|--------|-----------|---------|-----------|
| GetAsync | key, cancellationToken | T ou nulo | Busca valor do cache, desserializa de JSON |
| SetAsync | key, value, expiration, cancellationToken | void | Serializa para JSON e grava com TTL (padrao 1 hora) |
| RemoveAsync | key, cancellationToken | void | Remove entrada especifica |
| RemoveByPatternAsync | pattern, cancellationToken | void | Remove todas as chaves que correspondem ao pattern |

## Implementacao RedisCacheService

A classe RedisCacheService implementa ICacheService utilizando IConnectionMultiplexer do StackExchange.Redis. O metodo privado GetTenantKey prefixa toda chave com o formato "{tenantId}:{key}", garantindo que dados de diferentes municipios nunca colidam. A remocao por pattern utiliza o comando KEYS do servidor para encontrar chaves correspondentes e as deleta em lote.

## Convencao de Chaves

| Pattern | Exemplo | Entidade |
|---------|---------|----------|
| unit:{id} | unit:3fa85f64-... | Unidade individual |
| units:list:{hash} | units:list:a1b2c3 | Lista paginada (hash dos filtros) |
| holder:{id} | holder:3fa85f64-... | Titular individual |
| community:{id} | community:3fa85f64-... | Comunidade individual |
| community:{id}:stats | community:3fa85f64-...:stats | Estatisticas da comunidade |

## Padrao Cache-Aside

A classe CachedUnitRepository implementa o decorator pattern sobre IUnitRepository. No GetByIdAsync, primeiro consulta o cache. Se encontrar, retorna imediatamente. Caso contrario, consulta o repositorio real, grava o resultado no cache com TTL de 30 minutos e retorna.

## Invalidacao

O handler UnitUpdatedEventHandler escuta o evento UnitUpdatedEvent e remove tanto a chave individual da unidade quanto todas as chaves de listagem (pattern units:list:*), garantindo consistencia apos atualizacoes.

## Tabela Completa de Cache Keys

| Pattern | TTL | Invalidacao | Exemplo Chave Completa |
|---------|-----|-------------|----------------------|
| unit:{id} | 30min | UnitCreatedEvent, UnitUpdatedEvent, UnitDeletedEvent | tenant-uuid:unit:unit-uuid |
| units:list:{filterHash} | 5min | UnitCreatedEvent, UnitUpdatedEvent, UnitDeletedEvent | tenant-uuid:units:list:a1b2c3 |
| holder:{id} | 30min | HolderUpdatedEvent, HolderDeletedEvent | tenant-uuid:holder:holder-uuid |
| holders:list:{filterHash} | 5min | HolderCreatedEvent, HolderUpdatedEvent | tenant-uuid:holders:list:d4e5f6 |
| community:{id} | 1h | CommunityUpdatedEvent | tenant-uuid:community:comm-uuid |
| community:{id}:stats | 6h | Recalculado por CommunityStatsRefreshJob | tenant-uuid:community:comm-uuid:stats |
| community:{id}:boundary | 24h | CommunityBoundaryChangedEvent | tenant-uuid:community:comm-uuid:boundary |
| legitimation:{id} | 15min | RequestStatusChangedEvent | tenant-uuid:legitimation:leg-uuid |
| user:{id}:permissions | 10min | RoleChangedEvent, CommunityAuthorizationChangedEvent | tenant-uuid:user:user-uuid:permissions |
| tenant:{id}:config | 1h | TenantUpdatedEvent | tenant:tenant-uuid:config |

### Estrategia de TTL

- **Entidades individuais** (unit, holder, community): TTL mais longo (30min-1h) pois invalidacao explicita via domain events garante consistencia
- **Listas paginadas** (units:list, holders:list): TTL curto (5min) pois sao mais frequentemente afetadas por operacoes de criacao/exclusao
- **Estatisticas** (community:stats): TTL longo (6h) pois sao recalculadas pelo job CommunityStatsRefreshJob
- **Boundaries** (community:boundary): TTL muito longo (24h) pois raramente mudam apos definicao inicial
- **Permissoes** (user:permissions): TTL curto (10min) pois mudancas de role devem refletir rapidamente
- **Configuracao de tenant** (tenant:config): TTL moderado (1h) pois configuracoes mudam raramente

### Invalidacao por Domain Event

| Domain Event | Chaves Invalidadas |
|-------------|-------------------|
| UnitCreatedEvent | units:list:* |
| UnitUpdatedEvent | unit:{id}, units:list:* |
| UnitDeletedEvent | unit:{id}, units:list:* |
| HolderCreatedEvent | holders:list:* |
| HolderUpdatedEvent | holder:{id}, holders:list:* |
| HolderDeletedEvent | holder:{id}, holders:list:* |
| CommunityUpdatedEvent | community:{id} |
| CommunityBoundaryChangedEvent | community:{id}:boundary |
| RequestStatusChangedEvent | legitimation:{id} |
| RoleChangedEvent | user:{userId}:permissions |
| CommunityAuthorizationChangedEvent | user:{userId}:permissions |
| TenantUpdatedEvent | tenant:{tenantId}:config |

## Metricas de Cache

A GEOAPI expoe metricas de cache via Prometheus para monitoramento da eficacia do cache.

### Counters Prometheus

| Metrica | Tipo | Labels | Descricao |
|---------|------|--------|-----------|
| cache_hits_total | Counter | entity_type, operation | Total de cache hits |
| cache_misses_total | Counter | entity_type, operation | Total de cache misses |
| cache_evictions_total | Counter | entity_type, reason | Total de evictions (TTL ou invalidacao) |
| cache_set_duration_seconds | Histogram | entity_type | Tempo de escrita no cache |
| cache_get_duration_seconds | Histogram | entity_type | Tempo de leitura do cache |

### Targets de Hit Ratio

| Tipo de Chave | Hit Ratio Target | Justificativa |
|---------------|-----------------|---------------|
| Entidades individuais (unit, holder, community) | > 95% | Acessadas frequentemente, TTL longo, invalidacao por evento |
| Listas paginadas (units:list, holders:list) | > 80% | TTL curto, variacoes de filtro |
| Permissoes (user:permissions) | > 90% | Verificadas em toda requisicao, TTL moderado |
| Estatisticas (community:stats) | > 98% | Recalculadas a cada 6h, leitura frequente |

### Dashboard Grafana

Painel recomendado: hit ratio = `cache_hits_total / (cache_hits_total + cache_misses_total)` agrupado por entity_type. Alerta se hit ratio cair abaixo de 50% por mais de 10 minutos, indicando possivel problema de invalidacao excessiva ou TTL muito curto.

## Consideracoes de Producao

1. **Memoria Redis**: monitorar `used_memory` vs `maxmemory`. Politica de eviction recomendada: `allkeys-lru`
2. **Conexoes**: pool de conexoes via IConnectionMultiplexer (Singleton). Nao criar multiplas instancias
3. **Serialization**: JSON via System.Text.Json com opcoes padrao. Evitar objetos com referencias circulares
4. **Cluster**: em producao, Redis Cluster com 3 masters e 3 replicas para alta disponibilidade
5. **Fallback**: se Redis estiver indisponivel, cache miss silencioso — a aplicacao busca do banco normalmente
