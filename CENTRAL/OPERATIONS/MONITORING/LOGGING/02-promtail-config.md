# Promtail Configuration

Configuração do Promtail para coleta e envio de logs ao Loki.

## Configuração Principal

```yaml
# promtail-config.yaml
server:
  http_listen_port: 9080
  grpc_listen_port: 0

positions:
  filename: /tmp/positions.yaml

clients:
  - url: http://loki:3100/loki/api/v1/push
    tenant_id: carf
    batchwait: 1s
    batchsize: 1048576  # 1MB
    timeout: 10s

scrape_configs:
  # Logs de containers Kubernetes
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Keep only pods in carf namespace
      - source_labels: [__meta_kubernetes_namespace]
        regex: carf|monitoring
        action: keep

      # Extrair labels
      - source_labels: [__meta_kubernetes_namespace]
        target_label: namespace
      - source_labels: [__meta_kubernetes_pod_name]
        target_label: pod
      - source_labels: [__meta_kubernetes_pod_container_name]
        target_label: container
      - source_labels: [__meta_kubernetes_pod_label_app]
        target_label: app

      # Path dos logs
      - source_labels: [__meta_kubernetes_pod_uid, __meta_kubernetes_pod_container_name]
        target_label: __path__
        replacement: /var/log/pods/*$1/$2/*.log

    pipeline_stages:
      # Parse JSON logs
      - json:
          expressions:
            level: level
            message: message
            timestamp: timestamp
            correlation_id: correlation_id
            tenant_id: tenant_id
            user_id: user_id

      # Set labels from parsed fields
      - labels:
          level:
          tenant_id:

      # Timestamp from log
      - timestamp:
          source: timestamp
          format: RFC3339

      # Output only message field
      - output:
          source: message
```

## Pipeline Stages Detalhado

### Parse de Logs JSON (GEOAPI)

```yaml
pipeline_stages:
  # Logs da aplicação são JSON estruturado
  - json:
      expressions:
        level: level
        message: msg
        timestamp: "@t"
        correlation_id: correlation_id
        tenant_id: tenant_id
        user_id: user_id
        endpoint: endpoint
        method: method
        status_code: status_code
        duration_ms: duration_ms
        exception: exception

  # Labels dinâmicos
  - labels:
      level:
      tenant_id:

  # Métricas de logs (opcional)
  - metrics:
      log_lines_total:
        type: Counter
        description: "Total log lines"
        source: level
        config:
          action: inc
      http_requests_logged:
        type: Counter
        description: "HTTP requests logged"
        source: status_code
        config:
          action: inc
```

### Parse de Logs do Nginx Ingress

```yaml
- job_name: nginx-ingress
  static_configs:
    - targets:
        - localhost
      labels:
        app: nginx-ingress
        __path__: /var/log/nginx/*.log

  pipeline_stages:
    - regex:
        expression: '^(?P<remote_addr>[\d\.]+) - (?P<remote_user>\S+) \[(?P<time_local>[^\]]+)\] "(?P<method>\S+) (?P<request>[^"]+)" (?P<status>\d+) (?P<body_bytes_sent>\d+) "(?P<http_referer>[^"]*)" "(?P<http_user_agent>[^"]*)"'

    - labels:
        method:
        status:

    - timestamp:
        source: time_local
        format: "02/Jan/2006:15:04:05 -0700"
```

## Kubernetes DaemonSet

```yaml
# k8s/promtail-daemonset.yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: promtail
  namespace: monitoring
spec:
  selector:
    matchLabels:
      app: promtail
  template:
    metadata:
      labels:
        app: promtail
    spec:
      serviceAccountName: promtail
      containers:
        - name: promtail
          image: grafana/promtail:2.9.0
          args:
            - -config.file=/etc/promtail/promtail.yaml
          volumeMounts:
            - name: config
              mountPath: /etc/promtail
            - name: varlog
              mountPath: /var/log
              readOnly: true
            - name: varlibdockercontainers
              mountPath: /var/lib/docker/containers
              readOnly: true
            - name: positions
              mountPath: /tmp
      volumes:
        - name: config
          configMap:
            name: promtail-config
        - name: varlog
          hostPath:
            path: /var/log
        - name: varlibdockercontainers
          hostPath:
            path: /var/lib/docker/containers
        - name: positions
          emptyDir: {}
```

## Verificação

```bash
# Verificar targets descobertos
curl http://promtail:9080/targets

# Verificar métricas de ingestão
curl http://promtail:9080/metrics | grep promtail_read_lines_total

# Logs do próprio promtail
kubectl logs -l app=promtail -n monitoring --tail=50
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
