# Base Deployments

Manifests Kubernetes base para deployments do CARF usando Kustomize.

## GEOAPI Deployment

```yaml
# base/geoapi-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geoapi
  labels:
    app: geoapi
    component: backend
spec:
  replicas: 1  # Sobrescrito por overlay
  selector:
    matchLabels:
      app: geoapi
  template:
    metadata:
      labels:
        app: geoapi
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: geoapi
      containers:
        - name: geoapi
          image: geoapi:latest  # Tag sobrescrita por overlay
          ports:
            - containerPort: 8080
              name: http
          envFrom:
            - configMapRef:
                name: geoapi-config
            - secretRef:
                name: geoapi-secrets
          resources: {}  # Definido por overlay
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 5
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
```

## GEOWEB Deployment

```yaml
# base/geoweb-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: geoweb
  labels:
    app: geoweb
    component: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      app: geoweb
  template:
    metadata:
      labels:
        app: geoweb
    spec:
      containers:
        - name: geoweb
          image: geoweb:latest
          ports:
            - containerPort: 3000
              name: http
          livenessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /api/health
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
```

## Services

```yaml
# base/services.yaml
apiVersion: v1
kind: Service
metadata:
  name: geoapi
spec:
  selector:
    app: geoapi
  ports:
    - port: 80
      targetPort: 8080
      name: http
---
apiVersion: v1
kind: Service
metadata:
  name: geoweb
spec:
  selector:
    app: geoweb
  ports:
    - port: 80
      targetPort: 3000
      name: http
```

## Kustomization

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - geoapi-deployment.yaml
  - geoweb-deployment.yaml
  - services.yaml
  - configmap.yaml
  - ingress.yaml
  - serviceaccount.yaml
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
