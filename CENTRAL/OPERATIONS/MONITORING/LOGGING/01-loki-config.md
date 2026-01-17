# Loki Configuration

Configuração do Grafana Loki para agregação centralizada de logs do CARF.

## Configuração Principal

```yaml
# loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100
  grpc_listen_port: 9096

common:
  path_prefix: /loki
  storage:
    filesystem:
      chunks_directory: /loki/chunks
      rules_directory: /loki/rules
  replication_factor: 1
  ring:
    kvstore:
      store: inmemory

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: s3
      schema: v11
      index:
        prefix: loki_index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
    cache_ttl: 24h
    shared_store: s3
  aws:
    s3: s3://carf-logs
    region: sa-east-1
    bucketnames: carf-logs

limits_config:
  enforce_metric_name: false
  reject_old_samples: true
  reject_old_samples_max_age: 168h  # 7 dias
  ingestion_rate_mb: 10
  ingestion_burst_size_mb: 20
  max_entries_limit_per_query: 5000
  retention_period: 2160h  # 90 dias

chunk_store_config:
  max_look_back_period: 2160h  # 90 dias

compactor:
  working_directory: /loki/compactor
  shared_store: s3
  retention_enabled: true
  retention_delete_delay: 2h
  retention_delete_worker_count: 150

ruler:
  storage:
    type: local
    local:
      directory: /loki/rules
  rule_path: /loki/rules-temp
  alertmanager_url: http://alertmanager:9093
  ring:
    kvstore:
      store: inmemory
  enable_api: true
```

## Política de Retenção por Label

```yaml
# retention por tipo de log
limits_config:
  retention_period: 2160h  # 90 dias default

  per_tenant_override_config: /etc/loki/overrides.yaml

# overrides.yaml
overrides:
  carf:
    retention_period: 2160h  # 90 dias logs gerais

# Label-based retention via compactor
compactor:
  retention_enabled: true
  delete_request_cancel_period: 24h
```

## Streams e Labels

Labels padrão para logs do CARF:

| Label | Descrição | Exemplo |
|-------|-----------|---------|
| namespace | Namespace K8s | `carf` |
| app | Nome da aplicação | `geoapi` |
| pod | Nome do pod | `geoapi-5f4b7c8d9-x2j4k` |
| container | Container | `geoapi` |
| level | Nível de log | `info`, `warn`, `error` |
| tenant_id | Tenant (multi-tenant) | `tenant-123` |

## Kubernetes Deployment

```yaml
# k8s/loki-deployment.yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: loki
  namespace: monitoring
spec:
  serviceName: loki
  replicas: 1
  selector:
    matchLabels:
      app: loki
  template:
    spec:
      containers:
        - name: loki
          image: grafana/loki:2.9.0
          args:
            - -config.file=/etc/loki/loki-config.yaml
          ports:
            - containerPort: 3100
          volumeMounts:
            - name: config
              mountPath: /etc/loki
            - name: storage
              mountPath: /loki
      volumes:
        - name: config
          configMap:
            name: loki-config
  volumeClaimTemplates:
    - metadata:
        name: storage
      spec:
        accessModes: ["ReadWriteOnce"]
        resources:
          requests:
            storage: 50Gi
```

## Verificação

```bash
# Health check
curl http://loki:3100/ready

# Verificar labels disponíveis
curl http://loki:3100/loki/api/v1/labels

# Query de teste
curl -G http://loki:3100/loki/api/v1/query \
  --data-urlencode 'query={app="geoapi"} |= "error"' \
  --data-urlencode 'limit=10'
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
