# PROD Overlay

Kustomization overlay para ambiente de produção.

## kustomization.yaml

```yaml
# overlays/prod/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: carf-prod

resources:
  - ../../base
  - hpa.yaml
  - pdb.yaml

commonLabels:
  environment: production

images:
  - name: geoapi
    newName: carf/geoapi
    newTag: "1.2.3"  # Versão específica
  - name: geoweb
    newName: carf/geoweb
    newTag: "1.2.3"

replicas:
  - name: geoapi
    count: 3
  - name: geoweb
    count: 2

patches:
  - path: resources-patch.yaml
  - path: configmap-patch.yaml
  - path: probes-patch.yaml
```

## Resources Patch

```yaml
# overlays/prod/resources-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geoapi
spec:
  template:
    spec:
      containers:
        - name: geoapi
          resources:
            requests:
              cpu: 500m
              memory: 1Gi
            limits:
              cpu: 2000m
              memory: 2Gi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geoweb
spec:
  template:
    spec:
      containers:
        - name: geoweb
          resources:
            requests:
              cpu: 200m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
```

## HPA (Horizontal Pod Autoscaler)

```yaml
# overlays/prod/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: geoapi-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: geoapi
  minReplicas: 3
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

## PDB (Pod Disruption Budget)

```yaml
# overlays/prod/pdb.yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: geoapi-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: geoapi
---
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: geoweb-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: geoweb
```

## Probes Patch (mais agressivo)

```yaml
# overlays/prod/probes-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geoapi
spec:
  template:
    spec:
      containers:
        - name: geoapi
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2
```

## Deploy

```bash
# Aplicar em produção
kubectl apply -k overlays/prod

# Verificar HPA
kubectl get hpa -n carf-prod

# Verificar PDB
kubectl get pdb -n carf-prod
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
