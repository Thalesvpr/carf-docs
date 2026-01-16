# Dashboards Provisioning

Configuração de auto-provisioning de dashboards no Grafana.

## Configuração do Provider

```yaml
# provisioning/dashboards/default.yml
apiVersion: 1

providers:
  - name: 'CARF Dashboards'
    orgId: 1
    folder: 'CARF'
    folderUid: 'carf'
    type: file
    disableDeletion: false
    updateIntervalSeconds: 30
    allowUiUpdates: false
    options:
      path: /var/lib/grafana/dashboards/carf
      foldersFromFilesStructure: true
```

## Estrutura de Pastas

```
/var/lib/grafana/dashboards/
├── carf/
│   ├── geoapi-overview.json
│   ├── postgres-metrics.json
│   └── infrastructure.json
├── alerts/
│   └── alert-overview.json
└── slo/
    └── slo-dashboard.json
```

## Kubernetes ConfigMap para Dashboards

```yaml
# k8s/grafana-dashboards-configmap.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards-provider
  namespace: monitoring
data:
  default.yaml: |
    apiVersion: 1
    providers:
      - name: 'CARF'
        folder: 'CARF'
        type: file
        options:
          path: /var/lib/grafana/dashboards/carf

---
apiVersion: v1
kind: ConfigMap
metadata:
  name: grafana-dashboards-carf
  namespace: monitoring
  labels:
    grafana_dashboard: "1"
data:
  geoapi-overview.json: |
    {
      "title": "GEOAPI Overview",
      "uid": "geoapi-overview",
      ...
    }
```

## Sidecar para Auto-Discovery

```yaml
# Usando Grafana sidecar para descobrir dashboards
spec:
  containers:
    - name: grafana
      env:
        - name: GF_DASHBOARDS_DEFAULT_HOME_DASHBOARD_PATH
          value: /var/lib/grafana/dashboards/carf/geoapi-overview.json

    - name: grafana-sidecar
      image: kiwigrid/k8s-sidecar:1.24.0
      env:
        - name: LABEL
          value: "grafana_dashboard"
        - name: FOLDER
          value: /var/lib/grafana/dashboards
        - name: RESOURCE
          value: "both"
      volumeMounts:
        - name: dashboards
          mountPath: /var/lib/grafana/dashboards
```

## Exportar Dashboard Existente

```bash
# Exportar dashboard por UID
curl -s -u admin:$GRAFANA_PASSWORD \
  "http://grafana:3000/api/dashboards/uid/geoapi-overview" | \
  jq '.dashboard' > geoapi-overview.json

# Remover campos dinâmicos para versionamento
jq 'del(.id, .uid, .version, .iteration)' geoapi-overview.json > geoapi-clean.json
```

## Importar Dashboard via API

```bash
# Importar dashboard JSON
curl -X POST -u admin:$GRAFANA_PASSWORD \
  -H "Content-Type: application/json" \
  -d @geoapi-overview.json \
  "http://grafana:3000/api/dashboards/db"
```

## Notifiers Provisioning

```yaml
# provisioning/notifiers/slack.yml
apiVersion: 1

notifiers:
  - name: slack-ops
    type: slack
    uid: slack-ops
    org_id: 1
    is_default: true
    settings:
      url: $SLACK_WEBHOOK_URL
      recipient: "#ops-alerts"
      mentionChannel: "here"
    secure_settings:
      token: $SLACK_TOKEN
```

## Verificação

```bash
# Listar dashboards provisionados
curl -s -u admin:$GRAFANA_PASSWORD \
  "http://grafana:3000/api/search?type=dash-db" | jq '.[].title'

# Verificar status de provisioning
kubectl logs -l app=grafana -n monitoring | grep -i provision
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
