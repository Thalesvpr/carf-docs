# DEV Overlay

Kustomization overlay para ambiente de desenvolvimento.

## kustomization.yaml

```yaml
# overlays/dev/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: carf-dev

resources:
  - ../../base

namePrefix: dev-

commonLabels:
  environment: development

images:
  - name: geoapi
    newName: carf/geoapi
    newTag: dev
  - name: geoweb
    newName: carf/geoweb
    newTag: dev

replicas:
  - name: geoapi
    count: 1
  - name: geoweb
    count: 1

patches:
  - path: resources-patch.yaml
  - path: configmap-patch.yaml
```

## Resources Patch

```yaml
# overlays/dev/resources-patch.yaml
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
              cpu: 100m
              memory: 256Mi
            limits:
              cpu: 500m
              memory: 512Mi
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
              cpu: 50m
              memory: 128Mi
            limits:
              cpu: 200m
              memory: 256Mi
```

## ConfigMap Patch

```yaml
# overlays/dev/configmap-patch.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: geoapi-config
data:
  ASPNETCORE_ENVIRONMENT: "Development"
  Logging__LogLevel__Default: "Debug"
  Cors__AllowedOrigins: "http://localhost:3000,http://dev.carf.com.br"
```

## Ingress Patch

```yaml
# overlays/dev/ingress-patch.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: carf-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-staging
spec:
  tls:
    - hosts:
        - api-dev.carf.com.br
        - app-dev.carf.com.br
      secretName: carf-dev-tls
  rules:
    - host: api-dev.carf.com.br
    - host: app-dev.carf.com.br
```

## Deploy

```bash
# Criar namespace
kubectl create namespace carf-dev

# Aplicar overlay
kubectl apply -k overlays/dev

# Verificar recursos
kubectl get all -n carf-dev
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Pronto
