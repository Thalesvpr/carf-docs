# Redis Cache

Implementação de cache distribuído com Redis.

## ICacheService

```csharp
public interface ICacheService
{
    Task<T?> GetAsync<T>(string key, CancellationToken ct = default);
    Task SetAsync<T>(string key, T value, TimeSpan? expiration = null, CancellationToken ct = default);
    Task RemoveAsync(string key, CancellationToken ct = default);
    Task RemoveByPatternAsync(string pattern, CancellationToken ct = default);
}
```

## RedisCacheService

```csharp
public class RedisCacheService : ICacheService
{
    private readonly IConnectionMultiplexer _redis;
    private readonly IDatabase _db;
    private readonly ITenantContext _tenantContext;

    public async Task<T?> GetAsync<T>(string key, CancellationToken ct = default)
    {
        var tenantKey = GetTenantKey(key);
        var value = await _db.StringGetAsync(tenantKey);
        return value.HasValue
            ? JsonSerializer.Deserialize<T>(value!)
            : default;
    }

    public async Task SetAsync<T>(string key, T value, TimeSpan? expiration = null, CancellationToken ct = default)
    {
        var tenantKey = GetTenantKey(key);
        var json = JsonSerializer.Serialize(value);
        await _db.StringSetAsync(tenantKey, json, expiration ?? TimeSpan.FromHours(1));
    }

    public async Task RemoveByPatternAsync(string pattern, CancellationToken ct = default)
    {
        var tenantPattern = GetTenantKey(pattern);
        var server = _redis.GetServer(_redis.GetEndPoints().First());
        var keys = server.Keys(pattern: tenantPattern);
        await _db.KeyDeleteAsync(keys.ToArray());
    }

    private string GetTenantKey(string key) =>
        $"{_tenantContext.TenantId}:{key}";
}
```

## Cache Keys

```csharp
public static class CacheKeys
{
    public static string Unit(Guid id) => $"unit:{id}";
    public static string UnitList(string hash) => $"units:list:{hash}";
    public static string Holder(Guid id) => $"holder:{id}";
    public static string Community(Guid id) => $"community:{id}";
    public static string CommunityStats(Guid id) => $"community:{id}:stats";
}
```

## Cache-Aside Pattern

```csharp
public class CachedUnitRepository : IUnitRepository
{
    private readonly IUnitRepository _inner;
    private readonly ICacheService _cache;

    public async Task<Unit?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        var cached = await _cache.GetAsync<Unit>(CacheKeys.Unit(id), ct);
        if (cached != null) return cached;

        var unit = await _inner.GetByIdAsync(id, ct);
        if (unit != null)
            await _cache.SetAsync(CacheKeys.Unit(id), unit, TimeSpan.FromMinutes(30), ct);

        return unit;
    }
}
```

## Invalidação

```csharp
// Ao atualizar entidade, invalidar cache
public class UnitUpdatedEventHandler : INotificationHandler<UnitUpdatedEvent>
{
    public async Task Handle(UnitUpdatedEvent notification, CancellationToken ct)
    {
        await _cache.RemoveAsync(CacheKeys.Unit(notification.UnitId), ct);
        await _cache.RemoveByPatternAsync("units:list:*", ct);
    }
}
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
