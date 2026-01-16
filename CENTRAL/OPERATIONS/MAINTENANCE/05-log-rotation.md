# Log Rotation

Configuração de rotação de logs para evitar consumo excessivo de disco.

## Logs de Aplicação (Kubernetes)

Logs de containers são gerenciados pelo containerd com rotação automática:

```bash
# Configuração do containerd (/etc/containerd/config.toml)
[plugins."io.containerd.grpc.v1.cri".containerd]
  max-container-log-line-size = 16384

# Limites de log por container
kubectl describe node | grep -A5 "Container Runtime"
```

## Logs do PostgreSQL

Configuração no `postgresql.conf`:

```ini
# Rotação de logs
logging_collector = on
log_directory = 'pg_log'
log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
log_rotation_age = 1d
log_rotation_size = 100MB
log_truncate_on_rotation = off

# Retenção (via logrotate)
# /etc/logrotate.d/postgresql
/var/log/postgresql/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 0640 postgres postgres
}
```

## Logs do Nginx Ingress

```yaml
# ConfigMap do ingress-nginx
apiVersion: v1
kind: ConfigMap
metadata:
  name: nginx-configuration
data:
  access-log-path: "/var/log/nginx/access.log"
  error-log-path: "/var/log/nginx/error.log"
  # Rotação via sidecar
```

## Logs no Loki (Retenção)

Configuração do Loki para retenção de logs:

```yaml
# loki-config.yaml
schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: s3
      schema: v11
      index:
        prefix: loki_index_
        period: 24h

limits_config:
  retention_period: 720h  # 30 dias

compactor:
  working_directory: /loki/compactor
  shared_store: s3
  retention_enabled: true
  retention_delete_delay: 2h
```

## Verificar Uso de Disco

```bash
# Espaço usado por logs em cada node
kubectl get nodes -o name | xargs -I {} kubectl debug {} -it --image=busybox -- du -sh /var/log/

# Logs mais antigos
find /var/log -name "*.log" -mtime +7 -exec ls -lh {} \;

# Limpar logs antigos manualmente (emergência)
find /var/log/containers -name "*.log" -mtime +3 -delete
```

## Alertas

```yaml
- alert: DiskSpaceLow
  expr: (node_filesystem_avail_bytes{mountpoint="/var/log"} / node_filesystem_size_bytes{mountpoint="/var/log"}) < 0.1
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Espaço em disco para logs abaixo de 10% no node {{ $labels.instance }}"
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
