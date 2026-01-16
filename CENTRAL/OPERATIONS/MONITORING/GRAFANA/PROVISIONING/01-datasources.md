# Datasources Provisioning

Configuração de auto-provisioning de datasources no Grafana.

## Prometheus

```yaml
# provisioning/datasources/prometheus.yml
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus-server:9090
    isDefault: true
    editable: false
    jsonData:
      timeInterval: "15s"
      httpMethod: POST
      manageAlerts: true
      prometheusType: Prometheus
      prometheusVersion: "2.45.0"
```

## Loki

```yaml
# provisioning/datasources/loki.yml
apiVersion: 1

datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
    jsonData:
      maxLines: 1000
      derivedFields:
        - datasourceUid: tempo
          matcherRegex: "correlation_id=(\\w+)"
          name: correlation_id
          url: "$${__value.raw}"
```

## PostgreSQL (Direct)

```yaml
# provisioning/datasources/postgres.yml
apiVersion: 1

datasources:
  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    user: grafana_readonly
    secureJsonData:
      password: $GRAFANA_POSTGRES_PASSWORD
    jsonData:
      database: carf
      sslmode: require
      maxOpenConns: 5
      maxIdleConns: 2
      connMaxLifetime: 14400
    editable: false
```

## Alertmanager

```yaml
# provisioning/datasources/alertmanager.yml
apiVersion: 1

datasources:
  - name: Alertmanager
    type: alertmanager
    access: proxy
    url: http://alertmanager:9093
    jsonData:
      implementation: prometheus
```

## Kubernetes ConfigMap

```yaml
# k8s/grafana-datasources-configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-datasources
  namespace: monitoring
  labels:
    grafana_datasource: "1"
data:
  datasources.yaml: |
    apiVersion: 1
    datasources:
      - name: Prometheus
        type: prometheus
        access: proxy
        url: http://prometheus-server:9090
        isDefault: true
      - name: Loki
        type: loki
        access: proxy
        url: http://loki:3100
      - name: Alertmanager
        type: alertmanager
        access: proxy
        url: http://alertmanager:9093
```

## Volume Mount no Deployment

```yaml
# Grafana deployment snippet
spec:
  containers:
    - name: grafana
      volumeMounts:
        - name: datasources
          mountPath: /etc/grafana/provisioning/datasources
  volumes:
    - name: datasources
      configMap:
        name: grafana-datasources
```

## Verificação

```bash
# Verificar datasources provisionados
curl -s -u admin:$GRAFANA_PASSWORD \
  http://grafana:3000/api/datasources | jq '.[].name'

# Testar conexão de datasource
curl -s -u admin:$GRAFANA_PASSWORD \
  http://grafana:3000/api/datasources/1/health
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
