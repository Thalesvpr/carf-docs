# Cache Invalidation

Runbook para invalidar cache Redis quando dados estão desatualizados ou inconsistentes.

## Diagnóstico

```bash
# Conectar ao Redis
redis-cli -h redis -p 6379

# Verificar memória usada
redis-cli INFO memory | grep used_memory_human

# Listar keys por padrão
redis-cli KEYS "tenant:*" | head -20
redis-cli KEYS "user:*" | head -20
redis-cli KEYS "units:*" | head -20

# Contar keys por prefixo
redis-cli KEYS "tenant:*" | wc -l
```

## Invalidação por Padrão

```bash
# Invalidar cache de tenant específico
redis-cli KEYS "tenant:uuid-do-tenant:*" | xargs redis-cli DEL

# Invalidar cache de usuário específico
redis-cli KEYS "user:user-id:*" | xargs redis-cli DEL

# Invalidar todas as units de um tenant
redis-cli KEYS "*:units:tenant:uuid-do-tenant" | xargs redis-cli DEL

# Invalidar cache de metadados (communities, teams)
redis-cli KEYS "metadata:*" | xargs redis-cli DEL
```

## Flush Completo (Cuidado!)

```bash
# Flush apenas database específico (não toda instância)
redis-cli -n 0 FLUSHDB

# Flush completo (APENAS EM EMERGÊNCIA)
redis-cli FLUSHALL
```

## Verificar TTL

```bash
# Ver TTL de key específica
redis-cli TTL "tenant:uuid:units:list"

# Keys sem TTL (podem acumular)
redis-cli --scan --pattern "*" | while read key; do
  ttl=$(redis-cli TTL "$key")
  if [ "$ttl" = "-1" ]; then
    echo "$key has no TTL"
  fi
done | head -20
```

## Invalidação via API

```bash
# Endpoint de invalidação administrativa (requer role admin)
curl -X POST "https://api.carf.com.br/api/admin/cache/invalidate" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"pattern": "tenant:uuid-tenant:*"}'

# Invalidar cache de entidade específica
curl -X DELETE "https://api.carf.com.br/api/admin/cache/units/unit-id" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

## Configuração de Cache

GEOAPI cache settings:
```json
{
  "Cache": {
    "Redis": {
      "Configuration": "redis:6379",
      "InstanceName": "carf:",
      "DefaultTTL": "00:15:00",
      "MetadataTTL": "01:00:00",
      "ListTTL": "00:05:00"
    }
  }
}
```

## Monitoramento

Grafana dashboard deve mostrar:
- Hit rate (deve ser > 80%)
- Evictions por minuto
- Memória usada vs limite
- Keys por prefixo

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
