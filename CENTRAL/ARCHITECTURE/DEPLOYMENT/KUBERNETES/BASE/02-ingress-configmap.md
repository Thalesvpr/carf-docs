# Ingress e ConfigMap

Manifests base para Ingress e ConfigMap do CARF.

## Ingress

```yaml
# base/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: carf-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/proxy-body-size: "50m"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "300"
spec:
  tls:
    - hosts:
        - api.carf.com.br
        - app.carf.com.br
      secretName: carf-tls
  rules:
    - host: api.carf.com.br
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: geoapi
                port:
                  number: 80
    - host: app.carf.com.br
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: geoweb
                port:
                  number: 80
```

## ConfigMap Base

```yaml
# base/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: geoapi-config
data:
  ASPNETCORE_ENVIRONMENT: "Production"
  Logging__LogLevel__Default: "Information"
  Logging__LogLevel__Microsoft: "Warning"
  Cache__DefaultTTLMinutes: "60"
  Cors__AllowedOrigins: ""  # Sobrescrito por overlay
```

## Secret Template

```yaml
# base/secrets.yaml (valores via sealed-secrets ou external-secrets)
apiVersion: v1
kind: Secret
metadata:
  name: geoapi-secrets
type: Opaque
stringData:
  ConnectionStrings__DefaultConnection: ""
  Keycloak__ClientSecret: ""
  Redis__Password: ""
```

## ServiceAccount

```yaml
# base/serviceaccount.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: geoapi
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: geoapi-role
rules:
  - apiGroups: [""]
    resources: ["configmaps", "secrets"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: geoapi-rolebinding
subjects:
  - kind: ServiceAccount
    name: geoapi
roleRef:
  kind: Role
  name: geoapi-role
  apiGroup: rbac.authorization.k8s.io
```

## Network Policy

```yaml
# base/networkpolicy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: geoapi-network-policy
spec:
  podSelector:
    matchLabels:
      app: geoapi
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app: nginx-ingress
      ports:
        - port: 8080
  egress:
    - to:
        - podSelector:
            matchLabels:
              app: postgres
      ports:
        - port: 5432
    - to:
        - podSelector:
            matchLabels:
              app: redis
      ports:
        - port: 6379
```

---

**Última atualização:** 2026-01-16
**Status do arquivo**: Review
