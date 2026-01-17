# Infrastructure Dashboard

Dashboard de monitoramento de infraestrutura Kubernetes e recursos de sistema.

## Visão Geral

Dashboard para acompanhamento de recursos de infraestrutura incluindo nodes, pods, CPU, memória, disco e rede.

## Panels

### Row: Cluster Overview

| Panel | Tipo | Query | Descrição |
|-------|------|-------|-----------|
| Total Nodes | Stat | `count(up{job="node"} == 1)` | Nodes ativos |
| Total Pods | Stat | `count(kube_pod_info{namespace="carf"})` | Pods no namespace |
| Pod Restarts (1h) | Stat | `sum(increase(kube_pod_container_status_restarts_total{namespace="carf"}[1h]))` | Restarts recentes |
| Cluster CPU | Gauge | `avg(node:cpu_usage:rate5m) * 100` | CPU médio do cluster |

### Row: Node Resources

| Panel | Tipo | Query |
|-------|------|-------|
| CPU Usage by Node | Time Series | `node:cpu_usage:rate5m * 100` |
| Memory Usage by Node | Time Series | `node:memory_usage:ratio * 100` |
| Disk Usage by Node | Time Series | `node:disk_usage:ratio * 100` |
| Load Average | Time Series | `node_load1`, `node_load5`, `node_load15` |

### Row: Pod Status

| Panel | Tipo | Query |
|-------|------|-------|
| Pod Status | Table | `kube_pod_status_phase{namespace="carf"}` |
| Container Restarts | Time Series | `kube:pod_restarts:rate1h` |
| Pod CPU Usage | Time Series | `sum(rate(container_cpu_usage_seconds_total{namespace="carf"}[5m])) by (pod)` |
| Pod Memory Usage | Time Series | `sum(container_memory_working_set_bytes{namespace="carf"}) by (pod)` |

### Row: Network

| Panel | Tipo | Query |
|-------|------|-------|
| Network Receive | Time Series | `node:network_receive:rate5m` |
| Network Transmit | Time Series | `node:network_transmit:rate5m` |
| Pod Network IO | Time Series | `rate(container_network_receive_bytes_total{namespace="carf"}[5m])` |

### Row: Storage

| Panel | Tipo | Query |
|-------|------|-------|
| Disk Space Available | Time Series | `node_filesystem_avail_bytes{mountpoint="/"}` |
| Disk IOPS | Time Series | `rate(node_disk_reads_completed_total[5m])`, `rate(node_disk_writes_completed_total[5m])` |
| PV Usage | Bar Gauge | `kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes` |

### Row: Kubernetes Events

| Panel | Tipo | Descrição |
|-------|------|-----------|
| Recent Events | Logs | Kubernetes events filtrados por Warning/Error |
| Deployment Status | Table | Status de deployments no namespace |

## Variables

```json
{
  "templating": {
    "list": [
      {
        "name": "namespace",
        "type": "query",
        "query": "label_values(kube_pod_info, namespace)",
        "current": "carf"
      },
      {
        "name": "node",
        "type": "query",
        "query": "label_values(node_uname_info, nodename)"
      },
      {
        "name": "pod",
        "type": "query",
        "query": "label_values(kube_pod_info{namespace=\"$namespace\"}, pod)"
      }
    ]
  }
}
```

## Thresholds Padrão

| Recurso | Warning | Critical |
|---------|---------|----------|
| CPU | 70% | 85% |
| Memory | 80% | 90% |
| Disk | 75% | 90% |
| Pod Restarts (1h) | 1 | 3 |

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
